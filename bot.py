import os
import logging
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройки
BOT_TOKEN = "8081060276:AAER7c-zg47MsVVGJM-ZqnNl_CIUQ3_JN88"
CHANNEL_ID = "-1003016125655"

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
            body {{ 
                font-family: Arial, sans-serif; 
                padding: 20px; 
                text-align: center; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }}
            .container {{
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                max-width: 500px;
            }}
            .button {{ 
                background: #ff6b6b; 
                color: white; 
                padding: 15px 30px; 
                text-decoration: none; 
                border-radius: 25px; 
                display: inline-block; 
                margin: 20px 0;
                font-size: 18px;
                font-weight: bold;
                transition: transform 0.3s;
            }}
            .button:hover {{
                transform: scale(1.05);
            }}
            h2 {{ margin-bottom: 10px; }}
            p {{ font-size: 16px; line-height: 1.5; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>{guide['title']}</h2>
            <p>{guide['description']}</p>
            <a href="{guide['url']}" class="button" target="_blank">📖 Открыть гайд</a>
            <p><small>Закройте это окно чтобы вернуться в Telegram</small></p>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/')
def home():
    return "Бот работает!"

@app.route('/health')
def health():
    return jsonify({"status": "ok", "message": "Bot is running"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
