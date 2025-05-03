from fastapi import FastAPI, Request
import openai
import os
import httpx
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

load_dotenv()

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("8012584442:AAH06Upa6h22SrB1mrgFgcrwrPbAy_J0thk")
OPENAI_API_KEY = os.getenv("")
BOT_API_URL = f"https://api.telegram.org/bot{8012584442:AAH06Upa6h22SrB1mrgFgcrwrPbAy_J0thk}"

openai.api_key = OPENAI_API_KEY

# Функция для общения с OpenAI
async def ask_ai(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "❌ Ошибка при обращении к ИИ."

# Функция отправки сообщения в Telegram
async def send_message(chat_id: int, text: str):
    async with httpx.AsyncClient() as client:
        await client.post(f"{BOT_API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": text
        })

# Главный обработчик вебхука
@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()

    message = data.get("message")
    if not message:
        return JSONResponse(content={"ok": True})

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        welcome_text = (
            "Добро пожаловать в HeartLink 💜\n\n"
            "Выберите действие:\n"
            "🙋‍♀️ Я волонтёр\n🆘 Мне нужна помощь\n📖 О проекте\n🤖 Поговорить с ИИ"
        )
        await send_message(chat_id, welcome_text)

    elif "волонтёр" in text.lower():
        reply = (
            "Спасибо, что выбрали путь добрых дел!\n"
            "Вы зарегистрировались как волонтёр 💪\n\n"
            "Вместе мы сможем:\n"
            "— помогать тем, кто в этом нуждается,\n"
            "— участвовать в экологических и социальных акциях,\n"
            "— развивать навыки и заводить новых друзей!\n\n"
            "📋 Заполни форму волонтёра: https://forms.gle/UESqhq5SXRwbYieF6\n"
            "📢 Следи за событиями: https://t.me/+IOpcx4LXebFjNDk6"
        )
        await send_message(chat_id, reply)

    elif "помощь" in text.lower():
        reply = (
            "Спасибо, что выбрали путь добрых дел!\n"
            "Вы можете задать ваш вопрос в Telegram-канале:\n"
            "https://t.me/+IOpcx4LXebFjNDk6"
        )
        await send_message(chat_id, reply)

    elif "о проекте" in text.lower():
        about = (
            "HeartLink — это приложение, которое делает волонтёрство доступным и понятным для всех.\n\n"
            "Сегодня многие хотят помогать, но не знают, где найти подходящие мероприятия или с чего начать.\n"
            "Мы решаем эту проблему: HeartLink подбирает события под твои интересы, упрощает регистрацию и показывает твой вклад.\n"
            "Больше никаких сложных списков и пропущенных возможностей — всё самое важное всегда под рукой.\n\n"
            "В приложении есть личный профиль волонтёра, статистика участия и система достижений, которые мотивируют расти и продолжать делать добро.\n\n"
            "С HeartLink помогать становится проще, удобнее и по-настоящему."
        )
        await send_message(chat_id, about)

    elif "ии" in text.lower() or "🤖" in text:
        await send_message(chat_id, "Напиши свой вопрос, и я передам его ИИ 💬")

    else:
        ai_response = await ask_ai(text)
        await send_message(chat_id, ai_response)

    return JSONResponse(content={"ok": True})
