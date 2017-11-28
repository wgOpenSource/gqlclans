from aiohttp_utils import run

from gqlclans.app import app


if __name__ == '__main__':
    run(app, app_uri='gqlclans.app:app', port=8567, reload=True)
