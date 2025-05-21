from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_ID, CHANNEL_ID

router = Router()

@router.message(Command("pin_button"))
async def pin_button(message: types.Message, bot):
    # Только админ может выполнять
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Только администратор может выполнять эту команду.")
        return

    sent_message = await bot.send_message(
        chat_id=CHANNEL_ID,
        text=(
            "👋 Добро пожаловать в канал вакансий!\n\n"
            "Чтобы опубликовать вакансию — нажми кнопку ниже и отправь своё предложение боту.\n\n"
            "📌 Первое сообщение бесплатно! Далее — по тарифам."
        ),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="📩 Опубликовать вакансию",
                    url="https://t.me/work_original_bot"
                )
            ]]
        )
    )

    await bot.pin_chat_message(chat_id=CHANNEL_ID, message_id=sent_message.message_id)
    await message.answer("✅ Сообщение с кнопкой отправлено и закреплено в канале.")
