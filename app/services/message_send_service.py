import httpx
from loguru import logger
from typing import Annotated, Dict, Any
from fastapi import Depends
from app.repositories import RepositoryRedis
from app.core.config import Settings

class MessageSendService:
    def __init__(self, repository: Annotated[RepositoryRedis, Depends()], credentials: Annotated[Settings, Depends()]):
        self.repository = repository
        self.credentials = credentials

    async def send_message_whatsapp(self, chat_id: str, message: str):
        headers = {
            "Authorization": f"Bearer {self.credentials.WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }

        paylaod = {
            "messaging_product": "whatsapp",
            "to": chat_id,
            "type": "text",
            "text": {
                "body": message
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.credentials.WHATSAPP_API_URL, json=paylaod, headers=headers)

                response.raise_for_status()

                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Erro no envio da mensagem para a API do Whatsapp. Erro: {e}")

    async def send_message_telegram(self, chat_id: str, message: str):
        #todo - A API do telegram utiliza a autenticação de token através da URL, então é preciso fazer a concatenação do token na URL
        headears = {
            "Authorization": f"Bearer {self.credentials.TELEGRAM_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "chat_id": chat_id,
            "text": message
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.credentials.TELEGRAM_API_URL)

                response.raise_for_status()

                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Erro no envio da mensagem para a API do Telegram. Erro: {e}")