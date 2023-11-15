import copy
import shelve
import shutil
from abc import ABC
from datetime import datetime
from functools import wraps

import defaults
from imports import Any, ItemsView, KeysView, Mapping, ValuesView, os, p, tcr, unix

_db_directory_name = 'RoboTopDB'


if True:  # \/ # Prep
  _src_directory = p.Path(__file__).resolve().parent
  os.chdir(_src_directory)

  _db_folder_location = _src_directory.parent.parent / _db_directory_name
  _db_folder_location.mkdir(exist_ok=True)

  def backup_all_databases():
    curr_date = datetime.now().strftime('%d-%m-%Y %H;%M;%S')
    backup_folder = _db_folder_location.parent / f'{_db_directory_name} Backup'
    backup_folder.mkdir(exist_ok=True)
    backup_location = backup_folder / tcr.path.newdir(f'Backup {curr_date}', path=backup_folder)
    shutil.copytree(_db_folder_location, backup_location)

    def delete_old_backups(folder_path, num_to_keep=10):
      all_folders = [
        f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))
      ]
      all_folders.sort(key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
      num_to_delete = max(0, len(all_folders) - num_to_keep)
      for i in range(num_to_delete):
        folder_to_delete = os.path.join(folder_path, all_folders[i])
        shutil.rmtree(folder_to_delete)

    delete_old_backups(str(backup_folder), 20)

  backup_all_databases()


def _opendb(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    with shelve.open(str(args[0]._path)) as _db:
      if '_db' in kwargs:
        tcr.console.error(
          "Do not pass _db to database calls, it's handled automatically, the value was voided"
        )
      kwargs = {**kwargs, '_db': _db}
      return func(*args, **kwargs)

  return wrapper


class _DBInterace(ABC):
  """ABC for database interfaces."""

  _path: p.Path

  @_opendb
  def keys(self, *, tolist: bool = True, _db: shelve.Shelf) -> KeysView:
    """Return KeysView of `db`, unless todict=True, then return `deepcopy(db.keys())`."""
    a = _db.keys()
    if tolist:
      a = copy.deepcopy(list(a))
    return a

  @_opendb
  def values(self, *, tolist: bool = True, _db: shelve.Shelf) -> ValuesView:
    """Return ValuesView of `db`, unless todict=True, then return `deepcopy(db.values())`."""
    a = _db.values()
    if tolist:
      a = copy.deepcopy(list(a))
    return a

  @_opendb
  def items(self, *, todict: bool = True, _db: shelve.Shelf) -> ItemsView:
    """Return ItemsView of `db`, unless `todict=True`, then return `deepcopy(db.items())`."""
    a = _db.items()
    if todict:
      a = copy.deepcopy(dict(a))
    return a

  @_opendb
  def clear(self, *, _db: shelve.Shelf) -> None:
    """Clear the current database. Effectively `underlying_dict.clear()`."""
    _db.clear()

  @_opendb
  def pop(self, key: str, /, *, _db: shelve.Shelf):
    return _db.pop(key)

  @_opendb
  def update(self, values: Mapping[str, Any], /, *, _db: shelve.Shelf, **kwargs) -> None:
    _db.update({str(x): y for x, y in {**values, **kwargs}.items()})

  @_opendb
  def read(self, key: int | str, *, _db: shelve.Shelf) -> dict:
    key = str(key)
    this = dict(_db).copy().get(key) or self._thisdefault
    this = {x: y for x, y in this.items() if x in self._thisdefault}
    result = tcr.merge_dicts(this, self._thisdefault, strict=True)
    if 'first_seen' in result and result['first_seen'] is None:
      result['first_seen'] = unix()
    self.write(key, result)
    return result

  @_opendb
  def write(self, key: int | str, data: dict | None = None, *, _db: shelve.Shelf, **kwargs) -> dict:
    if data is None:
      data = {}
    data = {**data, **kwargs}
    key = str(key)
    previous_data = _db.get(key) or {}
    previous_data = {x: y for x, y in previous_data.items() if x in self._thisdefault}
    try:
      merged = tcr.merge_dicts(data, previous_data, self._thisdefault, strict=True)
    except ValueError as e:
      etitle = tcr.extract_error(e, raw=True)[1]
      msg = f'Unknown value: ({etitle[etitle.index("(")+1:etitle.index(")")]}); See defaults.py'
      raise ValueError(msg) from e
    if 'first_seen' in merged and merged['first_seen'] is None:
      merged['first_seen'] = unix()
    _db[key] = merged
    return _db[key]

  @_opendb
  def fix(self, *, _db: shelve.Shelf) -> dict:
    """Remove old keys that are not in the default dict and restores default dict missing keys."""
    new_db = {}
    for k, v in _db.items():
      new_db.update({k: {x: y for x, y in v.items() if x in self._thisdefault}})
    for k, v in new_db.copy().items():
      new_db[k] = tcr.merge_dicts(v, self._thisdefault)
      if 'first_seen' in new_db[k] and new_db[k]['first_seen'] is None:
        new_db[k]['first_seen'] = unix()

    self.override(new_db)

  @_opendb
  def override(self, new_db: dict, *, _db: shelve.Shelf):
    """Clear the database, then replace it with `new_db`."""
    _db.clear()
    _db.update(new_db)

  def get_default(self) -> dict:
    return self._thisdefault


class __User(_DBInterace):
  """Handles user-related DB storage."""

  _path = _db_folder_location / 'user.db'
  _thisdefault = defaults.db_user_data

  def read(self, user_id: int | str) -> defaults.DBUserData:
    return super().read(key=user_id)

  def write(
    self, user_id: int | str, data: defaults.DBUserData | None = None, **kwargs
  ) -> defaults.DBUserData:
    return super().write(key=user_id, data=data, **kwargs)


class __Guild(_DBInterace):
  """Handles guild-related DB storage."""

  _path = _db_folder_location / 'guild.db'
  _thisdefault = defaults.db_guild_data

  def read(self, guild_id: int | str) -> defaults.DBGuildData:
    return super().read(key=guild_id)

  def write(
    self, guild_id: int | str, data: defaults.DBGuildData | None = None, **kwargs
  ) -> defaults.DBGuildData:
    return super().write(key=guild_id, data=data, **kwargs)


user = __User()
guild = __Guild()

user.fix()
guild.fix()


class db:
  user = user
  guild = guild


__all__ = ['user', 'guild', 'backup_all_databases']
