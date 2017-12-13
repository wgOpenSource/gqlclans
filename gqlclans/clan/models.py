import graphene

from promise import Promise
from promise.dataloader import DataLoader

from gqlclans.logic import get_clan_info
from gqlclans.member.resolvers import resolve_members


class ClanLoader(DataLoader):
    def batch_load_fn(self, ids):
        return Promise.resolve([get_clan_info(id) for id in ids])


clan_loader = ClanLoader()


class Clan(graphene.ObjectType):
    name = graphene.String()
    tag = graphene.String()
    clan_id = graphene.ID()
    color = graphene.String()
    members = graphene.List('gqlclans.member.models.Member', resolver=resolve_members)
    messages = graphene.List('gqlclans.message.models.Message')
