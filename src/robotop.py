if True:  # \/ # PyVersion // assert sys.version_info[:2] == (3, 11)
  if __import__('sys').version_info[:2] != (3, 11):
    msg = 'Use py311'
    raise ValueError(msg)

if True:  # \/ # Imports
  from db import backup_all_databases, db
  from execute import execute
  from imports import *

if True:  # \/ # BotApp
  bot = lb.BotApp(
    token=token(),
    #   banner=None,
    default_enabled_guilds=S.DEFAULT_ENABLED_GUILDS,
  )

if True:  # \/ # Utilities
  if True:  # \/ # Synchronous

    def F(item: str) -> str:
      return eval(f'f{item!r}')

    def embed(
      title: str,
      description: str,
      *,
      url=None,
      color=None,
      timestamp=None,
      thumbnail=None,
      footer=None,
      footer_icon=None,
      author: dict | None = None,
      image=None,
      fields: list | None = None,
    ) -> hikari.Embed:
      if (title is not Null and not title.strip()) or (
        description is not Null and not description.strip()
      ):
        msg = f'Both title and description must be non-whitespace-only strings unless explicitly specified the title to be Null, got Title: {title!r}, Description: {description!r}'
        raise ValueError(msg)

      if fields is None:
        fields = []

      if author is None:
        author = {}

      out = hikari.Embed(
        title=title if title is not Null else None,
        description=description if description is not Null else None,
        color=color,
        timestamp=timestamp,
        url=url,
      )

      if thumbnail:
        out = out.set_thumbnail(thumbnail)

      if footer:
        out = out.set_footer(text=footer, icon=footer_icon)
      if author:
        out = out.set_author(**author)
      if image:
        out = out.set_image(image)

      for field in fields:
        if len(field) == 2:
          field = (*field, False)
        out = out.add_field(field[0], field[1], inline=field[2])
      return out

    def get_prefix(guild_id: int | str | None = None) -> str:
      """Return guild prefix, if no `guild_id` is passed in, return default (and DM) prefix."""
      if guild_id is None:
        return default.db_guild_data['prefix']
      return db.guild.read(guild_id)['prefix']

    def get_prefix_case_sensitivity(guild_id: int | str | None = None) -> bool:
      """Return guild prefix's case sensitivity, if no `guild_id` is passed in, return default (and DM) prefix's case sensitivity."""
      if guild_id is None:
        return default.db_guild_data['prefix_case_sensitive']
      return db.guild.read(guild_id)['prefix_case_sensitive']

    def is_dm_event(event: hikari.Event) -> bool:
      """Return True if the event is a DM-related event, else return False."""
      return hasattr(event, 'guild_id')

    def get_author_from_event(event: hikari.Event):
      """Try to return an author or member from an event."""
      try:
        return event.author
      except AttributeError:
        try:
          return event.member
        except AttributeError:
          return event.old_member

  if True:  # \/ # Assynchronous

    async def debug_send(
      channel_id_or_responder: int | str | Callable,
      text_or_dictmessage: list | str | types.DictMessage,
      *,
      as_dictmessage=False,
    ) -> hikari.Message:
      def debug_prepare(content: str | int | Iterable) -> str:
        if isinstance(content, str):
          return codeblock(f'{content!r}', langcode='py')
        elif isinstance(content, Iterable):
          return codeblock(tcr.print_iterable(content, raw=True), langcode='py')
        return codeblock(repr(content))

      if not as_dictmessage:
        text_or_dictmessage = {'content': text_or_dictmessage}
      text_or_dictmessage['content'] = debug_prepare(text_or_dictmessage['content'])
      if channel_id_or_responder in ['raw', 'return']:
        return text_or_dictmessage
      if isinstance(channel_id_or_responder, int | str):
        channel_id_or_responder = int(channel_id_or_responder)
        return await bot.rest.create_message(channel=channel_id_or_responder, **text_or_dictmessage)
      else:
        return await channel_id_or_responder(**text_or_dictmessage)

    async def error_send(): ...


if True:  # \/ # Prefix Commands
  if True:  # \/ # Guild

    def parse_guild_prefix_event(event: hikari.GuildMessageCreateEvent) -> types.ParsedPrefixEvent:
      prefix = get_prefix(event.guild_id)
      prefixed = event.content.startswith(prefix)
      message = event.content.removeprefix(prefix)
      return {
        'prefix': prefix,
        'message': message,
        'prefixed': prefixed,
      }

  if True:  # \/ # DMs

    def parse_DM_prefix_event(event: hikari.DMMessageCreateEvent) -> types.ParsedPrefixEvent:
      prefix = get_prefix()
      prefixed = event.content.startswith(prefix)
      message = event.content.removeprefix(prefix)
      return {
        'prefix': prefix,
        'message': message,
        'prefixed': prefixed,
      }


if True:  # \/ # Event listeners
  if True:  # \/ # Messages

    async def on_message(
      event: hikari.GuildMessageCreateEvent | hikari.DMMessageCreateEvent, *, in_dms: bool
    ):
      if not event.is_human:
        return
      parsed = parse_DM_prefix_event(event) if in_dms else parse_guild_prefix_event(event)
      await debug_send(event.message.respond, parsed)

    @bot.listen(hikari.GuildMessageCreateEvent)
    async def on_GuildMessageCreateEvent(event: hikari.GuildMessageCreateEvent):
      await on_message(event, in_dms=False)

    @bot.listen(hikari.DMMessageCreateEvent)
    async def on_DMMessageCreateEvent(event: hikari.DMMessageCreateEvent):
      await on_message(event, in_dms=True)

  if True:  # \/ # Globals

    @bot.listen(hikari.StartingEvent)
    async def on_StartingEvent(event: hikari.StartingEvent): ...

    @bot.listen(hikari.StartedEvent)
    async def on_StartedEvent(event: hikari.StartedEvent): ...

    @bot.listen(hikari.StoppingEvent)
    async def on_StoppingEvent(event: hikari.StoppingEvent): ...

    @bot.listen(hikari.StoppedEvent)
    async def on_StoppedEvent(event: hikari.StoppedEvent): ...


if True:  # \/ # Run
  if testmode:
    text = ''.join(
      [
        f'{c("RED", "Black") if i % 2 == 0 else c("YELLOW", "white")}{x}'
        for i, x in enumerate(f' Running in testmode ')
      ]
    ) + c('reset')
    kon.log(text)
  bot.run(status=STATUS, activity=ACTIVITY)
