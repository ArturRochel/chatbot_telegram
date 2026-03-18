from loguru import logger
from typing import Annotated
from fastapi import Depends
from app.repositories import RepositoryRedis
from datetime import datetime, timezone
from .message_send_service import MessageSendService
from app.schemas import MessageElement, UserSession
from app.utils import MENU_INICIAL, LIMITE_TENTATIVAS, OPCAO_INVALIDA_MENU

# todo - ADIÇÃO DE CONTEXTO 
# todo - CADASTRAR BOT
# todo - IMPLEMENTAR NGROK
# todo - TESTAR COM API OFICIAL

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
              
        if session.attempts >= 3:
                session.status = "INICIAL"
                session.attempts = 0

                response_erro = f"{LIMITE_TENTATIVAS} \n {MENU_INICIAL}"

                #! Enviar mensagem para o usuário
                # object_message = await self.send_service.send_message_telegram(chat_id=chat_id, message=response_erro)

                # if not object_message.sucess:
                #     logger.error(f"Erro ao enviar mensagem para API do {origin_service}. chat_id: {chat_id} | erro: {object_message.message_erro}")
                #     raise

                history.append(MessageElement(role="bot", message=response_erro))
                await self.repository.save_session_and_history(chat_id=chat_id, origin=origin_service, session_data=session, history_data=history)  

                return



        if session.status == "INICIAL":
            response_message = MENU_INICIAL
            session.status = "AGUARDANDO_OPCAO_1"

        elif session.status == "AGUARDANDO_OPCAO_1":

            if message == "1":
                response_message = "Você escolheu: Classificação contábil e orçamentária. Por favor, descreva sua dúvida detalhadamente."
                session.status = "AGUARDANDO_DUVIDA_CONTABIL"
            
            elif message == "2":
                response_message = "Você escolheu: Execução da despesa. Informe o tipo de processo (Empenho, Liquidação, etc) e o número, se houver."
                session.status = "AGUARDANDO_DETALHE_DESPESA"

            elif message == "3":
                response_message = "Você escolheu: Conciliação Bancária. Por favor, envie o número da Guia de Recebimento (GR) ou descreva o lançamento."
                session.status = "AGUARDANDO_CONCILIACAO"

            elif message == "4":
                response_message = "Você escolheu: Pagamentos. Informe se a sua dúvida é sobre Preparação de Pagamento (PP) ou Ordem Bancária (OB)."
                session.status = "AGUARDANDO_TIPO_PAGAMENTO"

            elif message == "5":
                response_message = "Você escolheu: Movimentação financeira/orçamentária. Descreva qual operação deseja consultar (Repasse, Cotas, etc)."
                session.status = "AGUARDANDO_MOVIMENTACAO"

            elif message == "6":
                response_message = "Você escolheu: Superávit financeiro. Informe se deseja solicitar apuração ou revisão do cálculo."
                session.status = "AGUARDANDO_SUPERAVIT"

            elif message == "7":
                response_message = "Você escolheu: Retenções. Informe o tributo (INSS, IRRF, ISS) ou se a dúvida é sobre DCTFWeb."
                session.status = "AGUARDANDO_RETENCAO"

            elif message == "8":
                response_message = "Você escolheu: Almoxarifado. Informe se a dúvida é sobre entrada, saída ou ajustes de itens."
                session.status = "AGUARDANDO_ALMOXARIFADO"

            elif message == "9":
                response_message = "Você escolheu: Problemas com o SIGEF. Por favor, envie um print do erro ou descreva a funcionalidade com problemas."
                session.status = "AGUARDANDO_ERRO_SIGEF"

            elif message == "10":
                response_message = "Você escolheu a opção de outra dúvidas. Verifique se é uma dessas: ..."

            else:
                response_message = OPCAO_INVALIDA_MENU
                session.attempts += 1

        elif session.status == "ERRO":
            response_message = "Por favor, informe uma das opções disponíveis para que eu possa lhe ajudar."
            session.attempts += 1

        else:
            session.attempts += 1
            response_message = "Opção inválida. Por favor, escolha um número de 1 a 10 conforme o menu inicial."
        
        if origin_service == "TELEGRAM":
            logger.success(f"Mensagem Usuário: {message} | Resposta Bot: {response_message}")
            # object_message = await self.send_service.send_message_telegram(chat_id=chat_id, message=response_message)

            # if not object_message.sucess:
            #     logger.error(f"Erro ao enviar mensagem para API do {origin_service}. chat_id: {chat_id} | erro: {object_message.message_erro}")
            #     raise

        else:
            object_message = await self.send_service.send_message_whatsapp(chat_id=chat_id, message=response_message)

            if not object_message.sucess:
                logger.error(f"Erro ao enviar mensagem para API do {origin_service}. chat_id: {chat_id} | erro: {object_message.message_erro}")
                raise

        history.append(MessageElement(role="bot", message=response_message))
        await self.repository.save_session_and_history(chat_id=chat_id, origin=origin_service, session_data=session, history_data=history)

