import datetime
from pydantic import BaseModel, Field
from typing import Annotated
from .enum import Status

class UserSession(BaseModel):
    chat_id: Annotated[str, Field(..., description="Identificação do usuário")]
    status: Annotated[Status, Field(..., description="Etapa da máquina de estados na qual o usuário se encontra")]
    origin_service: Annotated[str, Field(..., description="Serviço de mensagem pelo qual o usuário envio a mensagem")]
    context: Annotated[str, Field(default=None, description="Contexto de menus")]
    attempts: Annotated[int, Field(default=0, description="Número de erros do usuário")]
    updated_at: Annotated[datetime.datetime, Field(default=None, description="Última atualização do usuário")]

class MessageElement(BaseModel):
    role: Annotated[str, Field(..., description="Quem enviou a mensagem")]
    message: Annotated[str, Field(..., description="Mensagem enviada")]

class FullSession(BaseModel):
    session: Annotated[UserSession, Field(..., description="Sessão do usuário")]
    history: Annotated[list[MessageElement], Field(..., description="Histórico de mensagens do usuário")]
    