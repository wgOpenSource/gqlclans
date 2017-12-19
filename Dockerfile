FROM python:3.6

RUN mkdir /src
WORKDIR /src

COPY requirements.txt requirements.txt
RUN pip install tox && \
    pip install -r requirements.txt

COPY scripts/start.sh start.sh
COPY ./start_app.py ./tox.ini /src/
COPY tests tests
COPY gqlclans gqlclans

EXPOSE 8567

CMD /src/start.sh
