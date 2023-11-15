#####


from typing import TypedDict


class DBUserData(TypedDict):
  first_seen: int | None
  acs_reducedPings: bool


class DBGuildData(TypedDict):
  first_seen: int | None
  prefix: str
  prefix_case_sensitive: bool


db_user_data: DBUserData = {
  'first_seen': None,  # Unix timestamp of first interaction with user on that id
  # None = Never interacted
  'acs_reducedPings': False,  # Account Settings: Reduced pings
}

db_guild_data: DBGuildData = {
  'first_seen': None,  # Unix timestamp of first interaction with guild on that id
  # None = Never interacted
  'prefix': 'r!',  # The default prefix for guilds
  'prefix_case_sensitive': True,  # The default prefix case sensitivity for guilds
}
