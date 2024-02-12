if True:  # \/ # PyVersion // assert sys.version_info[:2] == (3, 11)
  if __import__('sys').version_info[:2] != (3, 11):
    msg = 'Use py311'
    raise ValueError(msg)

if True:  # \/ # Imports
  from db import backup_all_databases, db
  from execute import ExecuteBracketsError, ExecuteParameterError, execute
  from imports import *

if True:  # \/ # BotApp

  def token():
    """Return selected token."""
    a = TOKEN2 if S.TESTMODE else TOKEN
    if a is None:
      msg = (
        f"{tcr.c('Red')}Unknown token - check TOKEN{'2' if S.TESTMODE else ''}.txt{tcr.c('reset')}"
      )
      raise tcr.error.ConfigurationError(msg)
    return a.strip()

  bot = lb.BotApp(
    token=token(),
    banner='hikari',
    default_enabled_guilds=S.DEFAULT_ENABLED_GUILDS,
    intents=hikari.Intents.ALL,
  )

  del TOKEN, TOKEN2, TOKEN_FILE, TOKEN2_FILE, token

if True:  # \/ # Commands
  command_categories: dict[str, types.CAT]
  commands: dict[str | bool | None | Null, types.CommandsLookup]

  if True:  # Setup Commands
    if True:  # \/ # Invalid / Restricted

      async def _unknown_command(
        *,
        cmdname: str,
        event: hikari.MessageCreateEvent,
        **kwargs,
      ):
        """Invalid command - Sent when user specified an unknown command."""
        await event.message.respond(rng.choice(pool.command_doesnt_exist).replace('{cmd}', cmdname))

      async def _not_in_dms(
        *,
        cmdname: str,
        event: hikari.MessageCreateEvent,
        **kwargs,
      ):
        """Guild command in DMs."""
        await event.message.respond(rng.choice(pool.guild_command_in_dms).replace('{cmd}', cmdname))

      async def _not_in_guild(
        *,
        cmdname: str,
        event: hikari.MessageCreateEvent,
        **kwargs,
      ):
        """DM command in Guild."""
        await event.message.respond(random(pool.dm_command_in_guild).replace('{cmd}', cmdname))

      async def _insufficient_permissions(
        *,
        cmdname: str,
        event: hikari.MessageCreateEvent,
        permissions_int: int | None = None,
      ):
        """User does not have sufficient permissions to complete that action."""
        if permissions_int:
          await event.message.respond(
            random(pool.insufficient_permissions_specified)
            .replace('{cmd}', cmdname)
            .replace('{permissions}', perms.to_str(permissions_int))
          )
        else:
          await event.message.respond(
            random(pool.insufficient_permissions).replace('{cmd}', cmdname)
          )

      # also do one for permissions later @ {Null: func}

    if True:  # \/ # CommandsT
      if True:  # \/ # Dev / Debug

        async def r_debug(*, event: hikari.MessageCreateEvent): ...

      if True:  # \/ # Hidden

        async def r_pray(
          *,
          args: str,
          event: hikari.MessageCreateEvent,
          **kwargs,
        ):
          await event.message.add_reaction(hikari.UnicodeEmoji('🙏'))

      if True:  # \/ # 💎 Fun
        ...

      if True:  # \/ # 🖼 Images
        ...

      if True:  # \/ # 📚 Information

        async def r_help(event: hikari.MessageCreateEvent, guild_id: int):
          if guild_id:  # Guild Help
            await event.message.respond(EMBEDS.r_help(is_guild=True))
          else:  # DM Help
            await event.message.respond(EMBEDS.r_help(is_guild=False))

      if True:  # \/ # 🎲 Random

        async def r_8ball(event: hikari.MessageCreateEvent):
          text = random(pool.eight_ball['responses'])
          edit = False
          if text.startswith('*'):
            text = text.removeprefix('*')
            edit = True
          text = f'🎱 {text}'

          message = await event.message.respond(text)

          if not edit:
            return

          await asyncio.sleep(rng.randint(5, 15))

          await message.edit(content=f'🎱 {random(pool.eight_ball["edits"])}')

      if True:  # \/ # 🛠 Tools

        async def r_execute(
          *,
          args: str,
          event: hikari.MessageCreateEvent,
          **kwargs,
        ):
          await execute(args, event=event, responder=event.message.respond)

      if True:  # \/ # 🔧 Server
        ...

      if True:  # \/ # ⚙ Settings

        async def r_prefix(
          *,
          args: str,
          event: hikari.MessageCreateEvent,
          **kwargs,
        ):
          await event.message.respond('not implemented')

      if True:  # \/ # ⚠ Moderation
        ...

    # fmt: off

    command_categories: dict[Any, types.CommandCategoryType] = {
      CAT.FUN:         {'name': 'Fun',         'emoji': '💎'},
      CAT.IMAGES:      {'name': 'Images',      'emoji': '🖼'},
      CAT.INFORMATION: {'name': 'Information', 'emoji': '📚'},
      CAT.RANDOM:      {'name': 'Random',      'emoji': '🎲'},
      CAT.TOOLS:       {'name': 'Tools',       'emoji': '🛠'},
      CAT.SERVER:      {'name': 'Server',      'emoji': '🔧'},
      CAT.SETTINGS:    {'name': 'Settings',    'emoji': '⚙'},
      CAT.MODERATION:  {'name': 'Moderation',  'emoji': '⚠'},
    }

    command_category_order = [
      CAT.FUN,
      CAT.IMAGES,
      CAT.INFORMATION,
      CAT.RANDOM,
      CAT.TOOLS,
      CAT.SERVER,
      CAT.SETTINGS,
      CAT.MODERATION,
    ]

    if set(command_category_order) != set(command_categories.keys()):
      msg = 'set(command_category_order) != set(command_categories.keys())'
      raise ValueError(msg)

    commands = {
        # Dev / Debug
        'debug': {'function': r_debug, 'flags': CTF.HIDDEN | CTF.DEV},

        # Hidden
        'pray': {'function': r_pray, 'flags': CTF.HIDDEN},

        # 💎 Fun

        # 🖼 Images

        # 📚 Information
        'help': {'function': r_help, 'category': CAT.INFORMATION},

        # 🎲 Random
        '8ball': {'function': r_8ball, 'category': CAT.RANDOM},

        # 🛠 Tools
        'execute': {'function': r_execute, 'category': CAT.TOOLS},

        # 🔧 Server

        # ⚙ Settings
        'prefix': {'function': r_prefix, 'category': CAT.SETTINGS, 'flags': CTF.GUILD_ONLY},

        # ⚠ Moderation

        # Special
        None:  {'function': _unknown_command,          'category': CAT.NONE, 'flags': CTF.HIDDEN},  # The specified command does not exist in `commands`.
        False: {'function': _not_in_guild,             'category': CAT.NONE, 'flags': CTF.HIDDEN},  # You are not allowed to use that command in a guild.
        True:  {'function': _not_in_dms,               'category': CAT.NONE, 'flags': CTF.HIDDEN},  # You are not allowed to use that command in DMs.
        Null:  {'function': _insufficient_permissions, 'category': CAT.NONE, 'flags': CTF.HIDDEN},  # You don't have enough permissions to use that command.
      }
    # fmt: on

    default_command_dict: types.CommandsLookup = {
      'function': partial(kon.error, 'Command with undefined callable was invoked!'),
      'category': CAT.NONE,
      'flags': CTF.NONE,
    }

    for command_name, command_dict in commands.items():
      commands[command_name] = tcr.merge_dicts(
        command_dict,
        default_command_dict,
        recursive=False,
        strict=True,
      )

