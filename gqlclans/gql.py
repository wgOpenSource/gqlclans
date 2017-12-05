
import json

from gqlclans.schema import schema


query = '''
{
    search(searchTxt: "BOU" ) {
        tag
        name
    }
}
'''

query = '''
{
    clans(clanId: "10164") {
      tag
      name
      members {
        name
        role
      }
    }
}
'''

result = schema.execute(query)

if result.errors:
    print(result.errors)
    exit(1)

print(json.dumps(result.data,indent=2))
