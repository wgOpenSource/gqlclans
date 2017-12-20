import graphene


class IServersRoot(graphene.Interface):
    servers = graphene.Field(graphene.List(lambda: IServerInfo), limit=graphene.Int(default_value=10))


class IServerInfo(graphene.Interface):
    players_online = graphene.Int()
    server = graphene.String()
