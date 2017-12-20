import graphene


class IClansRoot(graphene.Interface):
    clans = graphene.Field(graphene.List(lambda: IClan), clan_id=graphene.String(default_value='20226'))
    search = graphene.Field(graphene.List(lambda: IClan), search_txt=graphene.String(default_value=''))


class IMember(graphene.Interface):
    name = graphene.String()
    account_id = graphene.ID()
    role = graphene.String()
    clan_id = graphene.String()
    clan = graphene.Field(lambda: IClan)


class IMessage(graphene.Interface):
    body = graphene.String()


class IClan(graphene.Interface):
    name = graphene.String()
    tag = graphene.String()
    clan_id = graphene.ID()
    color = graphene.String()
    members = graphene.Field(graphene.List(lambda: IMember))
    messages = graphene.Field(graphene.List(lambda: IMessage))


class IAddMessage(graphene.Interface):

    success = graphene.Boolean()
    message = graphene.Field(lambda: IMessage)
