import json

from aiohttp_utils import run

from gqlclans.app import app
from gqlclans.schema import schema


def write_schema():
    with open('schema.json', 'w') as fp:
        json.dump({'data': schema.introspect()}, fp)


if __name__ == '__main__':
    write_schema()
    run(app, app_uri='gqlclans.app:app', port=8567, reload=True)
