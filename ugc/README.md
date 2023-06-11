# Код FAST API приложения

## Локальный запуск
Предварительно необходимо создать файл `src/core/.env` со следующими параметрами:
```dotenv
SERVICE_SECRET_KEY - секретный ключ, должен совпадать с сервисом авторизации
KAFKA_HOST - сервер кафки
KAFKA_TOPIC - название топика в кафка
```

Для запуска api под `uvicorn`:
```shell
uvicorn main:app --reload --host localhost --port 8001
```
Для запуска api под `gunicorn`:
```shell
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornH11Worker --bind 0.0.0.0:8001
```

Адрес документации: http://localhost:8001/apidocs/


## Запуск в Docker
Предварительно необходимо создать файл `src/core/docker.env` со следующими параметрами:
```dotenv
SERVICE_SECRET_KEY - секретный ключ, должен совпадать с сервисом авторизации
KAFKA_HOST=broker:29092
KAFKA_TOPIC - название топика в кафка
```

Для запуска api в `Docker` необходимо выполнить команду
```shell
docker compose up --build
```

Адрес документации: http://localhost:8005/apidocs/
