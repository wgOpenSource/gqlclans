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

    def process_preflight(self, request):
        response = super().process_preflight(request)
        accepted_headers = ('Content-Type',)
        if response.status == 200:
            response.headers.update({
                'Access-Control-Allow-Headers': ', '.join(accepted_headers),
            })
        return response

    async def __call__(self, request):
        response = await super().__call__(request)
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
        })
        return response
