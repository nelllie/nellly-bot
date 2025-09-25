import logging
import asyncio
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
    """Создает сообщение с кнопкой для канала"""
    keyboard = [
        [InlineKeyboardButton("🎁 Забрать гайд", callback_data="get_guide")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📚 Нажмите кнопку чтобы проверить доступ к гайду:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопки - проверяет подписку"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    # Проверяем подписку
    is_subscribed = await check_subscription(user_id, context.bot)
    
    if not is_subscribed:
        # Не подписан
        keyboard = [
            [InlineKeyboardButton("📢 Подписаться на канал", url="https://t.me/nellly_psy")],
            [InlineKeyboardButton("🔍 Проверить подписку", callback_data="get_guide")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "❌ Чтобы получить гайд, нужно подписаться на канал!\n\n"
            "После подписки нажмите 'Проверить подписку':",
            reply_markup=reply_markup
        )
    else:
        # Подписан - выдаем инструкцию
        await query.edit_message_text(
            "✅ Вы подписаны! Гайд доступен!\n\n"
            "📚 Ссылка на гайд находится в посте над этим сообщением\n\n"
            "Найдите ссылку в тексте поста и нажмите на нее!",
            reply_markup=None
        )

def main():
    """Запуск бота"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    application.run_polling()

if __name__ == "__main__":
    main()
