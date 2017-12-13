from gqlclans.logic import get_servers_info
from gqlclans.server_info.models import ServerInfo


def resolve_server_info(root, info, limit):
    result = get_servers_info()['data']['wot'][:limit]
    return map(lambda server: ServerInfo(
        players_online=server['players_online'],
        server=server['server'],
    ), result)
