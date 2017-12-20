from gqlclans.contrib.node_manager import manager
from gqlclans.server_info.dtos import (
    IServerInfo,
)
from gqlclans.server_info.resolvers import (
    ServerInfo,
)

manager.register(
    (IServerInfo, ServerInfo),
)
