#!/usr/bin/env python

from aiohttp import web

from gqlclans.app import app

if __name__ == '__main__':
    web.run_app(app, port=8567)
