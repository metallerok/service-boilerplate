PYTHON_VENV=.venv/bin/python
PYTHON=$(shell if test -f ${PYTHON_VENV}; then echo ${PYTHON_VENV}; else echo ${SYSTEM_PYTHON}; fi)
CONTAINER_NAME = service-boilerplate

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
