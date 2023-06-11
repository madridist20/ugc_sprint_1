import time
from functools import wraps

from core.log_writer import logger


def backoff(error, start_sleep_time: float = 0.1, factor: int = 2, border_sleep_time: int = 10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param error: тип ошибки для обработки
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            n = 1
            t = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except error:
                    t = start_sleep_time * factor**n if t < border_sleep_time else border_sleep_time
                    n += 1
                    time.sleep(t)
                    logger.error("Connection is broken. Reconnection after %s seconds", t)

        return inner

    return func_wrapper
