from abc import ABC, abstractmethod
from dataclasses import dataclass

from aiokafka import AIOKafkaProducer


class AbstractProducer(ABC):
    """Абстрактный класс для подключения к хранилищу."""

    @abstractmethod
    def send(self, topic: str, value: bytes, key: bytes):
        """Метод отправки данных в хранилище"""
        pass


@dataclass
class KafkaProducer(AbstractProducer):
    """
    Класс для отправки данных в Kafka
    """
    kafka: AIOKafkaProducer

    async def send(self, topic: str, value: bytes, key: bytes):
        """
        Метод отправки данных в Kafka

        :param topic: топик в Kafka
        :param value: тело сообщения
        :param key: ключ сообщения
        """
        await self.kafka.send(topic=topic, value=value, key=key)
