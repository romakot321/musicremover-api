# MusicRemover API
Разделение трека на несколько аудио-дорожек по инструментам

## Запуск

Установка uv
```bash
pip install uv
```

Или через скрипт
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Загрузка зависимостей
```bash
uv sync --frozen
```

Создание вирт. окружения
```bash
cp example.env .env
# Отредактировать .env с необходимыми настройками
```

Запуск
```bash
docker compose up -d --build
```
Запуск профиля dev(прокинуты порты БД и приложения)
```bash
docker compose --profile dev up -d --build
```

Или локально
```bash
uvx uvicorn backend.src.main:app --reload
```

## Документация кода

Основная структура
```
backend
├── alembic                 Файлы alembic (миграции БД)
├── alembic.ini
└── src                     Модули
    ├── core                Внутренние настройки/часто используемое
    │   ├── config.py
    │   ├── admin.py
    │   └── logging_setup.py
    ├── db                  Настройки ORM и подключения к бд
    ├── integration         Модуль интеграции с внешними сервисами
    ├── main.py             Входная точка
    └── task                Модуль работы с задачами. Запуск, постановка в очередь и т.д.
```

Структура модуля
```
task
├── api                         Слой внешних данных

│   ├── dependencies.py         Зависимости модуля
│   ├── admin.py                Настройка ModelView для sqladmin
│   └── rest.py                 Эндпоинты FastAPI

├── application                 Слой бизнес-логики
│   ├── interfaces
│   │   ├── task_repository.py  Работа с моделью задачи в БД
│   │   ├── task_runner.py      Интерфейс для запуска и получения результата задачи
│   │   └── task_uow.py         Unit of work. Облегчает работу с сессиями
│   └── use_cases
│       ├── create_task.py      Сохранение задачи в БД
│       ├── get_task.py         Получение задачи из БД
│       └── run_task.py         Запуск задачи (через интеграцию)

├── domain                      Слой данных
│   ├── dtos.py
│   ├── entities.py             Предметные модели модуля
│   └── mappers.py              Перевод модели из одного вида в другой

└── infrastructure              Слой доступа к данным. Реализация интерфейсов.
    └── db                      Доступ к данным БД
        ├── orm.py              ORM модели(sqlalchemy)
        ├── task_repository.py
        └── unit_of_work.py
```

Флоу работы с задачей
1) src.task.api.rest - FastAPI POST /api/task
2) src.task.application.use_cases.create_task - Сохранение в БД
3) src.task.application.use_cases.run_task - Запускается в фоне. Запуск и ожидание результата
4) src.integration.infrastructure.task_runner - Работа с интеграцией(HTTP, отправка запроса, получение результата)
5) src.task.application.use_cases.run_task - Сохранение результата (контент или ошибка) в БД
6) src.task.api.rest - FastAPI GET /api/task/{task_id}
7) src.task.application.use_cases.get_task - Получение задачи из БД

Архитектура позволяет легко расширять имеющуюся бизнес-логику, переписывать отдельные части и разрабатывать тесты. Рекомендую строго соблюдать ее, для простоты поддержки API
