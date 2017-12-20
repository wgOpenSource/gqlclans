import graphene

from gqlclans.contrib.node_manager import manager
from gqlclans.server_info.dtos import IServerInfo
from gqlclans.server_info.logic import get_servers_info


class RootResolvers(object):
    @manager.to_gql_type
    def resolve_servers(self, info, limit):
        return get_servers_info()['data']['wot'][:limit]


class ServerInfo(graphene.ObjectType):
    class Meta:
        interfaces = (IServerInfo, )
