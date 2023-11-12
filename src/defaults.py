#####


from typing import TypedDict


class DBUserData(TypedDict):
  first_seen: int | None

class DBGuildData(TypedDict):
  prefix: str

db_user_data: DBUserData = {
  "first_seen": None, # Unix timestamp of first interaction with user on that id
                      # None = Never interacted
}

db_guild_data: DBGuildData = {
  "first_seen": None, # Unix timestamp of first interaction with guild on that id
                      # None = Never interacted

  "prefix": "r!"      # The default prefix for guilds
}