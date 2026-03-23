from app.schemas import OriginService
import httpx
import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import get_redis
from app.core import get_configs
from app.api.v1.routers import chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    env = get_configs()
    client_redis = redis.from_url(env.REDIS_URL, decode_responses=True)
    await client_redis.ping()
    
    app.state.redis = client_redis 

    async with httpx.AsyncClient() as client:
        app.state.http_client = client
        yield
    
    await app.state.redis.close()

app = FastAPI(title="Chatbot SEFAZ", description="Projeto laboratório para desenvolvimento do chatbot para telegram", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

app.include_router(chat_router)

