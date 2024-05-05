# Начало работы
## Установить dev зависимости командой:
```bash
make install_dev
```

## Скопировать и настроить конфиг
```bash
cp config.py.example config.py
```

## Собрать docker образ вебсервера
```bash
make docker_build
```

## Запустить docker-compose который поднимет дополнительные сервисы (базы данных, брокеры, кеш)
```bash
make docker_up
```

## Вместе с запущенными докер сервисами можно выполнять тесты
```bash
make test
```

# Разработка модуля
Модули добавляются в `src.modules.{module_name}`. API эндпоинты добавленные в модуль после необходимо подключить в `src.modules.core.entrypoints.wsgi.wsgi.py` для синхронного API или в `src.modules.core.entrypoints.asgi.asgi.py` для асинхронного API.

Модели модуля нужно зарегистрировать в `src.lib.models_scanner`


От в зависимости от выбора типа API стоит подправить `docker/web/Dockerfile` для запуска нужного сервера
