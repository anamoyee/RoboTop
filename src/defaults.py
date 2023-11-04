from typing import TypedDict


class DBUserData(TypedDict):
    first_seen: int | None

db_user_data: DBUserData = {
  "first_seen": None, # Unix timestamp of first interaction with the userdb on that id
                      # None = Never interacted
}
