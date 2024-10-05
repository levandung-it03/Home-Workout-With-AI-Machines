from redis import StrictRedis


class Settings:
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_TIMEOUT: int = 60  # in seconds
    REDIS_PASSWORD: str = None  # set to None if no password


def connect_and_return():
    settings = Settings()
    return StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        socket_timeout=settings.REDIS_TIMEOUT / 1000.0  # Convert to seconds
    )

RedisConnection = connect_and_return()