if True:  # \/ # Utilities
  if True:  # \/ # Synchronous

    def F(item: str) -> str:
      return eval(f'f{item!r}')

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

    def get_author_from_event(event: hikari.Event) -> hikari.Member | hikari.User:
      """Try to return an author or member from an event."""
      try:
        return event.author
      except AttributeError:
        try:
          return event.member
        except AttributeError:
          return event.old_member

  if True:  # \/ # ASSynchronous

    async def send_debug(
      channel_id_or_responder: int | str | Callable,
      text_or_dictmessage: list | str | types.DictMessage,
      *,
      as_dictmessage=False,
    ) -> hikari.Message:
      def debug_prepare(content: str | int | Iterable) -> str:
        if isinstance(content, str):  # String
          return codeblock(
            tcr.cut_at(
              f'{content!r}',
              n=DiscordLimits.Message.LENGTH_SAFE,
            ),
            langcode='py',
          )
        elif isinstance(content, Iterable):  # Iterable
          return codeblock(
            tcr.cut_at(
              tcr.print_iterable(content, raw=True),
              n=DiscordLimits.Message.LENGTH_SAFE,
            ),
            langcode='py',
          )
        else:  # Other
          return codeblock(
            tcr.cut_at(
              repr(content),
              n=DiscordLimits.Message.LENGTH_SAFE,
            ),
          )

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

    async def send_error(
      e: Exception,
      channel_id_or_responder: int | str | Callable = S.Channels.STDERR[testintbool()],
      traceback: str | None = None,
      tb_langcode: str = 'py',
      **embed_kwargs,
    ) -> hikari.Message:
      embed = EMBEDS.generic_error(e, traceback, tb_langcode=tb_langcode, **embed_kwargs)

      if isinstance(channel_id_or_responder, int | str):
        return await bot.rest.create_message(int(channel_id_or_responder), embed)
      else:
        return await channel_id_or_responder(embed)

    async def send_user_error(
      responder_or_channel_id: Callable | int | str,
      text='error',
      extra_info=None,
    ):
      text = f'**{text.title()}!**'
      if extra_info:
        text += f' ({extra_info})'
      if isinstance(responder_or_channel_id, str):
        responder_or_channel_id = int(responder_or_channel_id)
      if isinstance(responder_or_channel_id, int):
        await bot.rest.create_message(responder_or_channel_id, text)
      await responder_or_channel_id(text)

  if True:  # \/ # Embeds

    class Embeds:
      def generic_error(
        self, e: Exception, traceback: str | None = None, tb_langcode: str = 'py', **embed_kwargs
      ):
        extracted = tcr.extract_error(e, raw=True)
        desc = extracted[1] or A.UNSET_VALUE

        if desc.startswith('codeblock!'):
          desc = codeblock(
            desc.removeprefix('codeblock!'),
            langcode=tb_langcode,
            max_length=DiscordLimits.Embed.DESCRIPTION - 50,
          )

        em = embed(
          extracted[0] or 'Unknown exception',
          desc,
          color=S.Color.ERROR,
          **embed_kwargs,
        )

        if traceback:
          em.add_field(
            'Traceback',
            codeblock(
              traceback,
              langcode=tb_langcode,
              max_length=DiscordLimits.Embed.Fields.DESCRIPTION - 50,
            ),
          )

        return em

      # Rs
      def r_help(self, *, is_guild: bool):  # Non-specific help
        if is_guild:  # In Guild
          rendered = '\n\n'.join(
            [
              f"{command_categories[cat]['emoji']} **{command_categories[cat]['name']}** - "
              + ', '.join(
                sorted(
                  [
                    f'`{command_name}`'
                    for command_name, command_value in commands.items()
                    if command_value['category'] == cat
                    and isinstance(command_name, str)
                    and not (command_value['flags'] & (CTF.DM_ONLY | CTF.HIDDEN))
                  ]
                )
              )
              for cat in command_category_order
            ]
          )
        else:  # In DMs
          rendered = ', '.join(
            [
              f'`{command_name}`'
              for command_name, command_value in commands.items()
              if not (command_value['flags'] & (CTF.GUILD_ONLY | CTF.HIDDEN))
            ]
          )

        desc = """
**Type `r!help [command]` for information on a command.**

{{}}

===
**RoboTop was shut down on August 12 2023.** This is only a recreation
===
"""[1:-1]
        footer = f"""
v2.{get_version()}, updated {NotImplemented} days ago. Currently in {tcr.commafy(GUILD_COUNT)} servers.
Bot originally created by twitter.com/TheRealGDColon.
"""[1:-1]

        return embed(
          Null,
          desc.replace('{{}}', rendered),
          footer=footer,
          author={
            'name': 'Command List' if is_guild else 'DM Commands',
            'icon': bot.get_me().avatar_url or 'https://gdcolon.com/assets/colon.png',
          },
          color=S.Color.MAIN,
        )

      def r_help_specific(self, command: str) -> hikari.Embed | str:
        if command not in [k for k, v in commands.items() if not (v['flags'] & (CTF.HIDDEN))]:
          return 'No help found'
        elif command in A.HELP_DOCS:
          cmd_template = A.HELP_DOCS[command]
          if isinstance(cmd_template, dict):
            return embed(**cmd_template)
          elif isinstance(cmd_template, str):
            return cmd_template
          else:
            raise ValueError(f'Unknown help doc type: {type(cmd_template)}')

    EMBEDS = Embeds()

