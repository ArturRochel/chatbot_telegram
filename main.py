import httpx
import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core import get_redis
from app.core import get_configs
from app.api.v1.routers import chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    env = get_configs()
    client_redis = redis.from_url(env.REDIS_URL, decode_responses=True)
    await client_redis.ping()

    async with httpx.AsyncClient() as client:
        app.state.http_client = client
        yield

app = FastAPI(title="Chatbot SEFAZ", description="Projeto laboratório para desenvolvimento do chatbot para telegram", lifespan=lifespan)

app.include_router(chat_router)