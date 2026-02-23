from app.schemas import WebhookTelegram, WebhookWhatsapp

def extract_telegram_data(data: WebhookTelegram):
    chat_id = data.message.chat.id
    message = data.message.text
    
    return (chat_id, message)

def extract_whatsapp_data(data: WebhookWhatsapp):
    chat_id = data.entry[0].changes[0].value.messages[0].from_number
    message = data.entry[0].changes[0].value.messages[0].text.body
    
    return (chat_id, message)