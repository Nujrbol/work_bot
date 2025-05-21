import json
from aiogram import Router, types, F
from config import CHANNEL_ID, ADMIN_ID
from utils import is_spam
from pathlib import Path
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

router = Router()

IGNORED_TEXTS = ["/start", "/help", "📢 Опубликовать вакансию", "📬 Поддержка"]

@router.message(F.chat.type == "private")
async def handle_post(message: types.Message):
    user_id = str(message.from_user.id)
    text = message.text or ""

    if text in IGNORED_TEXTS:
        return



BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / "data" / "storage.json"
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

# Создаем файл, если не существует
if not DATA_PATH.exists():
    DATA_PATH.write_text("{}")

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@router.message(F.chat.type == "private")
async def handle_post(message: types.Message):
    user_id = str(message.from_user.id)
    text = message.text or ""

    # Проверка спама
    reason = is_spam(text)
    if reason:
        await message.answer(f"🚫 Отклонено: {reason}")
        return

    db = load_data()

    # Проверка дубликатов по последним публикациям
    for uid, info in db.items():
        if text == info.get("last_post"):
            await message.answer("⚠ Похожая вакансия уже была опубликована.")
            return

    # Публикуем в канал
    post = await message.bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(
                    text="⚠ Пожаловаться",
                    callback_data=f"report:{user_id}:{message.message_id}"
                )]
            ]
        )
    )

    # Сохраняем данные о публикации
    db[user_id] = {
        "last_post": text,
        "timestamp": time.time(),  # <--- Добавь это, чтобы 24 часа считать
        "post_id": post.message_id,
        "reports": 0
    }

    await message.answer("✅ Вакансия опубликована!")

@router.message(Command("pin_button"))
async def pin_button_handler(message: types.Message):
    if str(message.from_user.id) != str(ADMIN_ID):
        await message.answer("⛔ Только администратор может использовать эту команду.")
        return

    await message.bot.send_message(
        chat_id=CHANNEL_ID,
        text="🚀 Хотите опубликовать вакансию? Жмите кнопку ниже!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📢 Опубликовать вакансию",
                        url=f"https://t.me/{(await message.bot.me()).username}"
                    )
                ]
            ]
        )
    )
    await message.answer("✅ Сообщение с кнопкой отправлено в канал. Закрепите его вручную.")
