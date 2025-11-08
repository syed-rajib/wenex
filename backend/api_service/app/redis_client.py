import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis_fastapi")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# decode_responses=True makes sure we get string data (not bytes)
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
