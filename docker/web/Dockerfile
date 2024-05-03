FROM python:3.10-slim as web_builder

WORKDIR /opt/app/backend

COPY pyproject.toml .
COPY Makefile .

RUN apt update \
    && apt install -y make libmagic1 libpq-dev gcc git\
    && ls -la \
    && make install

FROM web_builder
WORKDIR /opt/app/backend

COPY . .

RUN cp config.py.example config.py

CMD ["make", "run_async_web", "async_port=8000", "async_host=0.0.0.0"]
