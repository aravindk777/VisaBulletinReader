"""
A decorator that applies an LRU cache with a time-based expiration.
The cache is cleared after a specified number of seconds.
"""

from datetime import timedelta, datetime, timezone
from functools import lru_cache, wraps

def timed_lru_cache(seconds: int, maxsize: int = None):
    """
    Function to create a timed LRU cache decorator.
    :param seconds: The number of seconds before the cache expires.
    :param maxsize: The maximum size of the LRU cache.
    :return: The decorated function with caching.
    """

    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.now(timezone.utc) + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            print(f'datetime.now(timezone.utc): {datetime.now(timezone.utc)}, '
                  f'func.expiration: {func.expiration}')
            if datetime.now(timezone.utc) >= func.expiration:
                print('func.expiration lru_cache lifetime expired')
                func.cache_clear()
                func.expiration = datetime.now(timezone.utc) + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
