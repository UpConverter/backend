# Backend часть для Up Converter
> [Frontend репозиторий](https://github.com/TimofeyTst/up_converter_frontend) 
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
    pip install -r reqs.txt
```
### Заполняем базу данных по умолчанию
``` 
    python -m app.data.initial_data 
```
> Чтобы добавить тестовые данные ``` python -m app.data.test_data ```
### Запускаем сервер
```
    uvicorn app.main:app --reload
```

------
## Работа с запущенным сервером
По умолчанию сервер доступен на локальной сети на порту 8000
http://127.0.0.1:8000/
> Для просмотра документации допишите в конце адреса путь docs:
> http://127.0.0.1:8000/docs