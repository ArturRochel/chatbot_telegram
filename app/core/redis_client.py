import os
import redis.asyncio as redis
from loguru import logger

_redis_client = None

async def get_redis():
    global _redis_client

    if _redis_client is None:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

        _redis_client = redis.from_url(redis_url, decode_responses=True)

        try:
            await _redis_client.ping()
            logger.info("Conexão com o Redis estabalecida com sucesso")
        except Exception as e:
            logger.error(f"Falha ao conextar no Redis: {e}")
            raise e

    return _redis_client