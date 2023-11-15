if True:  # \/ # Imports
  import math
  import os
  import pathlib as p
  import random as rng
  import shelve
  import sys
  import time
  from collections.abc import Callable, ItemsView, Iterable, KeysView, Mapping, ValuesView
  from functools import partial
  from sys import exit as sexit
  from typing import Any, Literal, LiteralString

  import hikari
  import lightbulb as lb
  import miru
  import tcrutils as tcr
  from lightbulb.ext import tasks
  from tcrutils import Null, c, run_sac
  from tcrutils import console as kon

  import defaults as default
  import pools as pool
  import settings as S  # ass
  import types_ as types


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

if True:  # \/ # Sync functions

  def unix():
    """Return current unix timestamp."""
    return math.floor(time.time())

  def token():
    """Return selected token."""
    a = TOKEN2 if S.TESTMODE else TOKEN
    if a is None:
      msg = (
        f"{tcr.c('Red')}Unknown token - check TOKEN{'2' if S.TESTMODE else ''}.txt{tcr.c('reset')}"
      )
      raise tcr.error.ConfigurationError(msg)
    return a.strip()

  def testmode():
    """Return a suffix for displays if in testmode, can be used in if statements."""
    return ' - Testmode' if S.TESTMODE else ''

  def curly_filter(text, _key='𒐫𒐫𒐫𒐫𒐫'):
    return text.replace('{', _key + '[').replace('}', _key + ']')

  def curly_unfilter(text, _key='𒐫𒐫𒐫𒐫𒐫'):
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

  def float_or_int(n: float) -> float | int:
    if round(n) == n:
      return int(n)
    return float(n)

  int_or_float = float_or_int

  def commafy_str_or_int(text: str | int, splitter: str = ','):
    text = str(text)
    temp = ''
    for i, letter in enumerate(text[::-1]):
      temp += letter
      if i % 3 == 2 and i != len(text) - 1:
        temp += splitter
    return temp[::-1]

  def codeblock(text: str, langcode='') -> str:
    return 3 * '`' + langcode + '\n' + text + 3 * '`'

  def uncodeblock(text: str) -> str:
    if text[-3:] == tcr.BACKTICKS and text[:3] == tcr.BACKTICKS:
      code_start = 3
      code_end = -3
      if '\n' in text[3:]:  # Check if there is a language code specified
        code_start = text.index('\n') + 1
      return text[code_start:code_end].strip()
    return text
