import redis.asyncio as redis
from fastapi import Request

_redis_client = None

async def get_redis(request: Request) -> redis.Redis:
    return request.app.state.redis