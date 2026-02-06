from fastapi import APIRouter, Depends
from typing import Annotated
from app.schemas import TelegramUpdateData
from app.services import MachineState

machine_state = Annotated[MachineState, Depends()]
chat_router = APIRouter(prefix="/chat")

@chat_router.post("/", tags=["Webhook"], summary="Rota de webhook para atualizações pela API do sistema de mensagens", description="Essa rota é responsável por receber as atualizações do sistema mensageiros, utilizando uma lógica de webhook.")
async def message_receiver(message_api: TelegramUpdateData, service: machine_state):
    pass