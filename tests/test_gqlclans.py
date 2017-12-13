
import json

from graphene.test import Client
from gqlclans.schema import schema
from gqlclans.app import app


def test_clan():
    query = '{ clans(clanId: "10164") { tag name }}'
    client = Client(schema)
    result = client.execute(query)
    assert result == {
        'data': {
            'clans': [
                {
                    'tag': 'BOUHA',
                    'name': 'Второй  всадник  апокалипсиса',
                }
            ]
        }
    }


def test_servers():
    query = '{ servers(limit: 2) { server playersOnline }}'
    client = Client(schema)
    result = client.execute(query)
    assert result == {
        'data': {
            'servers': [
                {
                    'playersOnline': 14583,
                    'server': 'RU8',
                },
                {
                    'playersOnline': 37041,
                    'server': 'RU7',
                }
            ]
        }
    }


def test_search():
    query = '{ search(searchTxt: "BOUHA") { tag name }}'
    client = Client(schema)
    result = client.execute(query)
    assert result == {
        'data': {
            'search': [
                {
                    'tag': 'BETH',
                    'name': 'BouHa',
                },
                {
                    'tag': 'BOUHA',
                    'name': 'Второй  всадник  апокалипсиса',
                },
            ]
        }
    }


def test_mutation():
    query = '''
        mutation TestTitle {
            addMessage(body: "Some text", clanId: "28"){
                message {
                    body
                }
                success
            }
        }
    '''
    client = Client(schema)
    result = client.execute(query)
    assert result == {
        'data': {
            'addMessage': {
                'message': {
                    'body': 'Some text',
                },
                'success': True
            }
        }
    }


def test_batch_loading_cache(mocker):
    query = '''{
        clans(clanId: "12344") {
            name
            members {
                clan {
                    clanId
                }
            }
        }
    }
    '''
    mocked_clan_info_response = {
        'data': {
            '12344': {
                'clan_id': 12344,
                'name': 'Mocked Name',
                'tag': 'MCKD',
                'color': '000000',
                'members': [{
                    'account_name': f'Account-{i}',
                    'account_id': i,
                    'role': 'private',
                } for i in range(5)]
            }
        }
    }
    mocker.patch('gqlclans.clan.resolvers.get_clan_info', return_value=mocked_clan_info_response)
    member_clan_info_mock = mocker.patch('gqlclans.clan.models.get_clan_info', return_value=mocked_clan_info_response)

    client = Client(schema)
    result = client.execute(query)
    assert len(member_clan_info_mock.mock_calls) == 1
    assert result == {
        'data': {
            'clans': [{
                'name': 'Mocked Name',
                'members': [{
                    'clan': {
                        'clanId': '12344',
                    }
                } for _ in range(5)]
            }]
        },
    }


async def test_app(test_client):
    client = await test_client(app)
    response = await client.get('/?query={clans{name tag}}')
    assert response.history[0].status == 307
    assert response.status == 200
    assert response.url.relative().human_repr() == '/graphiql?query={clans{name tag}}'

    response = await client.get('/graphql?query={ clans(clanId: "10164") { tag name }}')
    assert response.status == 200
    content = await response.content.read()
    assert json.loads(content) == {
        'data': {
            'clans': [{'tag': 'BOUHA', 'name': 'Второй  всадник  апокалипсиса'}]
        }
    }
