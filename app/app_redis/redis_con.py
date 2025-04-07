import os

import redis_om
from dotenv import load_dotenv

load_dotenv()
REDIS_HOST, REDIS_PORT = str(os.getenv("REDIS_CONNECTION")).split(":")
REDIS_TIMEOUT = int(os.getenv("REDIS_TIMEOUT"))

RedisConnection = redis_om.get_redis_connection(
    host=REDIS_HOST,
    port=int(REDIS_PORT),
    decode_responses=True,
    socket_timeout=REDIS_TIMEOUT
)
