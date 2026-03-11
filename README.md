# Chatbot Multiplataforma (Telegram & WhatsApp)

Este projeto consiste em um sistema de chatbot assíncrono desenvolvido com **FastAPI**, projetado para operar tanto no Telegram quanto no WhatsApp. O sistema utiliza uma arquitetura de **Máquina de Estados** para gerenciar o fluxo de conversas e **Redis** para a persistência de sessões e histórico.

## 🛠️ Tecnologias e Dependências

O projeto utiliza as seguintes bibliotecas principais:
* **FastAPI**: Framework web para os endpoints de webhook.
* **Redis (aioredis)**: Armazenamento assíncrono de sessões e histórico.
* **Pydantic & Pydantic-settings**: Validação de dados e gerenciamento de configurações via variáveis de ambiente.
* **Loguru**: Sistema de logging para monitoramento de eventos.
* **Httpx**: Cliente HTTP assíncrono para comunicação com as APIs das plataformas.

## 🧠 Arquitetura do Sistema

### 1. Máquina de Estados (State Machine)
A lógica de conversação é centralizada no `MachineState` (`app/services/machine_state_service.py`). Ele identifica o estado atual do usuário (ex: `INICIAL`, `MENU`) e processa a mensagem recebida para determinar a próxima ação e resposta.

### 2. Gestão de Sessão com Redis
As informações do usuário são persistidas no Redis através da classe `RepositoryRedis` (`app/repositories/repository_redis.py`):
* **Sessão**: Armazena dados contextuais, status da etapa, serviço de origem e tentativas.
* **Histórico**: Mantém as últimas 20 mensagens trocadas para preservar o contexto da conversa.
* **TTL (Time to Live)**: As sessões e históricos são configurados para expirar automaticamente após 24 horas (86.400 segundos).