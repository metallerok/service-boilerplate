PYTHON_VENV=.venv/bin/python
SYSTEM_PYTHON=$(shell which python3 || shell which python)

PYTHON=$(shell if test -f ${PYTHON_VENV}; then echo ${PYTHON_VENV}; else echo ${SYSTEM_PYTHON}; fi)
CONTAINER_NAME = boilerplate-web

async_port ?= 8001
async_host ?= localhost

install:
	$(PYTHON) -m pip install -e .

install_dev:
	$(PYTHON) -m pip install -e .[dev]

test:
	$(PYTHON) -m pytest -x -s -v

run_web:
	$(PYTHON) -m gunicorn -c gunicorn.conf.py 'src.modules.core.entrypoints.wsgi.wsgi:make_app()'

run_async_web:
	$(PYTHON) -m uvicorn --reload --factory 'src.modules.core.entrypoints.asgi.asgi:make_app' --port $(async_port) --host $(async_host)

migrate_up:
	$(PYTHON) -m alembic upgrade head

migrate_down:
	$(PYTHON) -m alembic downgrade -1

migration:
	$(PYTHON) -m alembic revision --autogenerate -m $(name)

docker_build:
	docker build -t $(CONTAINER_NAME) -f docker/web/Dockerfile .

docker_up:
	docker compose -f docker/docker-compose.dev.yml up

docker_down:
	docker compose -f docker/docker-compose.dev.yml down

docker_test:
	docker compose -f docker/docker-compose.dev.yml exec -it $(CONTAINER_NAME) make test

docker_migrate_up:
	docker compose -f docker/docker-compose.dev.yml exec -it '$(CONTAINER_NAME)' make migrate_up

docker_migrate_down:
	docker compose -f docker/docker-compose.dev.yml exec -it $(CONTAINER_NAME) make migrate_down
