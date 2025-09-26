import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# Настройки
BOT_TOKEN = "8081060276:AAER7c-zg47MsVVGJM-ZqnNl_CIUQ3_JN88"
CHANNEL_ID = "-1003016125655"  # Ваш канал

# Ваши гайды
GUIDES = {
    "stress": "https://docs.google.com/document/d/1CTjVagsMdjiCUng9jFgyOW9qnahrFqDAQs752",
    "sleep": "https://drive.google.com/ваша-ссылка-на-гайд-2", 
    "anxiety": "https://drive.google.com/ваша-ссылка-на-гайд-3"
}

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# Клавиатура с гайдами
def guides_keyboard():
    buttons = []
    for guide_name in GUIDES:
        # Красивые названия для кнопок
        pretty_names = {
            "stress": "🧘‍♀️ Гайд по стрессу",
            "sleep": "😴 Гайд по сну", 
            "anxiety": "😰 Гайд по тревоге"
        }
        buttons.append(InlineKeyboardButton(
            text=pretty_names[guide_name], 
            callback_data=f"guide_{guide_name}"
        ))
    return InlineKeyboardMarkup(resize_keyboard=True).add(*buttons)

# Клавиатура для проверки подписки
def check_subscription_keyboard(guide_name):
    return InlineKeyboardMarkup(resize_keyboard=True).add(
        InlineKeyboardButton("🔍 Проверить подписку", callback_data=f"check_{guide_name}"),
        InlineKeyboardButton("📢 Подписаться на канал", url=f"https://t.me/{CHANNEL_ID[1:]}")
    )

# Шаг 1. Старт
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(
        '👋 Привет! Я бот для получения психологических гайдов.\n\n'
        'Выберите гайд который вас интересует:',
        reply_markup=guides_keyboard()
    )

# Шаг 2. Выбор гайда
@dp.callback_query_handler(lambda c: c.data.startswith('guide_'))
async def choose_guide(callback: types.CallbackQuery):
    guide_name = callback.data.replace('guide_', '')
    
    # Сразу проверяем подписку
    user_id = callback.from_user.id
    is_subscribed = await check_subscription(user_id)
    
    if is_subscribed:
        # Если подписан - сразу даем гайд
        guide_url = GUIDES[guide_name]
        await callback.message.edit_text(
            f'🎉 Вот ваш гайд!\n\n'
            f'📚 {guide_url}\n\n'
            'Приятного изучения! 💫',
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("📖 Открыть гайд", url=guide_url)
            )
        )
    else:
        # Если не подписан - просим подписаться
        guide_title = {
            "stress": "🧘‍♀️ Гайд по борьбе со стрессом",
            "sleep": "😴 Гайд по улучшению сна",
            "anxiety": "😰 Гайд по снижению тревоги"
        }
        
        await callback.message.edit_text(
            f'❌ Для получения гайда нужно подписаться на канал!\n\n'
            f'📚 {guide_title[guide_name]}\n\n'
            'Подпишитесь на канал и нажмите "Проверить подписку":',
            reply_markup=check_subscription_keyboard(guide_name)
        )

# Шаг 3. Проверка подписки
@dp.callback_query_handler(lambda c: c.data.startswith('check_'))
async def check_subscription_handler(callback: types.CallbackQuery):
    guide_name = callback.data.replace('check_', '')
    user_id = callback.from_user.id
    
    is_subscribed = await check_subscription(user_id)
    
    if is_subscribed:
        # Подписан - выдаем гайд
        guide_url = GUIDES[guide_name]
        await callback.message.edit_text(
            f'✅ Отлично! Вы подписаны!\n\n'
            f'🎉 Вот ваш гайд:\n{guide_url}\n\n'
            'Приятного изучения! 📖',
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("📖 Открыть гайд", url=guide_url)
            )
        )
    else:
        # Не подписан - просим подписаться
        await callback.answer(
            '❌ Вы еще не подписались на канал! Подпишитесь и попробуйте снова.', 
            show_alert=True
        )

# Функция проверки подписки
async def check_subscription(user_id):
    try:
        chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except:
        return False

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)

