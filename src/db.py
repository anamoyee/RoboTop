from defaults import DBUserData, db_user_data
from imports import json, os, p, sqlite3, tcr

if True: # \/ # Prep
  script_directory = p.Path(__file__).resolve().parent
  os.chdir(script_directory)

  db_file_location = script_directory.parent.parent / "robotop.db"

  conn = sqlite3.connect(db_file_location)
  cursor = conn.cursor()

  cursor.execute('''
      CREATE TABLE IF NOT EXISTS users (
          user_id INTEGER PRIMARY KEY,
          user_settings TEXT
      )
  ''')

  conn.commit()
  conn.close()

def read(user_id: int) -> dict:
  """### Read & return the data found at key `user_id`.

  In case of missing value return a default dictionary
  """
  if not isinstance(user_id, int):
    raise tcr.error.NotIntegerError(user_id)

  conn = sqlite3.connect(db_file_location)
  cursor = conn.cursor()

  cursor.execute("SELECT user_settings FROM users WHERE user_id = ?", (user_id,))
  result = cursor.fetchone()

  conn.close()

  if result:
    user_settings_json = result[0]
    return json.loads(user_settings_json)

  raise KeyError(user_id)

def write(user_id: int, data: dict) -> None:
  """### Overwrite data found at key `user_id` in the database."""
  if not isinstance(user_id, int):
    raise tcr.error.NotIntegerError(user_id)

  conn = sqlite3.connect(db_file_location)
  cursor = conn.cursor()

  # Convert the user_settings dictionary to a JSON string
  user_settings_json = json.dumps(data)

  # Insert or replace the user data in the table
  cursor.execute("INSERT OR REPLACE INTO users (user_id, user_settings) VALUES (?, ?)", (user_id, user_settings_json))

  conn.commit()
  conn.close()

def keys() -> list[int]:
    conn = sqlite3.connect(db_file_location)
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]

    conn.close()

    return user_ids

def items() -> dict[int, DBUserData]:
    user_dict = {}
    user_ids = keys()

    for user_id in user_ids:
        user_data = read(user_id)
        user_dict[user_id] = user_data

    return user_dict
