from typing import Annotated
from fastapi import Depends
from app.schemas import WebhookTelegram, WebhookWhatsapp
from app.repositories import RepositoryRedis

repository_redis = Annotated[RepositoryRedis, Depends()]

class MachineState():

    def __init__(self, repository: repository_redis):
        self.repository = repository

    async def handle_update_telegram(self, data_message: WebhookTelegram):
        chat_id, message = self.extract_telegram_data(data=data_message)

        # Verifica se esse uusário já está no Redis, se não estiver adiciona
    async def handle_update_whatsapp(self, data_message: WebhookWhatsapp):
        chat_id, message = self.extract_whatsapp_data(data=data_message)