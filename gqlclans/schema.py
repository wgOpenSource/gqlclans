import graphene
from promise import Promise
from promise.dataloader import DataLoader
from stringcase import camelcase, snakecase

from gqlclans import logic
from gqlclans.utils import get_fields


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
    members = graphene.List(lambda: Account)
    messages = graphene.List(Message)

    @staticmethod
    def get_additional_info_requested_fields(requested_fields):
        clan_member_fields = list(map(camelcase, ('nickname', 'account_id', 'joined_at', 'role', 'role_i18n', 'clan',)))
        return {field for field in requested_fields if field not in clan_member_fields}

    @staticmethod
    def request_members_additional_info(accounts, fields):
        account_ids = map(lambda account: str(account['account_id']), accounts)
        account_promise = account_loader.load(','.join(account_ids)).then(lambda result: list(result['data'].values()))
        accounts_data = account_promise.get()
        for account in accounts:
            account.update({
                snakecase(field): accounts_data[snakecase(field)] for field in fields
            })

    def create_graphene_accounts(self, accounts_data, requested_fields):
        accounts = []
        for account in accounts_data:
            account_data = {
                'clan_id': self.clan_id,
                **{field: value for field, value in account.items() if camelcase(field) in requested_fields},
            }
            if 'nickname' in requested_fields:
                account_data.update({'nickname': account.get('account_name') or account.get('nickname')})
            accounts.append(Account(**account_data))

        return accounts

    def resolve_members(self, info):
        requested_fields = get_fields(info).keys()
        request_account_info_fields = self.get_additional_info_requested_fields(requested_fields)
        if request_account_info_fields:
            self.request_members_additional_info(self.members, request_account_info_fields)

        return self.create_graphene_accounts(self.members, requested_fields)


class Mutation(graphene.ObjectType):
    add_message = AddMessage.Field()


class Account(graphene.ObjectType):
    # Account info
    account_id = graphene.ID()
    clan_id = graphene.ID()
    client_language = graphene.String()
    created_at = graphene.Int()
    global_rating = graphene.Int()
    last_battle_time = graphene.Int()
    logout_at = graphene.Int()
    nickname = graphene.String()
    updated_at = graphene.Int()

    # Clan members info
    role = graphene.String()
    # Fields with numbers in names capitalize incorrectly, will be fixed in graphene 2.0.2
    # role_i18n = graphene.String()
    joined_at = graphene.Int()
    clan = graphene.Field(lambda: Clan)
    # Statistics is a complex structure
    # statistics = graphene.Field()

    def resolve_clan(self, info):
        if self.clan_id:
            return clan_loader.load(self.clan_id).then(lambda data: clan_from_data(data['data'][str(self.clan_id)]))
        return None


class Query(graphene.ObjectType):
    clans = graphene.Field(graphene.List(Clan), clan_id=graphene.String(default_value='20226'))
    search_clans = graphene.Field(graphene.List(Clan), search=graphene.String(default_value=''))
    servers = graphene.Field(graphene.List(ServerInfo), limit=graphene.Int(default_value=10))
    accounts = graphene.Field(graphene.List(Account), account_ids=graphene.List(graphene.String))

    def resolve_servers(self, info, limit):
        result = logic.get_servers_info()['data']['wot'][:limit]
        return map(lambda server: ServerInfo(
            players_online=server['players_online'],
            server=server['server'],
        ), result)

    def resolve_clans(self, info, clan_id):
        data = logic.get_clan_info(clan_id)['data']
        return parse_clans_data(data)

    def resolve_search_clans(self, info, search):
        result = logic.search_clan(search)['data']
        clan_ids = list(map(lambda clan: clan['clan_id'], result))
        clan_ids = ','.join(map(str, clan_ids))
        data = logic.get_clan_info(clan_ids)['data']
        return parse_clans_data(data)

    def resolve_accounts(self, info, account_ids):
        requested_fields = get_fields(info).keys()
        clan_specific_account_fields = list(map(camelcase, ('joined_at', 'role', 'role_i18n',)))
        request_clan_account_fields = [field for field in requested_fields if field in clan_specific_account_fields]

        accounts_promise = account_loader.load(','.join(account_ids)).then(lambda result: list(result['data'].values()))
        accounts_data = accounts_promise.get()

        if request_clan_account_fields:
            clan_ids = {str(account_data['clan_id']) for account_data in accounts_data if account_data.get('clan_id')}
            clans_data = None
            if clan_ids:
                clans_promise = clan_loader.load(','.join(clan_ids)).then(lambda result: result['data'])
                clans_data = clans_promise.get()
            for account in accounts_data:
                account_clan_data = None
                if account.get('clan_id'):
                    account_clan_data = [
                        member for member in clans_data[str(account['clan_id'])]['members'] if
                        member['account_id'] == account['account_id']
                    ][0]

                account_clans_data = {
                    snakecase(field): account_clan_data[snakecase(field)] if account_clan_data else None
                    for field in request_clan_account_fields
                }
                account.update(account_clans_data)

        return list(map(lambda data: Account(**{
            'clan_id': data['clan_id'],
            **{field: value for field, value in data.items() if camelcase(field) in requested_fields}
        }), accounts_data))


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