from fastapi import FastAPI
from app.api.v1.routers import chat_router

app = FastAPI(title="Chatbot Telegram", description="Projeto laboratório para desenvolvimento do chatbot para telegram")

@app.include_router(chat_router)