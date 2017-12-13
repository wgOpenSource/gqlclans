import graphene


class ServerInfo(graphene.ObjectType):
    players_online = graphene.Int()
    server = graphene.String()
