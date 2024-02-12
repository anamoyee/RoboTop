from functools import partial

from hikari import DMMessageCreateEvent as _DMMCE
from hikari import GuildMessageCreateEvent as _GMCE
from hikari import MessageCreateEvent as _MessageCreateEvent
from tcrutils import console as kon

import db
from imports import (
  _execute_embed,
  _execute_role_mentions,
  _execute_user_mentions,
)


def _flatten(args: tuple | list) -> list:
  return [x.lower() for x in args]


def _bool_to_str(bul: bool) -> str:  # noqa: FBT001
  if bul:
    return 'true'
  else:
    return 'false'


def _str_to_bool(string: str) -> bool:
  if not string:
    return False

  if string.lower() in ['false', '0']:
    return False

  return True


if True:  # \/ # User

  def mention(*args: str, event: _MessageCreateEvent) -> str:
    """### Return mention of the user.

    Args:
      - 'noping' - Will not ping the user but add an actual mention
      - user_id  - Will insert that

    Example output:
        `<@507642999992352779>`
    """

    args = _flatten(args)
    yesping = 'noping' not in args

    if not yesping:
      args.remove('noping')

    id_ = args[0] if len(args) > 0 else event.author.id

    if (
      yesping
      and not db.user.read(id_)['acs_reducedPings']
      and str(id_).isnumeric()
      and (id_ := int(id_)) >= 0
      and id_ <= 9223372036854775807
    ):
      _execute_user_mentions.add(id_)
    return f'<@{id_}>'

  def username(*args: str, event: _MessageCreateEvent) -> str:
    """### Return the username of the user - the unique one, not the displayname, may still not be unique if user/bot still uses a tag.

    This should be unique for all users

    Example output:
        `thecreatorrrr`
    """

    return event.author.username

  async def globalname(*args: str, event: _MessageCreateEvent) -> str:
    """### Return the globalname of the user - the NON-unique one, not the username. If user does not have one, fall back to username.

    This is not unique for all users

    Example output:
        `thecreatorrrr`
    """

    id = args[0] if args else None

    if id is None:
      return event.author.global_name or event.author.username

    user = await event.app.rest.fetch_user(id)
    return user.global_name or user.username

  async def displayname(*args, event: _MessageCreateEvent, in_dms: bool) -> str:
    """### Return the displayname of the user.

    This is not unique for all users

    #### Displayname is defined as follows:
      1. First it checks if user has a `nickname` (eg. MyCoolServerNickname),
      2. If user does not have one, `globalname` (eg. τ{ℎ∈ℂ}Γ(e)∀⊤∅ℜ⁴) - will not be unique for many users
      3. If user does not have one, `username` (eg. thecreatorrrr) - the discord's unique username

    #### Example output:
      `thecreatorrrr`
    """  # noqa: RUF002

    if in_dms:
      return event.author.global_name or event.author.username

    event: _GMCE = event

    id = args[0] if args else event.author_id

    member = await event.app.rest.fetch_member(event.guild_id, id)

    return member.display_name

  def discriminator(*, event: _MessageCreateEvent):
    """### Return the tag/discriminator of the user."""
    return event.author.discriminator.zfill(4)


if True:  # \/ # Other

  def comment() -> str:
    """### Ignores any input (returns `''`).

    Example:
      {username}{#| ← Returns the user's name }
    Output of example:
      thecreatorrrr
    """
    return ''

  def indms(in_dms) -> str:
    """Return True if in DMs, false otherwise."""

  async def evaluate(*args, execute, event: _MessageCreateEvent):
    """Do execute() on a substring of execute."""
    return (await execute(' '.join(args), event=event))['content']


if True:  # \/ # {Other}

  def _curly_brackets1(*args):
    """Return a literal `{`."""
    return '{'

  def _curly_brackets2(*args):
    """Return a literal `}`."""
    return '}'

  def _CURLY_BRACKETS_ARE_FUCKED_AGAIN(*args):
    return 'CURLY BRACKETS ARE FUCKED AGAIN 😠'


# fmt: off
aliases = {
  **{x: y for x, y in globals().copy().items() if not x.startswith('_')},

  **{ # User
    '@':  mention,
    '@@': partial(mention, "noping"),

    "discrim": discriminator,
    "tag":     discriminator,
  },

  **{ # Other
    '#':    comment,
    '//':   comment,
    '<!--': comment,
    '<--':  comment,
    "'":    comment,
    '--':   comment,

    "indm":   indms,
    "in_dm":  indms,
    "in_dms": indms,
    "in dm":  indms,
    "in dms": indms,

    'eval': evaluate,
    'exec': evaluate,
    'execute': evaluate
  },

  **{ # {Other}
    '[': _curly_brackets1,
    ']': _curly_brackets2,

    "ℎ∈ℂ": _CURLY_BRACKETS_ARE_FUCKED_AGAIN,  # noqa: RUF001
  },
}
