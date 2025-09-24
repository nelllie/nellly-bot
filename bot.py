import os
import logging
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройки
BOT_TOKEN = "8081060276:AAER7c-zg47MsVVGJM-ZqnNl_CIUQ3_JN88"  # Замените на токен бота
CHANNEL_ID = "-1003016125655"  # Замените на ID канала (например -1001234567890)

# Ваши гайды
GUIDES = {
    "stress": {
        "title": "📚 Гайд по борьбе со стрессом",
        "url": "https://telegra.ph/Ваш-гайд-01",
        "description": "Эффективные техники для снижения стресса"
    },
    "sleep": {
        "title": "😴 Гайд по улучшению сна", 
        "url": "https://telegra.ph/Ваш-гайд-02",
        "description": "Как наладить здоровый сон"
    }
}

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def check_subscription(user_id, bot):
    """Проверка подписки на канал"""
    try:
        chat_member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except:
        return False

@app.route('/webapp/<guide_name>')
def webapp(guide_name):
    """Web App для выдачи гайдов"""
    guide = GUIDES.get(guide_name)
    if not guide:
        return jsonify({"error": "Гайд не найден"})
    
    # HTML страница для Web App
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{guide['title']}</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; text-align: center; }}
            .button {{ background: #2481cc; color: white; padding: 15px 30px; 
                     text-decoration: none; border-radius: 10px; display: inline-block; margin: 10px; }}
        </style>
    </head>
    <body>
        <h2>{guide['title']}</h2>
        <p>{guide['description']}</p>
        <a href="{guide['url']}" class="button" target="_blank">📖 Открыть гайд</a>
        <p><small>Закройте это окно чтобы вернуться в Telegram</small></p>
    </body>
    </html>
    """
    return html

@app.route('/')
def home():
    return "Бот работает!"

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Установка webhook (вызовете этот URL один раз)"""
    return "Webhook будет установлен позже"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)