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
        response_message = "Vazio"
        
        #! Atualizar aqui também
        session = await self.repository.get_full_session(chat_id=chat_id, origin=api_origem)
        history = pass
        
        if not session:
            session = {
                "chat_id": usuario, # Identificação do usuário
                "status": "INICIAL", # Status da etapa
                "origin_service": api, # Serviço de origem
                "context": "", # Contexto dos menus
                "attempts": 0, # Tentativas 
                "updated_at": datetime.now(timezone.utc).isoformat() # Última atualização de registro
            }

            
            #! PRECISA ATUALIZAR PARA O NOVO MÉTODO DO REPOSITORY_REDIS
            logger.info(f"Nova sessão criada para o usuário {usuario} no serviço {api_origem}")
            
        if session["status"] == "INICIAL":
            response_message = "Olá! Bem vindo ao chat de dúvidas e consultas da SEFAZ-RN. Para iniciar o atendimento, escolha uma das opções a baixo para continuar:\n1 - Consulta de Saldo \n2 - Ressarcimento de Contas \n3 - Sistema SIGEF \n4 - Alteração de Contas \n5 - Consulta de CNPJ"
            session["status"] = "AGUARDANDO_OPCAO_1"

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
        
        if api_origem == "TELEGRAM":
            object_message = await self.send_service.send_message_telegram(chat_id=chat_id, message=response_message)

            if not object_message.sucess:
                logger.error(f"Erro ao enviar mensagem para API do {api_origem}. chat_id: {chat_id} | erro: {object_message.message_erro}")
                raise

        else:
            object_message = await self.send_service.send_message_whatsapp(chat_id=chat_id, message=response_message)

            if not object_message.sucess:
                logger.error(f"Erro ao enviar mensagem para API do {api_origem}. chat_id: {chat_id} | erro: {object_message.message_erro}")
                raise

        if(len(session["history"]) > 20):
                session["history"].pop(0)

        session["history"].append(response_message)
