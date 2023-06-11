from fastapi import Depends
from aiokafka import AIOKafkaProducer

from src.db.kafka import get_kafka
from src.utils.kafka_producer import AbstractProducer
from src.utils.kafka_producer import KafkaProducer


class EventService:
    """
    Сервис взаимодействия с Kafka
    """
    def __init__(self, kafka: AbstractProducer):
        self.kafka = kafka

    async def send_event(self, topic: str, value: bytes, key: bytes):
        """
        Метод отправки события в Kafka

        :param topic: топик в Kafka
        :param value: тело сообщения
        :param key: ключ сообщения
        """
        await self.kafka.send(topic=topic, value=value, key=key)


def get_event_service(
        kafka: AIOKafkaProducer = Depends(get_kafka)
) -> EventService:
    """
    Провайдер EventService,
    с помощью Depends он сообщает, что ему необходимы AIOKafkaProducer
    """
    return EventService(KafkaProducer(kafka))
