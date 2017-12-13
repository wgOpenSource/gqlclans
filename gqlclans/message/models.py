import graphene


class Message(graphene.ObjectType):
    body = graphene.String()