if True:  # \/ # Message related

  def parse_message_event(
    event: hikari.GuildMessageCreateEvent,
    guild_id: int | str | None = None,
  ) -> types.ParsedMessageEvent:
    """### Return a types.ParsedMessageEvent dict based on the received event.

    ```py
    return {
      "prefix":  str,  # The guild-specific or default prefix of that guild/DM
      "message": str,  # The message part of the event.content (without prefix if it was present!!)
      "prefixed": bool # Whether the prefix was found at the start of the message
    }
    ```
    """
    prefix = get_prefix(guild_id)
    prefixed = (event.content or '').startswith(prefix)
    message = (event.content or '').removeprefix(prefix)
    return {
      'prefix': prefix,
      'message': message,
      'prefixed': prefixed,
    }


if True:  # \/ # Event listeners
  if True:  # \/ # Messages

    async def on_message(
      event: hikari.GuildMessageCreateEvent | hikari.DMMessageCreateEvent,
      *,
      guild_id: int | None,
    ) -> None:
      if not event.is_human:
        return

      parsed = parse_message_event(event, guild_id)

      if not parsed['prefixed']:
        return

      splitted = parsed['message'].split(' ', maxsplit=1)
      cmdname, args = splitted if len(splitted) == 2 else [splitted[0], '']

      cmd: types.CommandsLookup = commands.get(cmdname)

      if cmd is not None:
        if guild_id:
          if cmd['flags'] & CTF.DM_ONLY:
            func = commands[True]['function']
            await run_sac(func, cmdname=cmdname, event=event)
            return
        else:
          if cmd['flags'] & CTF.GUILD_ONLY:
            func = commands[False]['function']
            await run_sac(func, cmdname=cmdname, event=event)
            return

        if (cmd['flags'] & CTF.DEV) and (event.author_id not in S.DEV_IDS):
          await run_sac(commands[None]['function'], cmdname=cmdname, event=event)
          return
      else:  # cmd is None
        await run_sac(commands[None]['function'], cmdname=cmdname, event=event)
        return

      payload = {
        'cmd': cmdname,
        'args': args,
        'event': event,
        'prefix': parsed['prefix'],
        'guild_id': guild_id,
      }

      excepted = False
      try:
        result = await run_sac(cmd['function'], **accept_args(cmd['function'], payload))
      except Exception as e:
        excepted = True
        result = e

      if result not in [None, 0]:
        match result:
          case (2, permission_int):
            await commands[Null]['function'](
              cmdname=cmdname, event=event, permission_int=permission_int
            )
          case 2:
            await commands[Null]['function'](cmdname=cmdname, event=event)
          case errcode:
            kon.error('`errcode`:', errcode)
            await send_user_error(event.message.respond)
            await send_error(
              InternalError(
                'codeblock!'
                + tcr.print_iterable(
                  {
                    'errcode': errcode,
                    'guild_id': guild_id,
                    'channel_id': event.channel_id,
                    'author_id': event.author_id,
                    'author_name': event.author.username
                    + ('' if str(a := event.author.discriminator) == '0' else f'#{a}'),
                  },
                  raw='both',
                  syntax_highlighting=True,
                )
              ),
              traceback=tcr.extract_traceback(result) if excepted else None,
              tb_langcode='ansi',
            )
            if testmode():
              raise result

    @bot.listen(hikari.GuildMessageCreateEvent)
    async def on_GuildMessageCreateEvent(event: hikari.GuildMessageCreateEvent):
      await on_message(event, guild_id=event.guild_id)

    @bot.listen(hikari.DMMessageCreateEvent)
    async def on_DMMessageCreateEvent(event: hikari.DMMessageCreateEvent):
      await on_message(event, guild_id=None)

  if True:  # \/ # Globals

    @bot.listen(hikari.StartingEvent)
    async def on_StartingEvent(event: hikari.StartingEvent): ...

    @bot.listen(hikari.StartedEvent)
    async def on_StartedEvent(event: hikari.StartedEvent):
      global GUILD_COUNT
      GUILD_COUNT = await get_guild_count(bot)

    @bot.listen(hikari.StoppingEvent)
    async def on_StoppingEvent(event: hikari.StoppingEvent): ...

    @bot.listen(hikari.StoppedEvent)
    async def on_StoppedEvent(event: hikari.StoppedEvent): ...


if True:  # \/ # Run
  if S.BANNER:
    print(S.BANNER)

  if testmode():
    text = ''.join(
      [
        f'{c("RED", "Black") if i % 2 == 0 else c("YELLOW", "white")}{x}'
        for i, x in enumerate(f' Running in testmode ')
      ]
    ) + c('reset')
    kon.log(text)

  bot.run(status=STATUS, activity=ACTIVITY)
