from fastapi import APIRouter, Depends
from typing import Annotated
from app.schemas import WebhookTelegram, WebhookWhatsapp
from app.services import MachineState

machine_state = Annotated[MachineState, Depends()]
chat_router = APIRouter(prefix="/webhook")

@chat_router.post("/telegram", tags=["Webhook"], summary="Rota de webhook para atualizações pela API do Telegram", description="Essa rota é responsável por receber as atualizações do sistema através da API oficial do Telegram, utilizando uma lógica de webhook.")
async def telegram_receiver(message_api: WebhookTelegram, service: machine_state):
    pass

@chat_router.post("/whatsapp", tags=["Webhook"], summary="Rota de webhook para atualizações pela API do Whatsapp", description="Essa rota é responsável por receber as atualizações do sistema através da API oficial do Whatsapp, utilizando uma lógica de webhook.")
async def whatsapp_receiver(message_api: WebhookWhatsapp, service: machine_state):
    pass