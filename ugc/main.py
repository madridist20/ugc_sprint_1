import sys
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_jwt_auth import AuthJWT
from aiokafka import AIOKafkaProducer
from contextlib import asynccontextmanager

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.api.v1 import films
from src.core.config import settings
from src.db import kafka


@asynccontextmanager
async def lifespan(application: FastAPI):
    kafka.kafka = AIOKafkaProducer(bootstrap_servers=settings.kafka_server)
    await kafka.kafka.start()
    yield
    await kafka.kafka.stop()


# Создание FastAPI приложения
app = FastAPI(
    title='name',
    description="API записи информации о просмотре фильма в Kafka",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    version='1.0.0',
    lifespan=lifespan
)


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return settings



# Подключаем роутер к серверу, указав префикс /v1/films
app.include_router(films.router, prefix='/api/v1/films', tags=['films'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.service_host,
        port=settings.service_port,
    )
