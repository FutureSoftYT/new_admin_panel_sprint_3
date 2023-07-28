from functools import wraps
from time import sleep

from logger import logger


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Function for retrying the execution of a function after a certain time if an error occurs. It uses a naive exponential growth of the waiting time (factor) up to the maximum waiting time (border_sleep_time).

    Formula:
    t = start_sleep_time * 2^(n) if t < border_sleep_time
    t = border_sleep_time if t >= border_sleep_time

    :param start_sleep_time: initial waiting time
    :param factor: factor by which the waiting time should be increased
    :param border_sleep_time: maximum waiting time
    :return: result of the function execution
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            while True:
                try:
                    result = func(*args, **kwargs)
                    break
                except Exception as e:
                    logger.error('App stop with error: %s', (e,))
                    logger.info('Will retry in: %s seconds', (sleep_time,))

                sleep(sleep_time)
                new_sleep_time = sleep_time * 2 ** factor
                sleep_time = new_sleep_time if new_sleep_time < border_sleep_time else border_sleep_time

            return result

        return inner

    return func_wrapper
