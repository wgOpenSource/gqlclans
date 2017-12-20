import graphene

from gqlclans.clans.dtos import IClansRoot
from gqlclans.clans.mutations import AddMessage
from gqlclans.clans.resolvers import RootResolver as ClansResolvers
from gqlclans.contrib.node_manager import manager
from gqlclans.server_info.dtos import IServersRoot
from gqlclans.server_info.resolvers import RootResolvers as ServersResolvers


class Roots(ClansResolvers, ServersResolvers, graphene.ObjectType):
    class Meta:
        interfaces = (IClansRoot, IServersRoot, )


class Mutation(graphene.ObjectType):
    add_message = AddMessage.Field()


schema = graphene.Schema(query=Roots, types=manager.types(), mutation=Mutation)
