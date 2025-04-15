
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Вставь сюда свой API-токен от BotFather
TELEGRAM_TOKEN = 'PASTE_YOUR_TOKEN_HERE'

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['🙋‍♀️ I am a volunteer', '🆘 I need help']]
    await update.message.reply_text(
        "Welcome to HeartLink 💜\nChoose an option below to get started:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )

# Обработка выбора
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if 'volunteer' in user_text.lower():
        await update.message.reply_text("Great! We’ll connect you to volunteer projects soon 🌱")
    elif 'help' in user_text.lower():
        await update.message.reply_text("No worries! Tell us more about what you need, and we’ll guide you 💬")
    else:
        await update.message.reply_text("Please choose one of the options to continue.")

# Основной запуск бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
