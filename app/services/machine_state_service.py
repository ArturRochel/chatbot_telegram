from loguru import logger
from typing import Annotated
from fastapi import Depends
from app.repositories import RepositoryRedis
from datetime import datetime, timezone
from .message_send_service import MessageSendService
from app.schemas import MessageSendStatus

class MachineState():

    def __init__(self, repository: Annotated[RepositoryRedis, Depends()], send_service: Annotated[MessageSendService, Depends()]):
        self.repository = repository
        self.send_service = send_service

    async def handle_update(self, chat_id: str, message: str, api: str):
        usuario = chat_id # Quem enviou a mensagem
        mensagem = message # O contéudo da mensagem
        api_origem = api # Serviço que enviou a mensagem (Telegram ou Whatsapp)
        
        chave_redis = f"session:{api_origem}:{usuario}"
        
        session = await self.repository.get_session(chave=chave_redis)
        
        if not session:
            session = {
                "chat_id": usuario,
                "status": "INICIAL",
                "service": api,
                "context": "",
                "history": [],
                "attempts": 0,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            await self.repository.save_session(chave=chave_redis, session=session)
            logger.info(f"Nova sessão criada para o usuário {usuario} no serviço {api_origem}")
            
        if session["status"] == "INICIAL":
            response_message = "Olá! Bem vindo ao chat de dúvidas e consultas da SEFAZ-RN. Para iniciar o atendimento, escolha uma das opções a baixo para continuar:\n1 - Consulta de Saldo \n2 - Ressarcimento de Contas \n3 - Sistema SIGEF \n4 - Alteração de Contas \n5 - Consulta de CNPJ"
            session["status"] = "AGUARDANDO_OPCAO_1"

            # todo - Alterar a lógica para evitar repetição, apenas após a mensgem ser decidida, é que o método de envio deve ser chamado
            if api == "TELEGRAM":
                object_message = await self.send_service.send_message_telegram(chat_id=chat_id, message=message)

                if object_message.sucess == False:
                    ...
            else: 
                object_message = await self.send_service.send_message_whatsapp(chat_id=chat_id, message=response_message)

                if object_message.sucess == False:
                    ...
        elif session["status"] == "AGUARDANDO_OPCAO_1":
            if mensagem == "1":
                response_message = "Você escolheu a opção de Consulta de NFE. Por favor, envie o número da NFE que deseja consultar."
                session["status"] = "AGUARDANDO_NUMERO_NFE"
            elif mensagem == "2":
                response_message = "Você escolheu a opção de Consulta de CNPJ. Por favor, envie o número do CNPJ que deseja consultar."
                session["status"] = "AGUARDANDO_NUMERO_CNPJ"
            elif mensagem == "3":
                response_message = "Você escolheu a opção de Ajustes SIGEFE. Por favor, descreva o ajuste que deseja realizar."
                session["status"] = "AGUARDANDO_DESCRICAO_AJUSTE"
            elif mensagem == "4":
                response_message = "Você escolheu a opção de falar com um atendente. Por favor, aguarde enquanto conectamos você com um atendente disponível."
                session["status"] = "AGUARDANDO_ATENDENTE"
            else:
                response_message = "Opção inválida. Por favor, escolha uma das opções abaixo:\n1 - Consulta de NFE\n2 - Consulta de CNPJ\n3 - Ajustes SIGEFE\n4 - Falar com um atendente"