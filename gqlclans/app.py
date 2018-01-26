import json

from aiohttp import web
from gqlclans.views import ClansGraphQLView

from gqlclans.schema import schema


app = web.Application()
app.router.add_get('/', lambda req: web.HTTPTemporaryRedirect(f'/graphiql?{req.query_string}'))
app.router.add_get('/schema', lambda req: web.Response(body=json.dumps({'data': schema.introspect()})))

graphiql_view = ClansGraphQLView(schema=schema, graphiql=True)
app.router.add_route('*', '/graphiql', graphiql_view)

graphql_view = ClansGraphQLView(schema=schema, batch=True)
app.router.add_route('*', '/graphql', graphql_view)

