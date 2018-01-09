import sys


DEFAULT_CLAN_ID = '20226'

try:
    from settings_local import *
except ImportError:
    print('settings_local is not provided', file=sys.stderr)
