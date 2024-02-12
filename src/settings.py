import os

VERSION: int = 1  # 2.{VERSION}

# fmt: off
if True: # \/ # Dev config
  DEV_IDS: tuple[int] = (507642999992352779,)

if True: # \/ # General bot config
  DEFAULT_ENABLED_GUILDS = ()  # Leave as empty tuple for slash commands to show up everywhere

  TESTMODE = os.name == 'nt'  # Use TOKEN2 if on windows, else use TOKEN

  class Color:
    MAIN  = '#FF8000' # 'colon'
    ERROR = '#FF0000' # 'red'

class Channels: # (ProductionID, TestingID)
  STDOUT = (1174460589926522972, 1174459450543841300)
  STDERR = (1174460612739338270, 1174459490171629628)

if True: # \/ # Execute config
  EXECUTE_BRACKETS = ("{", "}")
  EXECUTE_SPLITTER = "|"

if True: # \/ # Host machine terminal config
  BANNER = [r"""
    $8888888b.
    $888   Y88b         888           %88888888888
    $888    888         888               %888
    $888   d88P .d88b.  88888b.   .d88b.  %888  .d88b.  88888b.
    $8888888P" d88""88b 888 "88b d88""88b %888 d88""88b 888 "88b
    $888 T88b  888  888 888  888 888  888 %888 888  888 888  888
    $888  T88b Y88..88P 888 d88P Y88..88P %888 Y88..88P 888 d88P
    $888   T88b "Y88P"  88888P"   "Y88P"  %888  "Y88P"  88888P"
    $%                                                  888
    $%                                                  888

  """[1:-1], {
    "$": "dark\\_gray",
    "%": "Orange\\_1",
    "!": "Purple\\_1A",
  }]

  # Generated using this website: https://patorjk.com/software/taag/#p=display&f=Colossal&t=RoboTop
