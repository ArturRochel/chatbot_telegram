import httpx
from loguru import logger
from typing import Annotated
from fastapi import Depends
from app.repositories import RepositoryRedis
from app.core.config import Settings
from app.schemas import MessageSendStatus

class MessageSendService:
    def __init__(self, repository: Annotated[RepositoryRedis, Depends()], credentials: Annotated[Settings, Depends()]):
        self.repository = repository
        self.credentials = credentials

    async def send_message_whatsapp(self, chat_id: str, message: str) -> MessageSendStatus:
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
        headears = {
            "Content-Type": "application/json"
        }

        payload = {
            "chat_id": chat_id,
            "text": message
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"https://api.telegram.org/bot{self.credentials.TELEGRAM_TOKEN}/sendMessage", json=payload, headers=headears)

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
