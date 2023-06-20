# Backend часть для Up Converter
## Запуск под Linux Ubuntu
### Если вы хотите создать виртуальное окружение в Python:
```
    python3 -m venv venv
    source venv/bin/activate
```
### Далее устанавливаем зависимости
> Из виртуального окружения, или вне него
```
    pip install -r reqs.txt
```
### Запускаем сервер
```
    cd app/
    uvicorn main:app --reload
```
