from gqlclans.clan.models import Clan
from gqlclans.message.models import Message
from gqlclans.logic import get_messages


def clan_from_data(data):
    return Clan(
        name=data['name'],
        tag=data['tag'],
        clan_id=data['clan_id'],
        color=data['color'],
        members=data['members'],
        messages=map(lambda body: Message(body=body), get_messages(data['clan_id'])),
    )


def parse_clans_data(data):
    return [clan_from_data(content) for content in data.values()]
