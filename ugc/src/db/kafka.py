from typing import Optional
from aiokafka import AIOKafkaProducer

kafka: Optional[AIOKafkaProducer] = None


# Функция понадобится при внедрении зависимостей
async def get_kafka() -> AIOKafkaProducer:
    return kafka
