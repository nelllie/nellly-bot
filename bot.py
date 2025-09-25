from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает! Используйте /webapp для проверки доступа"

@app.route('/webapp')
def webapp():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Проверка подписки</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                padding: 20px; 
                text-align: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                margin: 0;
            }
            .container { 
                background: rgba(255,255,255,0.1); 
                padding: 40px; 
                border-radius: 15px; 
                backdrop-filter: blur(10px);
                max-width: 90%;
                margin: 0 auto;
            }
            .button { 
                background: #ff6b6b; 
                color: white; 
                padding: 15px 30px; 
                text-decoration: none; 
                border-radius: 25px; 
                display: inline-block; 
                margin: 15px 0;
                font-weight: bold;
                border: none;
                cursor: pointer;
            }
            .emoji { 
                font-size: 48px; 
                margin: 20px 0;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔐 Проверка доступа к гайду</h2>
            <p>Эта функция скоро будет доступна</p>
            <div class="emoji">📚</div>
            <p>Нажмите на кнопку для проверки подписки:</p>
            <button class="button" onclick="checkSubscription()">Проверить подписку</button>
        </div>
        
        <script>
            function checkSubscription() {
                alert('Функция проверки подписки скоро будет добавлена!');
            }
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
