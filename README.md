## Первый запуск

1) Сформируй виртуальное Python-окружение
2) Установи зависимости `pip install -r requirements.txt`
3) Установи pre-commit hook `pre-commit install`

## Запуск Docker
1) Создать docker контейнеры `docker-compose build`
2) Запуск `docker-compose up`

## Линтер

Конфигурация для flake8 находится в `setup.cfg`

Запуск flake8: `flake8`

Запуск isort: `isort .`

## Тестирование

Запуск: `pytest .`

## CI-CD

В GitHub actions настроен запуск линтера и тестов при событии push.

## Документация
[OpenAPI](http://0.0.0.0:8000/swagger-ui/ "Посмотреть")

## AsyncApi (for grpc)
[AsyncApi](https://github.com/ziminyuri/Async_API "Посмотреть")

## Чтобы создать суперпользователя, необходимо:
1) `сd src`
2) `flask create_superuser USERNAME PASSWORD`

## Чтобы записать БД фейковыми данными запустите скрипт
`tests/scripts/add_fake_data.py`
