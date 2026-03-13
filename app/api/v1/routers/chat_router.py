from fastapi import APIRouter, Depends, BackgroundTasks
from typing import Annotated
from app.schemas import WebhookTelegram, WebhookWhatsapp
from app.services import MachineState
from app.utils import extract_telegram_data, extract_whatsapp_data

chat_router = APIRouter(prefix="/webhook")

async def process_webhook_payload(service: Annotated[MachineState, Depends()], message_api: WebhookTelegram | WebhookWhatsapp, api: str):
    if(api == "TELEGRAM"):
        chat_id, message = extract_telegram_data(data=message_api)
    elif(api == "WHATSAPP"):
        chat_id, message = extract_whatsapp_data(data=message_api)
        
    await service.handle_update(chat_id=chat_id, message=message, origin_service=api)
    

@chat_router.post("/telegram", tags=["Webhook"], summary="Rota de webhook para atualizações pela API do Telegram", description="Essa rota é responsável por receber as atualizações do sistema através da API oficial do Telegram, utilizando uma lógica de webhook.")
async def telegram_receiver(message_api: WebhookTelegram, background_tasks: BackgroundTasks, service: Annotated[MachineState, Depends()]):
    background_tasks.add_task(process_webhook_payload, service, message_api, "TELEGRAM")
    
    return {"status": "ok"}


@chat_router.post("/whatsapp", tags=["Webhook"], summary="Rota de webhook para atualizações pela API do Whatsapp", description="Essa rota é responsável por receber as atualizações do sistema através da API oficial do Whatsapp, utilizando uma lógica de webhook.")
async def whatsapp_receiver(message_api: WebhookWhatsapp, background_tasks: BackgroundTasks,service: Annotated[MachineState, Depends()]):
    background_tasks.add_task(process_webhook_payload, service, message_api, "WHATSAPP")
    
    return {"status": "ok"}
    