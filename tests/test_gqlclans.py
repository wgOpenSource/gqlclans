
import json

from graphene.test import Client
from gqlclans.data_loaders import DataLoaders
from gqlclans.schema import schema
from gqlclans.app import app


def fake_clan_body(**kwargs):
    clan = {
        'clan_id': 12344,
        'name': 'Mocked Name',
        'tag': 'MCKD',
        'color': '000000',
        'accepts_join_requests': True,
        'created_at': 0,
        'creator_name': 'creator_name',
        'description': 'description',
        'description_html': '<p>description_html</p>',
        'emblems': {'x34': {'wot': 'http://example.com/x34.ipg'}},
        'game': 'wot',
        'is_clan_disbanded': False,
        'leader_name': 'leader_name',
        'members_count': 10,
        'motto': 'motto',
        'old_name': '',
        'old_tag': '',
        'renamed_at': 0,
        'updated_at': 0,
    }
    clan.update(kwargs)
    return clan


MOCKED_CLAN_INFO_RESPONSE = {
    'status': 'ok',
    'data': {
        '12344': fake_clan_body(members=[{
                'account_name': f'Account-{i}',
                'account_id': i,
                'role': 'private',
            } for i in range(5)])
    }
}

MOCKED_CLAN_SEARCH_RESPONSE = {
    'status': 'ok',
    'data': [
        fake_clan_body(name='Mocked Name', tag='MCKD 12344'),
        fake_clan_body(
            clan_id=10000,
            name='Mocked Name 10000',
            tag='MCKD 10000',
        ),
    ]
}

MOCKED_SERVERS_INFO_RESPONSE = {
    'status': 'ok',
    'data': {
        'wot': [{
            'players_online': i * 100,
            'server': f'RU{i}',
        } for i in range(8)]
    }
}


def test_clan(mocker):
    mocker.patch('gqlclans.logic.get_clan_info', return_value=MOCKED_CLAN_INFO_RESPONSE)
    query = '{ clans(clanId: "10164") { tag name }}'
    client = Client(schema)
    result = client.execute(query)
    assert result['data']['clans'] == [
        {
            'tag': 'MCKD',
            'name': 'Mocked Name',
        }
    ]


def test_servers(mocker):
    mocker.patch('gqlclans.logic.get_servers_info', return_value=MOCKED_SERVERS_INFO_RESPONSE)
    query = '{ servers(limit: 2) { server playersOnline }}'
    client = Client(schema)
    result = client.execute(query)
    assert result['data']['servers'] == [
        {
            'playersOnline': 0,
            'server': 'RU0',
        },
        {
            'playersOnline': 100,
            'server': 'RU1',
        }
    ]


def test_search(mocker):
    mocker.patch('gqlclans.logic.search_clan', return_value={
        'data': [{'clan_id': '12345'}, {'clan_id': '10000'}]
    })
    mocker.patch('gqlclans.logic.get_clan_info', return_value={
        'data': {
            '12345': fake_clan_body(name='Mocked Name 12344', tag='MCKD 12344', clan_id=12345, members=[]),
            '10000': fake_clan_body(name='Mocked Name 10000', tag='MCKD 10000', members=[], clan_id=10000,),
        }
    })
    query = '{ searchClans(search: "BOUHA") { tag name }}'
    client = Client(schema)
    result = client.execute(query)
    assert result['data']['searchClans'] == [
        {
            'tag': 'MCKD 12344',
            'name': 'Mocked Name 12344',
        },
        {
            'tag': 'MCKD 10000',
            'name': 'Mocked Name 10000',
        },
    ]


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
    mocked_clan_info = mocker.patch('gqlclans.logic.get_clan_info', return_value=MOCKED_CLAN_INFO_RESPONSE)
    query = '''{
        clans(clanId: "12344") {
            members {
                clan {
                    clanId
                }
            }
        }
    }
    '''

    client = Client(schema)
    result = client.execute(query, context_value={'data_loaders': DataLoaders})
    assert mocked_clan_info.call_count == 2
    assert result['data']['clans'] == [{
        'members': [{
            'clan': {
                'clanId': '12344',
            }
        } for _ in range(5)]
    }]


async def test_app(test_client, mocker):
    mocker.patch('gqlclans.logic.get_clan_info', return_value=MOCKED_CLAN_INFO_RESPONSE)

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
            'clans': [{'tag': 'MCKD', 'name': 'Mocked Name'}]
        }
    }
