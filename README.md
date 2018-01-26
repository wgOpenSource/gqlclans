# GQL Clans

A boilerplate app with integration [Wargaming public API](https://developers.wargaming.net/reference/) for [Graphene](http://graphene-python.org/).

## Installation

Install python packages in virtualenv:

```bash
    cd gqlclans
    mkvirtualenv gqlclans --python=python3.6
    pip install -r requirements.txt
```

## Usage

Generate settings

    ```bash
    python ./scripts/init_settings.py <WGAPI_APPLICATION_ID>
    ```

To run http server command:

```bash
    python start_app.py
```

To run server with reload mode use aiohttp-devtools `adev` comand:

```bash
adev runserver start_app.py --port=8567
```

Now you can visit [http://localhost:8567](http://localhost:8567) and play with GraphQL queries in GraphiQL console


## Docker

To run backend container from docker:

```bash
    docker create --name=gqlclans -t -i -p 8567:8567 sudoaptget/gqlclans:latest -e WGAPI_APPLICATION_ID=<WGAPI_APPLICATION_ID>
    docker start -i gqlclans
```

Service will be available via [http://0.0.0.0:8567](http://0.0.0.0:8567)


## Contributing
    
After developing, the full test suite can be evaluated by running:

```bash
    pytest --benchmark-skip  # Use -v -s for verbose mode
```
    
You can also run the benchmarks with:
    
```bash
    pytest --benchmark-only
```
    
For isolation, it could be better to use tox for running tests:

```bash
    tox
```