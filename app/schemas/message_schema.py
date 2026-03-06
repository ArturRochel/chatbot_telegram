from pydantic import BaseModel, Field
from typing import Annotated

class MessageSendStatus(BaseModel):
    sucess: Annotated[bool, Field(default=False,description="Campo responsável por indicar se a mensagem foi enviada")]
    message_erro: Annotated[str | None, Field(default= None, description="Mensagem de erro ou descrição da exceção, caso haja")]
    chat_id: Annotated[str, Field(..., description="Usuário que deve receber a mensagem")]