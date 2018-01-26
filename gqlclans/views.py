from aiohttp_graphql import GraphQLView as BaseGraphQLView

from gqlclans.data_loaders import DataLoaders


class ClansGraphQLView(BaseGraphQLView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context(self, request):
        context = super().get_context(request)
        context.update({
            'data_loaders': DataLoaders,
        })
        return context
