import json
import redis.asyncio as redis
from fastapi import Depends
from typing import Annotated
from app.core import get_redis
from loguru import logger

class RepositoryRedis:
    def __init__(self, client_redis: Annotated[redis.Redis, Depends(get_redis)]):
        self.redis = client_redis

    async def get_session(self, chave: str):
        try:
            sessao = await self.redis.get(chave)
        except Exception as e:
            logger.error(f"Erro ao puxar sessão no Redis. Erro: {e}")
            raise
        
        sessao_dict = json.loads(sessao)
        return sessao_dict

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