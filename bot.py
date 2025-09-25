import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройки
BOT_TOKEN = "8081060276:AAER7c-zg47MsVVGJM-ZqnNl_CIUQ3_JN88"
CHANNEL_ID = "-1003016125655"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def check_subscription(user_id, bot):
    """Проверка подписки на канал"""
    try:
        chat_member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logging.error(f"Ошибка проверки подписки: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    # Проверяем подписку
    is_subscribed = await check_subscription(user.id, context.bot)
    
    if is_subscribed:
        # Подписан - выдаем гайд
        keyboard = [
            [InlineKeyboardButton("📚 Получить гайд", callback_data="get_guide")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"✅ Привет, {user.first_name}! Вы подписаны на канал!\n\n"
            "Нажмите кнопку ниже чтобы получить гайд:",
            reply_markup=reply_markup
        )
    else:
        # Не подписан - просим подписаться
        keyboard = [
            [InlineKeyboardButton("📢 Подписаться на канал", url="https://t.me/nellly_psy")],
            [InlineKeyboardButton("🔍 Проверить подписку", callback_data="check_subscription")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "📚 Чтобы получить гайд, нужно подписаться на наш канал!\n\n"
            "После подписки нажмите 'Проверить подписку':",
            reply_markup=reply_markup
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == "check_subscription":
        is_subscribed = await check_subscription(user_id, context.bot)
        
        if is_subscribed:
            keyboard = [[InlineKeyboardButton("📚 Получить гайд", callback_data="get_guide")]]
            await query.edit_message_text(
                "✅ Отлично! Теперь вы подписаны!\n\nНажмите чтобы получить гайд:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            keyboard = [
                [InlineKeyboardButton("📢 Подписаться", url="https://t.me/nellly_psy")],
                [InlineKeyboardButton("🔍 Проверить снова", callback_data="check_subscription")]
            ]
            await query.edit_message_text(
                "❌ Вы еще не подписались на канал!\n\nПожалуйста, подпишитесь и проверьте снова:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    elif query.data == "get_guide":
        is_subscribed = await check_subscription(user_id, context.bot)
        
        if is_subscribed:
            # Выдаем гайд
            await query.edit_message_text(
                "🎉 Вот ваш гайд!\n\n"
                "Ссылка: https://drive.google.com/ваша-ссылка-на-гайд\n\n"
                "Приятного изучения! 📖"
            )
        else:
            await query.edit_message_text("❌ Доступ закрыт. Подпишитесь на канал.")

def main():
    """Запуск бота"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
