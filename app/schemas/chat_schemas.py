from pydantic import BaseModel, Field
from typing import Annotated, Optional
from datetime import datetime

class UseSession(BaseModel):
    chat_id: Annotated[str, Field(description="Identificador do usuário enviado pela API Oficial do serviço")]
    status: Annotated[str, Field(description="Status da etapa na qual o usuário se encontra dentro do processo")]
    context: Annotated[str, Field(description="Contexto da conversa com o ChatBot")]
    history: Annotated[list, Field(description="Histórico das últimas 10 mensagens da conversa")]
    attempts: Annotated[int, Field(description="Número de erros provacados pelo usuário ao enviar uma mensagem fora do padrão aguardado")]
    updated_at: Annotated[datetime, Field(description="Data e hora de quando aconteceu a ultima atualização de status")] 
    
class Chat(BaseModel):
    id: Annotated[str, Field(description="Identificar do chat")]
    
class Message(BaseModel):
    chat: Annotated[Chat, Field(description="Objeto com as informações a respeito")]
    text: Annotated[Optional[str], Field(description="Objeto contendo as informações a respeito da mensagem")]
    
class TelegramUpdateData(BaseModel):
    message: Annotated[dict, Field(description="Dados da mensagem")]