from functools import partial

import requests
from graphene import List, ID, Schema, ObjectType, String
from graphql import Source, parse, execute
from mock import patch, Mock
from stringcase import snakecase


DATA_RANGE = range(100)


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


def create_fake_response(url):
    if 'accounts' in url:
        return FakeResponse([{
            'account_id': account_id,
            'name': f'Account-{account_id}',
        } for account_id in DATA_RANGE])

    return FakeResponse({
        clan_id: {
            'clan_id': clan_id,
            'name': f'Clan-{clan_id}'
        } for clan_id in DATA_RANGE
    })


@patch('requests.get', Mock(side_effect=create_fake_response))
def test_complex_request_graphql_benchmark(benchmark):
    class Account(ObjectType):
        account_id = ID()
        name = String()

    class Clan(ObjectType):
        clan_id = ID()
        name = String()
        accounts = List(Account)

        def resolve_accounts(self, info):
            return map(lambda data: Account(**data), requests.get('http://testserver/accounts').json())

    class Query(ObjectType):
        clans = List(Clan)

        def resolve_clans(self, info):
            return map(lambda data: Clan(**data), requests.get('http://testserver/clans').json().values())

    hello_schema = Schema(Query)
    source = Source('{ clans { clanId name accounts { accountId name } } }')
    query_ast = parse(source)

    big_query = partial(execute, hello_schema, query_ast)
    result = benchmark(big_query)
    expected_data = [{
        'clanId': str(clan_id),
        'name': f'Clan-{clan_id}',
        'accounts': [{
            'accountId': str(account_id),
            'name': f'Account-{account_id}',
        } for account_id in DATA_RANGE]
    } for clan_id in DATA_RANGE]

    assert not result.errors
    assert result.data == {'clans': expected_data}


@patch('requests.get', Mock(side_effect=create_fake_response))
def test_complex_request_benchmark(benchmark):
    def get_accounts(fields):
        data = requests.get('http://testserver/accounts').json()
        return list(map(lambda account: {field: str(account[snakecase(field)]) for field in fields}, data))

    def get_clans(clan_fields, account_fields):
        data = requests.get('http://testserver/clans').json().values()
        clans = list(map(lambda clan: {field: str(clan[snakecase(field)]) for field in clan_fields}, data))
        for clan in clans:
            clan['accounts'] = get_accounts(account_fields)
        return clans

    def get_data(clan_fields, account_fields):
        return {
            'clans': get_clans(clan_fields, account_fields),
        }

    clan_fields = ['clanId', 'name']
    account_fields = ['accountId', 'name']
    big_request = partial(get_data, clan_fields, account_fields)
    result = benchmark(big_request)
    expected_data = [{
        'clanId': str(clan_id),
        'name': f'Clan-{clan_id}',
        'accounts': [{
            'accountId': str(account_id),
            'name': f'Account-{account_id}',
        } for account_id in DATA_RANGE]
    } for clan_id in DATA_RANGE]

    assert result == {'clans': expected_data}
