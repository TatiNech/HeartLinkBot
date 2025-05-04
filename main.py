import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import openai

# 🔐 Вставь свой OpenAI API-ключ
openai.api_key = ""

# 🔐 Вставь свой Telegram API-токен
TELEGRAM_TOKEN = "8012584442:AAH06Upa6h22SrB1mrgFgcrwrPbAy_J0thk"

# Логирование
logging.basicConfig(level=logging.INFO)

# Храним, в каком режиме пользователь (ИИ или обычный)
user_ai_mode = {}

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [
        ['🙋‍♀️ Я волонтёр', '🆘 Мне нужна помощь'],
        ['🤖 Задать вопрос ИИ', '📖 О проекте']
    ]
    await update.message.reply_text(
        "Добро пожаловать в HeartLink 💜\nВыберите, что вам интересно:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    )

# Обработка всех сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.lower()

    # Режим общения с ИИ
    if user_ai_mode.get(user_id):
        if 'стоп' in text or 'выход' in text:
            user_ai_mode[user_id] = False
            await update.message.reply_text("🔚 Вы вышли из режима общения с ИИ.")
            return

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": update.message.text}]
            )
            await update.message.reply_text(response.choices[0].message.content)
        except Exception as e:
            logging.error(e)
            await update.message.reply_text("❌ Ошибка при обращении к ИИ. Попробуйте позже.")
        return

    # Кнопка: Я волонтёр
    if 'волонтёр' in text:
        await update.message.reply_text(
            "💜 Спасибо, что выбрали путь добрых дел!\n\n"
            "Вы зарегистрировались как волонтёр 💪\n\n"
            "Вместе мы сможем:\n"
            "— помогать тем, кто в этом нуждается,\n"
            "— участвовать в экологических и социальных акциях,\n"
            "— развивать навыки и заводить новых друзей!\n\n"
            "📄 Заполни форму волонтера:\nhttps://forms.gle/UESqhq5SXRwbYieF6\n"
            "📢 Следи за событиями в Telegram-канале:\nhttps://t.me/+IOpcx4LXebFjNDk6"
        )

    # Кнопка: Мне нужна помощь
    elif 'нужна помощь' in text or 'помощь' in text:
        await update.message.reply_text(
            "💜 Спасибо, что выбрали путь добрых дел!\n\n"
            "Вы можете задать свой вопрос в Telegram-канале:\n"
            "https://t.me/+IOpcx4LXebFjNDk6\n\n"
            "📞 Контакты — тот же канал."
        )

    # Кнопка: О проекте
    elif 'о проекте' in text:
        await update.message.reply_text(
            "💡 *О проекте HeartLink*\n\n"
            "HeartLink — это приложение, которое делает волонтёрство доступным и понятным для всех. "
            "Сегодня многие хотят помогать, но не знают, с чего начать. Мы решаем эту проблему!\n\n"
            "🔹 HeartLink подбирает события под интересы волонтёра\n"
            "🔹 Упрощает регистрацию и отслеживает вклад\n"
            "🔹 Встроен личный профиль с достижениями и статистикой\n\n"
            "С HeartLink помогать проще, удобнее и вдохновляюще ✨"
        )

    # Кнопка: Задать вопрос ИИ
    elif 'ии' in text or '🤖' in text:
        user_ai_mode[user_id] = True
        await update.message.reply_text(
            "🧠 Можешь задать любой вопрос — я постараюсь помочь!\n\n"
            "Напиши *«стоп»*, чтобы выйти из режима общения с ИИ."
        )

    # Любой другой текст
    else:
        await update.message.reply_text("Выберите вариант из меню или нажмите /start.")

# Запуск
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Бот запущен!")
    app.run_polling()

if __name__ == '__main__':
    main()
