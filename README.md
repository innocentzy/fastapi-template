# FastAPI Template

Шаблон для быстрого старта REST API на FastAPI с асинхронным SQLAlchemy, JWT-аутентификацией, миграциями через Alembic и тестами на pytest.

## Стек

- **FastAPI** — веб-фреймворк
- **SQLAlchemy 2.0** (async) — ORM
- **Alembic** — миграции базы данных
- **SQLite** (для разработки) / **PostgreSQL** (для продакшена)
- **JWT** — аутентификация через access + refresh токены
- **bcrypt** — хэширование паролей
- **pytest + pytest-asyncio** — тестирование

## Структура проекта

```
.
├── app/
│   ├── models/         # SQLAlchemy модели
│   ├── routes/         # API роутеры
│   ├── schemas/        # Pydantic схемы
│   ├── config.py       # Настройки через pydantic-settings
│   ├── crud.py         # Операции с базой данных
│   ├── database.py     # Engine, сессия, Base
│   ├── dependencies.py # FastAPI зависимости (auth guards)
│   ├── main.py         # Точка входа
│   └── security.py     # JWT и утилиты для паролей
├── migrations/         # Alembic миграции
├── tests/
│   ├── conftest.py     # Фикстуры (in-memory тестовая БД)
│   └── test_auth.py
├── .env.example
├── alembic.ini
├── requirements.in
└── requirements.txt
```

## Быстрый старт

### 1. Клонировать и настроить окружение

```bash
git clone https://github.com/innocentzy/fastapi-template.git
cd fastapi-template

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Настроить переменные окружения

```bash
cp .env.example .env
```

Откройте `.env` и задайте свои значения.

### 3. Применить миграции

```bash
alembic upgrade head
```

### 4. Запустить сервер

```bash
uvicorn app.main:app --reload
```

API доступен по адресу `http://localhost:8000`  
Swagger-документация — `http://localhost:8000/docs`

## Эндпоинты аутентификации

| Метод | Эндпоинт                | Описание                      |
| ----- | ----------------------- | ----------------------------- |
| POST  | `/auth/register/{role}` | Регистрация (`role`: `user`)  |
| POST  | `/auth/login`           | Вход, возвращает пару токенов |
| POST  | `/auth/update-token`    | Обновление access-токена      |

## Запуск тестов

```bash
pytest
```

Тесты используют in-memory SQLite и не затрагивают локальные данные.

## Переход на PostgreSQL

В `.env` замените `DATABASE_URL`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/mydb
```

Затем пересоздайте миграции:

```bash
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

## Как использовать шаблон

1. Добавляйте модели в `app/models/`
2. Создавайте схемы в `app/schemas/`
3. Пишите бизнес-логику в `app/crud.py`
4. Регистрируйте роутеры в `app/main.py`
5. Генерируйте миграции: `alembic revision --autogenerate -m "описание"`
