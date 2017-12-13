from gqlclans.clan.models import clan_loader
from gqlclans.clan.helpers import parse_clans_data, clan_from_data
from gqlclans.logic import get_clan_info, search_clan


def resolve_clan(root, info, clan_id):
    data = get_clan_info(clan_id)['data']
    return parse_clans_data(data)


def resolve_search(root, info, search_txt):
    result = search_clan(search_txt)['data']
    clan_ids = list(map(lambda clan: clan['clan_id'], result))
    clan_ids = ','.join(map(str, clan_ids))
    data = get_clan_info(clan_ids)['data']
    return parse_clans_data(data)


def resolve_member_clan(root, info):
    return clan_loader.load(root.clanId).then(lambda data: clan_from_data(data['data'][str(root.clanId)]))
