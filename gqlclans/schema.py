import graphene

from gqlclans import logic


class ServerInfo(graphene.ObjectType):
    players_online = graphene.Int()
    server = graphene.String()


class Member(graphene.ObjectType):
    name = graphene.String()
    account_id = graphene.ID()
    role = graphene.String()


class Message(graphene.ObjectType):
    body = graphene.String()


class AddMessage(graphene.Mutation):
    class Arguments:
        body = graphene.String()
        clan_id = graphene.ID()

    success = graphene.Boolean()
    message = graphene.Field(lambda: Message)# lambda is nice pattern for describe relation with not loaded yet classes

    def mutate(self, info, body, clan_id):
        logic.save_message(clan_id, body)
        message = Message(body=body)
        success = True
        return AddMessage(message=message, success=success)


class Clan(graphene.ObjectType):
    name = graphene.String()
    tag = graphene.String()
    clan_id = graphene.ID()
    color = graphene.String()
    members = graphene.List(Member)
    messages = graphene.List(Message)


class Mutation(graphene.ObjectType):
    add_message = AddMessage.Field()


class Query(graphene.ObjectType):
    clans = graphene.Field(graphene.List(Clan), clan_id=graphene.String(default_value='20226'))
    search = graphene.Field(graphene.List(Clan), search_txt=graphene.String(default_value=''))
    servers = graphene.Field(graphene.List(ServerInfo), limit=graphene.Int(default_value=10))

    def resolve_servers(self, info, limit):
        result = logic.get_servers_info()['data']['wot'][:limit]
        return map(lambda server: ServerInfo(
            players_online=server['players_online'],
            server=server['server'],
        ), result)

    def resolve_clans(context, info, clan_id):
        data = logic.get_clan_info(clan_id)['data']
        return parse_data(data)

    def resolve_search(context, info, search_txt):
        result = logic.search_clan(search_txt)['data']
        clan_ids = list(map(lambda clan: clan['clan_id'], result))
        clan_ids = ','.join(map(str, clan_ids))
        data = logic.get_clan_info(clan_ids)['data']
        return parse_data(data)


def parse_data(data):
    get_member = lambda member: Member(
        name=member['account_name'],
        account_id=member['account_id'],
        role=member['role']
    )
    clans = []
    for content in data.values():
        clans.append(
            Clan(
                name=content['name'],
                tag=content['tag'],
                clan_id=content['clan_id'],
                color=content['color'],
                members=map(get_member, content['members']),
                messages=map(lambda msg: Message(body=msg),
                             logic.get_messages(content['clan_id'])),  # TODO: just for test
            ))
    return clans


schema = graphene.Schema(query=Query, mutation=Mutation)
