from app.schemas import WebhookTelegram, WebhookWhatsapp

def extract_telegram_data(data: WebhookTelegram):

    return (chat_id, message)

def extract_whatsapp_data(data: WebhookWhatsapp):

    return (chat_id, message)