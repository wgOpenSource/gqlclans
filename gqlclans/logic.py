from collections import defaultdict

import urllib.parse

import requests

import settings

CLAN_INFO = '/wgn/clans/info/?game=wot&clan_id={}'
ACCOUNT_INFO = '/wot/account/info/?account_id={}'
SEARCH_CLAN = '/wgn/clans/list/?fields=clan_id&game=wot&search={}'
SERVERS_INFO = '/wgn/servers/info/?game=wot'


__all__ = (
    'get_clan_info',
    'search_clan',
    'get_servers_info',
    'save_message',
    'get_messages',
)


def build_url(path):
    url = urllib.parse.urljoin(settings.WGAPI_BASE_URL, path)
    url_parts = list(urllib.parse.urlparse(url))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update({'application_id': settings.WGAPI_APPLICATION_ID})
    url_parts[4] = urllib.parse.urlencode(query)
    return urllib.parse.urlunparse(url_parts)


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
    return papi_request.session.get(build_url(CLAN_INFO.format(clan_id))).json()


def get_account_info(account_id):
    papi_request = PapiRequestSession()
    return papi_request.session.get(build_url(ACCOUNT_INFO.format(account_id))).json()


def search_clan(search):
    papi_request = PapiRequestSession()
    return papi_request.session.get(build_url(SEARCH_CLAN.format(search))).json()


def get_servers_info():
    papi_request = PapiRequestSession()
    return papi_request.session.get(build_url(SERVERS_INFO)).json()


def save_message(clan_id, message):
    papi_request = PapiRequestSession()
    papi_request.store[str(clan_id)].append(message)


def get_messages(clan_id):
    papi_request = PapiRequestSession()
    return papi_request.store[str(clan_id)]
