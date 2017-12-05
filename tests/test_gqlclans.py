
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


def test_get_messages_after_mutation():
    mutation = '''
        mutation TestSaveMessage {
            addMessage(body: "Text", clanId: "10164"){
                success
            }
        }
    '''
    query = '''
        query TestQuery {
            clans(clanId: "10164") {
                messages {
                    body
                }
            }
        }
    '''
    client = Client(schema)
    mutation_result = client.execute(mutation)
    result = client.execute(query)

    assert mutation_result == {
        'data': {
            'addMessage': {
                'success': True
            }
        }
    }
    assert result == {
        'data': {
            'clans': [
                {'messages': [{ 'body': 'Text' }]}
            ]
        }
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
