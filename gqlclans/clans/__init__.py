from gqlclans.contrib.node_manager import manager
from gqlclans.clans.dtos import (
    IMember,
    IClan,
    IMessage,
    IAddMessage,
)
from gqlclans.clans.resolvers import (
    Member,
    Clan,
    Message,
)
from gqlclans.clans.mutations import AddMessage


manager.register(
    (IMember, Member),
    (IClan, Clan),
    (IMessage, Message),
    (IAddMessage, AddMessage)
)
