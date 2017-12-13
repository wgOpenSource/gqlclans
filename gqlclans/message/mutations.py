import graphene

from gqlclans.logic import save_message
from gqlclans.message.models import Message


class AddMessage(graphene.Mutation):
    class Arguments:
        body = graphene.String()
        clan_id = graphene.ID()

    success = graphene.Boolean()
    message = graphene.Field(lambda: Message)

    def mutate(self, info, body, clan_id):
        save_message(clan_id, body)
        message = Message(body=body)
        success = True
        return AddMessage(message=message, success=success)
