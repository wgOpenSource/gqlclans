import graphene
from promise import Promise
from promise.dataloader import DataLoader

from gqlclans import logic


class ClanLoader(DataLoader):
    def batch_load_fn(self, ids):
        return Promise.resolve([logic.get_clan_info(id) for id in ids])


class AccountLoader(DataLoader):
    def batch_load_fn(self, ids):
        return Promise.resolve([logic.get_account_info(id) for id in ids])


clan_loader = ClanLoader()
account_loader = AccountLoader()


class ServerInfo(graphene.ObjectType):
    players_online = graphene.Int()
    server = graphene.String()


class Member(graphene.ObjectType):
    name = graphene.String()
    account_id = graphene.ID()
    role = graphene.String()
    clan_id = graphene.String()
    clan = graphene.Field(lambda: Clan)

    def resolve_clan(self, info):
        return clan_loader.load(self.clan_id).then(lambda data: clan_from_data(data['data'][str(self.clan_id)]))


class Message(graphene.ObjectType):
    body = graphene.String()


class AddMessage(graphene.Mutation):
    class Arguments:
        body = graphene.String()
        clan_id = graphene.ID()

    success = graphene.Boolean()
    message = graphene.Field(lambda: Message)

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

    def resolve_members(self, info):
        return map(lambda member: Member(
            name=member['account_name'],
            account_id=member['account_id'],
            role=member['role'],
            clan_id=self.clan_id,
        ), self.members)


class Mutation(graphene.ObjectType):
    add_message = AddMessage.Field()


class Account(graphene.ObjectType):
    account_id = graphene.ID()
    created_at = graphene.Int()
    games = graphene.List(graphene.String)
    nickname = graphene.String()


class Query(graphene.ObjectType):
    clans = graphene.Field(graphene.List(Clan), clan_id=graphene.String(default_value='20226'))
    search_clans = graphene.Field(graphene.List(Clan), search=graphene.String(default_value=''))
    servers = graphene.Field(graphene.List(ServerInfo), limit=graphene.Int(default_value=10))
    search_accounts = graphene.Field(graphene.List(Account), search=graphene.String())

    def resolve_servers(self, info, limit):
        result = logic.get_servers_info()['data']['wot'][:limit]
        return map(lambda server: ServerInfo(
            players_online=server['players_online'],
            server=server['server'],
        ), result)

    def resolve_clans(self, info, clan_id):
        data = logic.get_clan_info(clan_id)['data']
        return parse_clans_data(data)

    def resolve_search(self, info, search):
        result = logic.search_clan(search)['data']
        clan_ids = list(map(lambda clan: clan['clan_id'], result))
        clan_ids = ','.join(map(str, clan_ids))
        data = logic.get_clan_info(clan_ids)['data']
        return parse_clans_data(data)

    def resolve_accounts(self, info, search):
        accounts_data = logic.search_accounts(search)['data']
        return [Account(**account_data) for account_data in accounts_data]


def clan_from_data(data):
    return Clan(
        name=data['name'],
        tag=data['tag'],
        clan_id=data['clan_id'],
        color=data['color'],
        members=data['members'],
        messages=map(lambda body: Message(body=body), logic.get_messages(data['clan_id'])),
    )


def parse_clans_data(data):
    return [clan_from_data(content) for content in data.values()]


schema = graphene.Schema(query=Query, mutation=Mutation)
