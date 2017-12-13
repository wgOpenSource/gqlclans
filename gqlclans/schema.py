import graphene

from gqlclans.clan.models import Clan
from gqlclans.message.mutations import AddMessage
from gqlclans.clan.resolvers import resolve_clan, resolve_search
from gqlclans.server_info.models import ServerInfo
from gqlclans.server_info.resolvers import resolve_server_info


class Mutation(graphene.ObjectType):
    add_message = AddMessage.Field()


class Query(graphene.ObjectType):
    clans = graphene.Field(graphene.List(Clan), clan_id=graphene.String(default_value='20226'), resolver=resolve_clan)
    search = graphene.Field(graphene.List(Clan), search_txt=graphene.String(default_value=''), resolver=resolve_search)
    servers = graphene.Field(graphene.List(ServerInfo), limit=graphene.Int(default_value=10), resolver=resolve_server_info)


schema = graphene.Schema(query=Query, mutation=Mutation)
