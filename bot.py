import os
import logging
from flask import Flask, request
import requests

# Настройки
BOT_TOKEN = "8081060276:AAER7c-zg47MsVVGJM-ZqnNl_CIUQ3_JN88"
CHANNEL_ID = "-1003016125655"

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def check_subscription(user_id):
    """Проверка подписки на канал"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
        data = {"chat_id": CHANNEL_ID, "user_id": user_id}
        response = requests.post(url, data=data).json()
        
        if response["ok"]:
            status = response["result"]["status"]
            return status in ["member", "administrator", "creator"]
        return False
    except:
        return False

@app.route('/webapp')
def webapp():
    """Web App только проверяет подписку"""
    # Получаем ID пользователя из Telegram
    init_data = request.args.get('tgWebAppData', '')
    user_id = None
    
    if init_data:
        try:
            from urllib.parse import parse_qs
            params = parse_qs(init_data)
            user_data = params.get('user', [None])[0]
            if user_data:
                import json
                user = json.loads(user_data)
                user_id = user['id']
        except:
            pass

    if not user_id:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ошибка</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { 
                    font-family: Arial; padding: 20px; text-align: center;
                    background: #667eea; color: white; min-height: 100vh;
                    display: flex; flex-direction: column; justify-content: center;
                }
                .container { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; }
                .button { background: white; color: #667eea; padding: 15px 30px; 
                         text-decoration: none; border-radius: 25px; display: inline-block; margin: 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>🚫 Ошибка</h2>
                <p>Откройте через кнопку в канале</p>
                <a href="https://t.me/nellly_psy" class="button">Перейти в канал</a>
            </div>
        </body>
        </html>
        """

    # Проверяем подписку
    is_subscribed = check_subscription(user_id)

    if not is_subscribed:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Подписка требуется</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { 
                    font-family: Arial; padding: 20px; text-align: center;
                    background: #ff6b6b; color: white; min-height: 100vh;
                    display: flex; flex-direction: column; justify-content: center;
                }
                .container { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; }
                .button { background: white; color: #ff6b6b; padding: 15px 30px; 
                         text-decoration: none; border-radius: 25px; display: inline-block; margin: 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>📢 Подпишитесь на канал</h2>
                <p>Чтобы получить гайд, нужно быть подписанным</p>
                <a href="https://t.me/nellly_psy" class="button" target="_blank">Подписаться</a>
                <p>После подписки закройте окно и нажмите на кнопку снова</p>
            </div>
        </body>
        </html>
        """
    else:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Гайд доступен</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { 
                    font-family: Arial; padding: 20px; text-align: center;
                    background: #00b894; color: white; min-height: 100vh;
                    display: flex; flex-direction: column; justify-content: center;
                }
                .container { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; }
                .emoji { 
                    font-size: 60px; margin: 20px; cursor: pointer;
                    transition: transform 0.3s; 
                }
                .emoji:hover { transform: scale(1.2); }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>🎉 Гайд доступен!</h2>
                <p>Ссылка на гайд находится в посте под этим сообщением</p>
                <div class="emoji" onclick="alert('Ссылка в посте над кнопкой!')">
                    📚
                </div>
                <p>Нажмите на 📚 чтобы увидеть напоминание</p>
            </div>
        </body>
        </html>
        """

@app.route('/')
def home():
    return "Бот работает!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
