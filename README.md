<h2>Тестовое задание компании S7</h2>

### Поднятие проекта локально:

Создать окружение и активировать его
```
python -m venv venv 
venv\Scripts\activate
```

Установить poetry
```
pip install poetry
```

Установить зависимости
```
poetry lock
poetry install
```

Применить миграции
```
alembic upgrade heads
```

Запустить проект
```
uvicorn --host 127.0.0.1 --port 8000 --reload src.main:app
```

### Поднятие проекта в докере:

```
docker-compose up --build -d
```
