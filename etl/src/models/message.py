

class Message:
    """ Модель одного сообщения из Kafka"""

    def __init__(self, user_movie_ids: bytes, timestamp: bytes):
        self.user_id: str = user_movie_ids.decode("utf-8").split('+')[0]
        self.movie_id: str = user_movie_ids.decode("utf-8").split('+')[1]
        self.event_ts: int = int(timestamp.decode("utf-8"))

