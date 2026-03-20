import httpx
from loguru import logger
from typing import Annotated
from fastapi import Depends
from app.repositories import RepositoryRedis
from app.core.config import Settings, get_configs
from app.schemas import MessageSendStatus
from app.core import get_http_client

class MessageSendService:
    def __init__(self, repository: Annotated[RepositoryRedis, Depends()], credentials: Annotated[Settings, Depends(get_configs)], client: Annotated[httpx.AsyncClient, Depends(get_http_client)]):
        self.repository = repository
        self.credentials = credentials
        self.client = client

    async def send_message_whatsapp(self, chat_id: str, message: str) -> MessageSendStatus:
        headers = {
            "Authorization": f"Bearer {self.credentials.WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": chat_id,
            "type": "text",
            "text": {
                "body": message
            }
        }
        
        try:
            response = await self.client.post(self.credentials.WHATSAPP_API_URL, json=payload, headers=headers)

            response.raise_for_status()

            return MessageSendStatus(
                sucess=True,
                chat_id=chat_id
            )
        except httpx.HTTPError as e:
            logger.error(f"Erro no envio da mensagem para a API do Whatsapp. Erro: {e}")
            return MessageSendStatus(
                sucess=False,
                chat_id=chat_id,
                message_erro=str(e)
            )

    async def send_message_telegram(self, chat_id: str, message: str) -> MessageSendStatus:
        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "chat_id": chat_id,
            "text": message
        }

        try:
            response = await self.client.post(f"https://api.telegram.org/bot{self.credentials.TELEGRAM_TOKEN}/sendMessage", json=payload, headers=headers)

            response.raise_for_status()

            return MessageSendStatus(
                sucess = True,
                chat_id = chat_id
            )
        except httpx.HTTPError as e:
            logger.error(f"Erro no envio da mensagem para a API do Telegram. Erro: {e}")
            return MessageSendStatus(
                sucess=False,
                chat_id=chat_id,
                message_erro=str(e)
            )
