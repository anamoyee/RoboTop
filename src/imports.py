if True: # \/ # Imports
  import math
  import os
  import pathlib as p
  import shelve
  import sys
  import time
  from collections.abc import Callable, ItemsView, KeysView, Mapping, ValuesView
  from typing import Any

  import hikari
  import lightbulb
  import miru
  import tcrutils as tcr
  from tcrutils import console as kon

  import defaults as default
  import pools as pool
  import settings as S  # ass


if True: # \/ # Sync functions
  def unix():
    """Return current unix timestamp."""
    return math.floor(time.time())