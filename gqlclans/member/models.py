import graphene

from gqlclans.clan.resolvers import resolve_member_clan


class Member(graphene.ObjectType):
    name = graphene.String()
    account_id = graphene.ID()
    role = graphene.String()
    clanId = graphene.String()
    clan = graphene.Field('gqlclans.clan.models.Clan', resolver=resolve_member_clan)

