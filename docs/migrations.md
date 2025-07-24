Для осуществляения миграции:
1) Импортировать новые модели в models/__init__.py
2) Зайти в контейнер
3) Выполнить команду 
```shell
uv run --no-sync alembic revision --autogenerate -m "Migration name"
```
4) Применение миграции:
```shell
uv run --no-sync alembic upgrade head
```