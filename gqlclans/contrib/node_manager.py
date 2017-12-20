import collections
from functools import wraps

from graphene.utils.deprecated import string_types


class NodeManager(object):
    def __init__(self):
        self._nodes = {}

    def register(self, *nodes):
        self._nodes.update(dict(nodes))

    def resolve(self, base_node):
        return self._nodes[base_node]

    def type_from_info(self, info):
        if hasattr(info.return_type, 'graphene_type'):
            type_to_resolve = info.return_type.graphene_type
        else:
            type_to_resolve = info.return_type.of_type.graphene_type
        return self.resolve(type_to_resolve)

    def to_gql_type(self, func):
        @wraps(func)
        def __decorator__(*args, **kwargs):
            info = args[1]
            result = func(*args, **kwargs)
            result_type = self.type_from_info(info)
            if isinstance(result, collections.Mapping):
                result = result_type(**result)
            elif isinstance(result, collections.Iterable) and not isinstance(result, string_types):
                result = map(lambda r: result_type(**r), result)
            return result

        return __decorator__

    def types(self):
        return self._nodes.values()


manager = NodeManager()
