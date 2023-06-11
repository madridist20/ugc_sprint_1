from abc import ABC, abstractmethod

from clickhouse_driver import Client, errors as ch_errors

from src.models.message import Message
from core.config import ClickHouseSettings
from src.backoff import backoff
from core.log_writer import logger


class AbstractWriter(ABC):
    """Абстрактный класс для подключения к хранилищу."""

    @abstractmethod
    def write_messages(self, messages: list[Message]):
        pass


class ClickHouseWriter(AbstractWriter):
    """Класс для подключения к ClickHouse"""

    def __init__(self, conf: ClickHouseSettings):
        self.__conf = conf
        self.__client = None
        self.__connect()

    @backoff(error=(ch_errors.NetworkError, EOFError), start_sleep_time=2)
    def __connect(self):
        self.__client = Client(host=self.__conf.host)
        self.__client.execute('SHOW DATABASES')
        logger.info('ClickHouse connected!')

    def __write_message(self, messages: list[Message]):
        self.__client.execute(
            "INSERT INTO default.movie_events (userId, movieId, event_ts) VALUES",
            ((message.user_id, message.movie_id, message.event_ts,) for message in messages)
        )

    def write_messages(self, messages: list[Message]):
        """
        Метод записи сообщений в ClickHouse

        :param messages: список сообщений
        """
        try:
            self.__write_message(messages)
        except (ch_errors.NetworkError, EOFError):
            self.__connect()
            self.__write_message(messages)

