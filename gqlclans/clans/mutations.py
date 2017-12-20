import graphene

from gqlclans.clans.dtos import IAddMessage
from gqlclans.clans.logic import save_message
from gqlclans.contrib.node_manager import manager


class AddMessage(graphene.Mutation):
    class Arguments:
        body = graphene.String()
        clan_id = graphene.ID()

    class Meta:
        interfaces = (IAddMessage, )

    def mutate(self, info, body, clan_id):
        save_message(clan_id, body)
        success = True
        return AddMessage(message=body, success=success)

    @manager.to_gql_type
    def resolve_message(self, info):
        return {'body': self.message}
