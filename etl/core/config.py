from pydantic import BaseSettings, Field


class KafkaSettings(BaseSettings):
    """Конфиг Kafka"""

    topic_name: str = 'views'
    host: str = Field('localhost:9092', env='KAFKA_HOST')
    auto_offset_reset: str = 'earliest'
    group_id: str = 'echo-messages-to-stdout'
    enable_auto_commit = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class ClickHouseSettings(BaseSettings):
    """Конфиг ClickHouse"""

    host: str = Field('localhost', env='CLICKHOUSE_HOST')
    wait_time: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


clickhouse_conf = ClickHouseSettings()
kafka_conf = KafkaSettings()


class LoggerSettings(BaseSettings):
    """Конфиг логирования."""

    version: int = 1
    disable_existing_loggers: bool = False

    formatters: dict = {
        "default_formatter": {
            "format": '%(levelname)s\t%(asctime)s\t%(funcName)s\t"%(message)s"'
        },
    }

    handlers: dict = {
        "file_handler": {
            "class": "logging.FileHandler",
            "filename": "logs.log",
            "formatter": "default_formatter",
        },
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
        },
    }

    loggers: dict = {
        "my_logger": {
            "handlers": ["stream_handler"],
            "level": "DEBUG",
            "propagate": True,
        }
    }
