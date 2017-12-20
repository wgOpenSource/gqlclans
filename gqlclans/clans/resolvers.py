import graphene
from promise import Promise
from promise.dataloader import DataLoader

from gqlclans.contrib.node_manager import manager
from gqlclans.clans.dtos import (
    IMember,
    IClan,
    IMessage
)
from gqlclans.clans.logic import (
    get_messages,
    get_clan_info,
    search_clan,
)


class ClanLoader(DataLoader):
    def batch_load_fn(self, ids):
        return Promise.resolve([get_clan_info(id) for id in ids])


clan_loader = ClanLoader()


class RootResolver(object):
    def resolve_clans(self, info, clan_id):
        result_cls = manager.type_from_info(info)
        response_data = get_clan_info(clan_id)['data']
        return [
            result_cls.from_data(data)
            for data in response_data.values()
        ]

    def resolve_search(self, info, search_txt):
        result_cls = manager.type_from_info(info)
        result = search_clan(search_txt)['data']
        clan_ids = list(map(lambda clan: clan['clan_id'], result))
        clan_ids = ','.join(map(str, clan_ids))
        response_data = get_clan_info(clan_ids)['data']
        return [
            result_cls.from_data(data)
            for data in response_data.values()
        ]


class Clan(graphene.ObjectType):
    class Meta:
        interfaces = (IClan, )

    @classmethod
    def from_data(cls, data):
        return cls(
            name=data['name'],
            tag=data['tag'],
            clan_id=data['clan_id'],
            color=data['color'],
            members=data['members'],
        )

    def resolve_members(self, info):
        result_cls = manager.type_from_info(info)
        return [result_cls.from_data(member, self.clan_id) for member in self.members]

    @manager.to_gql_type
    def resolve_messages(self, info):
        return get_messages(self.clan_id)


class Member(graphene.ObjectType):
    class Meta:
        interfaces = (IMember,)

    @classmethod
    def from_data(cls, data, clan_id):
        return cls(
            name=data['account_name'],
            account_id=data['account_id'],
            role=data['role'],
            clan_id=clan_id,
        )

    def resolve_clan(self, info):
        result_cls = manager.type_from_info(info)
        return (clan_loader.load(self.clan_id)
                .then(lambda data: result_cls.from_data(data['data'][str(self.clan_id)])))


class Message(graphene.ObjectType):
    class Meta:
        interfaces = (IMessage, )
