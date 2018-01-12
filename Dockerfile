FROM python:3.6

COPY requirements.txt /src/requirements.txt
RUN pip install tox && \
    pip install -r /src/requirements.txt

WORKDIR /src
COPY scripts/start.sh start.sh
COPY ./start_app.py ./tox.ini ./settings.py /src/
COPY scripts/init_settings.py /src/scripts/init_settings.py
COPY tests tests
COPY gqlclans gqlclans

RUN python ./scripts/init_settings.py -s "os.environ.get('WGAPI_APPLICATION_ID')"

EXPOSE 8567

CMD /src/start.sh
