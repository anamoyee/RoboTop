if True:  # \/ # Imports
  import asyncio
  import inspect
  import math
  import os
  import pathlib as p
  import random as rng
  import shelve
  import sys
  import time
  from collections.abc import Callable, ItemsView, Iterable, KeysView, Mapping, ValuesView
  from functools import partial
  from random import choice as random
  from sys import exit as sexit
  from typing import Any, Literal, LiteralString, Unpack

  import hikari
  import lightbulb as lb
  import miru
  import tcrutils as tcr
  from lightbulb.ext import tasks
  from tcrutils import DiscordLimits, Null, c, codeblock, run_sac, uncodeblock
  from tcrutils import console as kon
  from tcrutils import float2int as float_or_int
  from tcrutils import float2int as int_or_float
  from tcrutils.discord import PERMISSIONS_DICT, embed
  from tcrutils.discord import permissions as perms

  import assets as A
  import defaults as default
  import pools as pool
  import settings as S  # ass
  import types_ as types
  from types_ import CAT, CTF


if True:  # \/ # Consts
  SRC_DIRECTORY = p.Path(__file__).parent
  ROOT_DIRECTORY = p.Path(SRC_DIRECTORY).parent
  TOKEN_FILE = p.Path(ROOT_DIRECTORY).parent / 'TOKEN.txt'
  TOKEN2_FILE = p.Path(ROOT_DIRECTORY).parent / 'TOKEN2.txt'

  TOKEN = TOKEN_FILE.read_text() if TOKEN_FILE.is_file() else None
  TOKEN2 = TOKEN2_FILE.read_text() if TOKEN2_FILE.is_file() else None

  STATUS = hikari.Status.DO_NOT_DISTURB
  ACTIVITY = hikari.Activity(
    name=('Clone of RoboTop' + ' - Testmode' if S.TESTMODE else ''),
    type=hikari.ActivityType.CUSTOM,
  )

  GUILD_COUNT: int = -1  # Gets set in on_StartedEvent()

if True:  # \/ # Banner sheit
  for k, v in S.BANNER[1].items():
    S.BANNER[0] = S.BANNER[0].replace(k, c('reset') + c(v))
  S.BANNER = S.BANNER[0] + c('reset')

if True:  # \/ # Execute structs
  _execute_user_mentions = set()
  _execute_role_mentions = set()
  _execute_embed = {}

if True:  # \/ # Sync functions

  def unix() -> int:
    """Return current unix timestamp (int)."""
    return math.floor(time.time())

  def get_version() -> int:
    """Return the current version as an int."""
    return S.VERSION

  def testmode():
    """Return a suffix for displays if in testmode, can be used in if statements."""
    return ' - Testmode' if S.TESTMODE else ''

  def testintbool():
    """Alias for bool(testmode())."""
    return tcr.intbool(testmode())

  def curly_filter(text, _key='𒐫𒐫𒐫𒐫𒐫') -> str:
    return text.replace('{', _key + '[').replace('}', _key + ']')

  def curly_unfilter(text, _key='𒐫𒐫𒐫𒐫𒐫') -> str:
    return text.replace(_key + '[', '{').replace(_key + ']', '}')

  def number_converter(*args, replace_with=0, negative_allowed=True):
    args = [str(x) for x in args]
    temp = []
    for arg in args:
      try:
        b = int(arg)
      except ValueError:
        try:
          b = float(arg)
        except ValueError:
          b = replace_with
      if b < 0 and not negative_allowed:
        b = replace_with
      temp.append(b)
    return type(args)(temp)

  def accept_args(func: Callable, kwargs: Mapping) -> Mapping:
    func_params = inspect.signature(func).parameters

    return {key: value for key, value in kwargs.items() if key in func_params}

if True:  # \/ # Async functions

  async def get_guild_count(bot: lb.BotApp):
    return len(await bot.rest.fetch_my_guilds())

if True:  # \/ # Errors

  class InternalError(Exception):
    """Something wrong happened internally."""

  class ParametersError(Exception):
    """Used when parse_command_parameters() wants to signify invalid parameters."""
