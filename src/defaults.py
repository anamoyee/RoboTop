from typing import TypedDict

# fmt: off

class DBUserData(TypedDict):
  first_seen:       int
  acs_reducedPings: bool


class DBGuildData(TypedDict):
  first_seen:            int
  first_seen_version:    int
  prefix:                str
  prefix_case_sensitive: bool
  commands:              dict[str, bool]


db_user_data: DBUserData = {
  'first_seen': None,  # Unix timestamp of first interaction with user on that id
                       # Actual 'None' will never be returned, this value is always updated on db.read() if and only if it == None

  'acs_reducedPings': False,  # Account Settings: Reduced pings on/off by default
}

db_guild_data: DBGuildData = {
  'first_seen': None,  # Unix timestamp of first interaction with guild on that id
                       # Actual 'None' will never be returned, this value is always updated on db.read() if and only if it == None

  'prefix': 'r!',  # The default prefix for guilds

  'prefix_case_sensitive': True,  # The default prefix case sensitivity for guilds

  'commands': { # Whether the commands are enabled or disabled in a guild by default
    'prefix':  True,
    'execute': True,
    '8ball':   True,
  },
}
