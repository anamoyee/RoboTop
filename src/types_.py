from collections.abc import Sequence
from typing import TypedDict, Union

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


class ParsedPrefixEvent(TypedDict):
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
