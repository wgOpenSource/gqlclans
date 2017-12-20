from gqlclans.contrib.session import PapiRequestSession

SERVERS_INFO = 'https://api.worldoftanks.ru/wgn/servers/info/?application_id=8c2d3111d4e93eaa2a6e008424123d6d&game=wot'


def get_servers_info():
    papi_request = PapiRequestSession()
    return papi_request.session.get(SERVERS_INFO).json()
