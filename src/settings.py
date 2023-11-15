import os
from enum import Enum

DEV_IDS = (507642999992352779,)

DEFAULT_ENABLED_GUILDS = ()  # Leave as empty tuple for slash commands to show up everywhere

TESTMODE = os.name == 'nt'  # Use TOKEN2 if on windows, else use TOKEN
