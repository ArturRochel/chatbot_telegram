from loguru import logger
from typing import Annotated
from fastapi import Depends
from app.repositories import RepositoryRedis
from datetime import datetime, timezone
from .message_send_service import MessageSendService
from app.schemas import MessageElement, FullSession, UserSession

class MachineState():

    def __init__(self, repository: Annotated[RepositoryRedis, Depends()], send_service: Annotated[MessageSendService, Depends()]):
        self.repository = repository
        self.send_service = send_service

    async def handle_update(self, chat_id: str, message: str, origin_service: str):
        response_message = "Vazio"
        
        result_session_query = await self.repository.get_session_and_history(chat_id=chat_id, origin=origin_service) 

        if result_session_query is not None:
            session = result_session_query.session
            history = result_session_query.history

            history.append(MessageElement(role="user", message=message))
        else:
            session = UserSession(
                chat_id=chat_id,
                status="INICIAL",
                origin_service=origin_service,
                context="",
                attempts=0,
                updated_at=datetime.now(timezone.utc)
            )
        
            history = [MessageElement(role="user", message=message)]
              
            
        if session.status == "INICIAL":
            response_message = "Olá! Bem vindo ao chat de dúvidas e consultas da SEFAZ-RN. Para iniciar o atendimento, escolha uma das opções a baixo para continuar:\n1 - Consulta de Saldo \n2 - Ressarcimento de Contas \n3 - Sistema SIGEF \n4 - Alteração de Contas \n5 - Consulta de CNPJ"
            session.status = "AGUARDANDO_OPCAO_1"

        elif session.status == "AGUARDANDO_OPCAO_1":
            if message == "1":
                response_message = "Você escolheu a opção de Consulta de NFE. Por favor, envie o número da NFE que deseja consultar."
                session.status = "AGUARDANDO_NUMERO_NFE"
            elif message == "2":
                response_message = "Você escolheu a opção de Consulta de CNPJ. Por favor, envie o número do CNPJ que deseja consultar."
                session.status = "AGUARDANDO_NUMERO_CNPJ"
            elif message == "3":
                response_message = "Você escolheu a opção de Ajustes SIGEFE. Por favor, descreva o ajuste que deseja realizar."
                session.status = "AGUARDANDO_DESCRICAO_AJUSTE"
            elif message == "4":
                response_message = "Você escolheu a opção de falar com um atendente. Por favor, aguarde enquanto conectamos você com um atendente disponível."
                session.status = "AGUARDANDO_ATENDENTE"
            else:
                response_message = "Opção inválida. Por favor, escolha uma das opções abaixo:\n1 - Consulta de NFE\n2 - Consulta de CNPJ\n3 - Ajustes SIGEFE\n4 - Falar com um atendente"
        
        if origin_service == "TELEGRAM":
            object_message = await self.send_service.send_message_telegram(chat_id=chat_id, message=response_message)

            if not object_message.sucess:
                logger.error(f"Erro ao enviar mensagem para API do {origin_service}. chat_id: {chat_id} | erro: {object_message.message_erro}")
                raise

        else:
            object_message = await self.send_service.send_message_whatsapp(chat_id=chat_id, message=response_message)

            if not object_message.sucess:
                logger.error(f"Erro ao enviar mensagem para API do {origin_service}. chat_id: {chat_id} | erro: {object_message.message_erro}")
                raise

        history.append(MessageElement(role="bot", message=response_message))
        await self.repository.save_session_and_history(chat_id=chat_id, origin=origin_service, session_data=session, history_data=history)

