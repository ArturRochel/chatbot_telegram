from fastapi import APIRouter
import redis.asyncio as redis

chat_router = APIRouter(prefix="/chat")

redis_client = redis.from_url("reddis://localhost",port=5500, decode_respose=True)

redis_client.set('teste', 'concluido')
redis_client.get('teste')