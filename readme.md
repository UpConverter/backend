# Backend часть для Up Converter
> [Frontend репозиторий](https://github.com/TimofeyTst/up_converter_frontend) 
## Настройка из докера
Предварительно нужно создать базу данных Postgres и файл ```.env``` в корне проекта по шаблону:
```
DATABASE_URL=postgresql://POSTGRES_USER:PASSWORD@upconverter_db:5432/upconverter

SITE_DOMAIN=0.0.0.0
SECURE_COOKIES=false

ENVIRONMENT=LOCAL

CORS_HEADERS=["*"]
CORS_ORIGINS=["http://localhost:3000"]
```
Далее надо освободить порт, используемый Postgres, после чего запускаем контейнер:

```
    docker network create upconverter_main
    docker-compose up -d --build
```
### Linter
```
    docker compose exec app format
```
## Настройка под Linux Ubuntu
### При необходимости создайте виртуальное окружение в Python
> Можно пропустить этот шаг
```
    python3 -m venv venv
    source venv/bin/activate
```
### Устанавливаем зависимости
> Внутри виртуального окружения или без него
```
    pip install -r requirements/base.txt
```
### Заполняем базу данных по умолчанию
``` 
    python -m src.__data__.initial_data 
```
> Чтобы добавить тестовые данные ``` python -m src.__data__.test_data ```
### Запускаем сервер
```
    uvicorn src.main:app --reload
```

------
## Работа с запущенным сервером
По умолчанию сервер доступен на локальной сети на порту 8000
http://127.0.0.1:8000/
> Для просмотра документации допишите в конце адреса путь docs:
> http://127.0.0.1:8000/docs

### Доп информация
Структура проекта взята [отсюда](https://github.com/zhanymkanov/fastapi-best-practices#1-project-structure-consistent--predictable)