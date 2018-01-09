# Installation

Install python packages in virtualenv:

    ```
    cd gqlclans
    mkvritualenv gqlclans --python=python3
    pip install -r requirements
    ```


# Usage

Generate settings

    ```
    python ./scripts/init_settings.py <WGAPI_APPLICATION_ID>
    ```

To run http server command:

    ```
    python start_app.py
    ```

Now you can visit [http://localhost:8567](http://localhost:8567) and play with GraphQL queries in GraphiQL console


# Docker

To run backend container from docker:

    ```
    docker create --name=gqlclans -t -i -p 8567:8567 sudoaptget/gqlclans:latest -e WGAPI_APPLICATION_ID=<WGAPI_APPLICATION_ID>
    docker start -i gqlclans
    ```

Service will be available via [http://0.0.0.0:8567](http://0.0.0.0:8567)

