import sys


WGAPI_BASE_URL = 'https://api.worldoftanks.ru'

try:
    from settings_local import *
except ImportError:
    print('settings_local is not provided', file=sys.stderr)

