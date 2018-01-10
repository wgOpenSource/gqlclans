from collections import defaultdict

import requests


CLAN_INFO = 'https://api.worldoftanks.ru/wgn/clans/info/?application_id=8c2d3111d4e93eaa2a6e008424123d6d&game=wot&clan_id={}'
ACCOUNT_INFO = 'https://api.worldoftanks.ru/wot/account/info/?application_id=8c2d3111d4e93eaa2a6e008424123d6d&account_id={}'
SEARCH_CLAN = 'https://api.worldoftanks.ru/wgn/clans/list/?application_id=8c2d3111d4e93eaa2a6e008424123d6d&fields=clan_id&game=wot&search={}'
SERVERS_INFO = 'https://api.worldoftanks.ru/wgn/servers/info/?application_id=8c2d3111d4e93eaa2a6e008424123d6d&game=wot'


__all__ = (
    'get_clan_info',
    'search_clan',
    'get_servers_info',
    'save_message',
    'get_messages',
)


class PapiRequestSession:
    session = None
    adapters = {}
    store = defaultdict(list)

    def __init__(self):
        self.session = requests.Session()
        for url, adapter in PapiRequestSession.adapters.items():
            self.session.mount(url, adapter)


def get_clan_info(clan_id):
    papi_request = PapiRequestSession()
    return papi_request.session.get(CLAN_INFO.format(clan_id)).json()


def get_account_info(account_id):
    papi_request = PapiRequestSession()
    return papi_request.session.get(ACCOUNT_INFO.format(account_id)).json()


def search_clan(search):
    papi_request = PapiRequestSession()
    return papi_request.session.get(SEARCH_CLAN.format(search)).json()


def get_servers_info():
    papi_request = PapiRequestSession()
    return papi_request.session.get(SERVERS_INFO).json()


def save_message(clan_id, message):
    papi_request = PapiRequestSession()
    papi_request.store[str(clan_id)].append(message)


def get_messages(clan_id):
    papi_request = PapiRequestSession()
    return papi_request.store[str(clan_id)]
