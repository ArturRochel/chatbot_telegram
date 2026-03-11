from app.schemas import UserSession
import json
import redis.asyncio as redis
from fastapi import Depends
from typing import Annotated
from app.core import get_redis
from loguru import logger
from app.schemas import UserSession, FullSession

class RepositoryRedis:
    def __init__(self, client_redis: Annotated[redis.Redis, Depends(get_redis)]):
        self.redis = client_redis

    async def save_session_and_history(self, chat_id:str, origin:str, session_data: dict, history_data: list):
        session_key = f"session:{origin}:{chat_id}"
        history_key = f"history:{origin}:{chat_id}"

        serialized_history = [json.dumps(message) for message in history_data]

        try:
            await self.redis.hset(session_key, mapping=session_data)

            if serialized_history:
                await self.redis.rpush(history_key, *serialized_history)
                await self.redis.ltrim(history_key, -20, -1)

            await self.redis.expire(session_key, 86400)
            await self.redis.expire(history_key, 86400)
        except Exception as erro:
            logger.error(f"Erro na persistência Redis. Erro: {erro}")

    async def get_session_and_history(self, chat_id: str, origin: str) -> FullSession | None:
        session_key = f"session:{origin}:{chat_id}"
        history_key = f"history:{origin}:{chat_id}"

        session_data, history_string_data = await asyncio.gather(
            self.redis.hgetall(session_key),
            self.redis.lrange(history_key, 0, -1)
        )

        if not session_data:
            return None

        if history_string_data:
            history_data = [json.loads(message) for message in history_string_data]
        else:
            history_data = []

        return FullSession(session=UserSession(**session_data), history=history_data)

    async def add_session(self, chave: str, sessao: dict):
        sessao_string = json.dumps(sessao)

        await self.redis.set(chave, sessao_string, ex=86400)

    async def delete_session(self, chave=str):
        try:
            await self.redis.delete(chave)
        except Exception as e:
            logger.error(f"Erro ao excluir sessão {chave}. Erro: {e}")
            raise 
        

    async def edit_session(self, chave:str, novos_dados:dict):
        sessao_atual = await self.get_session(chave=chave)

        if sessao_atual:
            sessao_atual.update(novos_dados)
            await self.add_session(chave, sessao_atual)
        else:
            logger.warning(f"Tentativa de editar uma sessão inexistente. Sessão: {chave}")