Для осуществляения миграции:
1) Импортировать новые модели в migrations/env.py (мб не обязательно)
2) Зайти в контейнер
3) Выполнить команду 
```shell
uv run alembic revision --autogenerate -m "Migration name"
```
4) Применение миграции:
```shell
uv run alembic upgrade head
```