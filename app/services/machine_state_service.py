from loguru import logger
from typing import Annotated
from fastapi import Depends
from app.repositories import RepositoryRedis
from datetime import datetime, timezone
from .message_send_service import MessageSendService
from app.utils import MENU_INICIAL, LIMITE_TENTATIVAS, OPCAO_INVALIDA_MENU
from app.schemas import (FullSession, MessageElement, UserSession, Status, TypeUser, OriginService)

# todo - ADIÇÃO DE CONTEXTO 
# todo - CADASTRAR BOT
# todo - IMPLEMENTAR NGROK
# todo - TESTAR COM API OFICIAL

class MachineState():

    def __init__(self, repository: Annotated[RepositoryRedis, Depends()], send_service: Annotated[MessageSendService, Depends()]):
        self.repository = repository
        self.send_service = send_service

    async def handle_update(self, chat_id: str, message: str, origin_service: OriginService) -> None:

        session_and_history = await self._get_or_create_session(chat_id=chat_id, origin_service=origin_service)

        session = session_and_history.session
        history = session_and_history.history

        history.append(MessageElement(role=TypeUser.USER, message=message))

        response_message = self._process_state(session=session, history=history, message=message)

        await self._send_message(chat_id=chat_id, message=response_message, origin_service=origin_service)

        history.append(MessageElement(role=TypeUser.BOT, message=response_message))

        await self.repository.save_session_and_history(chat_id=chat_id, origin=origin_service.value, session_data=session, history_data=history)

    async def _get_or_create_session(self, chat_id: str, origin_service: OriginService) -> FullSession:
        result_session_query = await self.repository.get_session_and_history(chat_id=chat_id, origin=origin_service.value)

        if result_session_query is not None:
            session = result_session_query.session
            history = result_session_query.history
        else:
            session = UserSession(
                chat_id=chat_id,
                status=Status.INICIAL,
                origin_service=origin_service,
                context="",
                attempts=0,
                updated_at=datetime.now(timezone.utc)
            )
            history = []

        return FullSession(session=session, history=history)

    def _process_state(self, session: UserSession, history: list[MessageElement], message: str) -> str | None:
        response_message = "Mensagem inicial"
        
        if session.attempts >= 3:
            session.status = Status.ERRO
            session.attempts = 0
            response_message = f"{LIMITE_TENTATIVAS} \n {MENU_INICIAL}"
            return response_message

        if session.status == Status.INICIAL:
            response_message = MENU_INICIAL
            session.status = Status.AGUARDANDO_OPCAO_1

        elif session.status == Status.AGUARDANDO_OPCAO_1:

            if message == "1":
                response_message = "Você escolheu: Classificação contábil e orçamentária. Por favor, descreva sua dúvida detalhadamente."
                session.status = Status.AGUARDANDO_DUVIDA_CONTABIL
            
            elif message == "2":
                response_message = "Você escolheu: Execução da despesa. Informe o tipo de processo (Empenho, Liquidação, etc) e o número, se houver."
                session.status = Status.AGUARDANDO_DETALHE_DESPESA

            elif message == "3":
                response_message = "Você escolheu: Conciliação Bancária. Por favor, envie o número da Guia de Recebimento (GR) ou descreva o lançamento."
                session.status = Status.AGUARDANDO_CONCILIACAO

            elif message == "4":
                response_message = "Você escolheu: Pagamentos. Informe se a sua dúvida é sobre Preparação de Pagamento (PP) ou Ordem Bancária (OB)."
                session.status = Status.AGUARDANDO_TIPO_PAGAMENTO

            elif message == "5":
                response_message = "Você escolheu: Movimentação financeira/orçamentária. Descreva qual operação deseja consultar (Repasse, Cotas, etc)."
                session.status = Status.AGUARDANDO_MOVIMENTACAO

            elif message == "6":
                response_message = "Você escolheu: Superávit financeiro. Informe se deseja solicitar apuração ou revisão do cálculo."
                session.status = Status.AGUARDANDO_SUPERAVIT

            elif message == "7":
                response_message = "Você escolheu: Retenções. Informe o tributo (INSS, IRRF, ISS) ou se a dúvida é sobre DCTFWeb."
                session.status = Status.AGUARDANDO_RETENCAO

            elif message == "8":
                response_message = "Você escolheu: Almoxarifado. Informe se a dúvida é sobre entrada, saída ou ajustes de itens."
                session.status = Status.AGUARDANDO_ALMOXARIFADO

            elif message == "9":
                response_message = "Você escolheu: Problemas com o SIGEF. Por favor, envie um print do erro ou descreva a funcionalidade com problemas."
                session.status = Status.AGUARDANDO_ERRO_SIGEF

            elif message == "10":
                response_message = "Você escolheu a opção de outra dúvidas. Verifique se é uma dessas: ..."

            else:
                response_message = OPCAO_INVALIDA_MENU
                session.attempts += 1

        elif session.status == Status.AGUARDANDO_PERGUNTA:
            #chamar LLM, passa session e historye e aguardar resposta
            pass

        return response_message

    async def _send_message(self, chat_id: str, message: str, origin_service: OriginService) -> None:
        if origin_service == OriginService.TELEGRAM:
            #object_message = await self.send_service.send_message_telegram(chat_id=chat_id, message=message)
            logger.success(f"{message}")
        else:
            logger.success(f"{message}")
            #object_message = await self.send_service.send_message_whatsapp(chat_id=chat_id, message=message)

        # if not object_message.sucess:
        #     logger.error(f"Erro ao enviar mensagem para API do {origin_service}. chat_id: {chat_id} | erro: {object_message.message_erro}")
        #     raise 