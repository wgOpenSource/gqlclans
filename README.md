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

To run http server command:

    ```bash
    python start_app.py
    ```

Now you can visit [http://localhost:8567](http://localhost:8567) and play with GraphQL queries in GraphiQL console


## Docker

To run backend container from docker:

    ```bash
    docker create --name=gqlclans -t -i -p 8567:8567 sudoaptget/gqlclans:latest
    docker start -i gqlclans
    ```

Service will be available via [http://0.0.0.0:8567](http://0.0.0.0:8567)

## Contibuting

After developing, the full test suide can be evaluated by running:
    ```bash
    tox
    ```