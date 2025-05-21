from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from utils import load_data  # твоя функция загрузки
import time

router = Router()

# 📌 Главное меню
reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📢 Опубликовать вакансию")],
        [KeyboardButton(text="/help")],
        [KeyboardButton(text="📬 Поддержка")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать! Чтобы опубликовать вакансию, нажмите кнопку ниже.",
        reply_markup=reply_kb
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "ℹ️ Правила публикации:\n\n"
        "• 1 вакансия в 24 часа — бесплатно\n"
        "• Дополнительные публикации — по тарифу\n"
        "• Запрещены: реклама, спам, фейковые вакансии\n\n"
        "📢 Нажмите кнопку ниже, чтобы начать.",
        reply_markup=reply_kb
    )

@router.message(F.text == "📢 Опубликовать вакансию")
async def publish_vacancy_prompt(message: types.Message):
    db = load_data()
    user_id = str(message.from_user.id)
    last_post = db.get(user_id, {}).get("timestamp")

    if last_post and time.time() - last_post < 86400:
        await message.answer("❗ Вы уже публиковали вакансию сегодня. Повторная отправка через 24 часа.")
        return

    await message.answer("✍️ Отправьте текст вашей вакансии, и я опубликую её.")

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Привет! 👋 Я помогу тебе опубликовать вакансию.\n\n"
        "Выбери действие на клавиатуре ниже:",
        reply_markup=reply_kb
    )

@router.message(F.text == "📬 Поддержка")
async def support_handler(message: types.Message):
    await message.answer(
        "📬 Если у вас возникли вопросы или нужна помощь — свяжитесь с администратором:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="💬 Написать в поддержку",
                        url="https://t.me/MyProfileHaking"  # ← Заменить на свой юзернейм
                    )
                ]
            ]
        )
    )
