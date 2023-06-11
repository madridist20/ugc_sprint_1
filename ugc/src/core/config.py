from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Конфиг сервиса"""

    service_host: str = Field('localhost', env='SERVICE_HOST')
    service_port: int = Field(8001, env='SERVICE_PORT')
    # authjwt_secret_key должен совпадать с сервисом авторизации
    authjwt_secret_key: str = Field(..., env='SERVICE_SECRET_KEY')

    kafka_server: str = Field('localhost:9092', env='KAFKA_HOST')
    kafka_topic: str = Field('views', env='KAFKA_TOPIC')

    class Config:
        env_file = "src/core/.env"
        env_file_encoding = "utf-8"


settings = Settings()
