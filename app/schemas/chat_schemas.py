from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from datetime import datetime

class UseSession(BaseModel):
    chat_id: Annotated[str, Field(description="Identificador do usuário enviado pela API Oficial do serviço")]
    status: Annotated[str, Field(description="Status da etapa na qual o usuário se encontra dentro do processo")]
    context: Annotated[str, Field(description="Contexto da conversa com o ChatBot")]
    history: Annotated[list, Field(description="Histórico das últimas 10 mensagens da conversa")]
    attempts: Annotated[int, Field(description="Número de erros provacados pelo usuário ao enviar uma mensagem fora do padrão aguardado")]
    updated_at: Annotated[datetime, Field(description="Data e hora de quando aconteceu a ultima atualização de status")] 

class ChatTelegram(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: Annotated[int | str, Field(description="Identificador do chat")]
    
class MessageTelegram(BaseModel):
    model_config = ConfigDict(extra="ignore")
    chat: Annotated[ChatTelegram, Field(..., description="Objeto com as informações do chat")]
    text: Annotated[str | None, Field(None, description="Texto da mensagem")]
    message_id: int | None
    
class WebhookTelegram(BaseModel):
    model_config = ConfigDict(extra='ignore')
    message: Annotated[MessageTelegram, Field(..., description="Dados da mensagem")]

class SaidaTelegram(BaseModel):
    chat_id: Annotated[str, Field(..., description="Identificação do chat para o qual o bot vai responder.")]
    text: Annotated[str, Field(..., description="Texto da mensagem enviada")]

class TextoWhatsApp(BaseModel):
    body: Annotated[str, Field(..., description="Corpo do texto da mensagem")]

class SaidaWhatsApp(BaseModel):
    messaging_product: Annotated[str, Field(default="whatsapp", description="Produto de mensageria")]
    to: Annotated[str, Field(..., description="Número de destino")]
    type: Annotated[str, Field(default="text", description="Tipo de mensagem")]
    text: Annotated[TextoWhatsApp, Field(..., description="Objeto contendo o texto")]

class TextBodyWpp(BaseModel):
    body: str

class MessageWpp(BaseModel):
    from_number: Annotated[str, Field(alias="from", description="Número de quem enviou")]
    text: TextBodyWpp

class ValueWpp(BaseModel):
    messages: Annotated[list[MessageWpp] | None, Field(default=None, description="Campo com as mensagens do JSON enviado pelo Whatsapp")]

class ChangeWpp(BaseModel):
    value: ValueWpp

class EntryWpp(BaseModel):
    id: str
    changes: list[ChangeWpp]

class WebhookWhatsapp(BaseModel):
    object: str
    entry: Annotated[EntryWpp, Field(..., description="Objeto contendo as informações de mudanças e mensagens.")]