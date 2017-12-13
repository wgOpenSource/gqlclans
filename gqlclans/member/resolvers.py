def resolve_members(root, info):
    from gqlclans.member.models import Member
    return map(lambda member: Member(
        name=member['account_name'],
        account_id=member['account_id'],
        role=member['role'],
        clanId=root.clan_id,
    ), root.members)
