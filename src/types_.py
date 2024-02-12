from collections.abc import Callable, Sequence
from enum import Enum
from typing import TypedDict

from hikari import (
  Embed,
  MessageFlag,
  PartialMessage,
  PartialSticker,
  api,
  files,
  guilds,
  snowflakes,
  undefined,
  users,
)


class ParsedMessageEvent(TypedDict):
  prefix: str
  message: str
  prefixed: bool


class DictMessage(TypedDict):
  content: str
  attachment: undefined.UndefinedOr[files.Resourceish]
  attachments: undefined.UndefinedOr[Sequence[files.Resourceish]]
  component: undefined.UndefinedOr[api.CommandBuilder]
  components: undefined.UndefinedOr[Sequence[api.ComponentBuilder]]
  embed: undefined.UndefinedOr[Embed]
  embeds: undefined.UndefinedOr[Sequence[Embed]]
  sticker: undefined.UndefinedOr[snowflakes.SnowflakeishOr[PartialSticker]]
  stickers: undefined.UndefinedOr[snowflakes.SnowflakeishSequence[PartialSticker]]
  tts: undefined.UndefinedOr[bool]
  reply: undefined.UndefinedOr[snowflakes.SnowflakeishOr[PartialMessage]]
  reply_must_exist: undefined.UndefinedOr[bool]
  mentions_everyone: undefined.UndefinedOr[bool]
  mentions_reply: undefined.UndefinedOr[bool]
  user_mentions: undefined.UndefinedOr[snowflakes.SnowflakeishSequence[users.PartialUser] | bool]
  role_mentions: undefined.UndefinedOr[snowflakes.SnowflakeishSequence[guilds.PartialRole] | bool]
  flags: undefined.UndefinedType | (int | MessageFlag)


class CTF:
  NONE = 1 << 0
  DEV = 1 << 1
  HIDDEN = 1 << 2  # Not visible in r!help and other places if any.
  SPECIAL = 1 << 3  # I literally forgor whta this meant 💀
  DM_ONLY = 1 << 4
  GUILD_ONLY = 1 << 5


class CAT(Enum):
  NONE = None
  FUN = 'fun'
  IMAGES = 'images'
  INFORMATION = 'information'
  RANDOM = 'random'
  TOOLS = 'tools'
  SERVER = 'server'
  SETTINGS = 'settings'
  MODERATION = 'moderation'


class CommandsLookup(TypedDict):
  function: Callable
  category: str | None  # None if no category contains this command
  flags: int


class CommandCategoryType(TypedDict):
  name: str
  emoji: str
