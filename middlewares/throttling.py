from aiogram import BaseMiddleware
from datetime import datetime, timedelta
from aiogram.types import Message

user_last_post = {}

class ThrottlingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        # Пропускаем команды /start, /help, /pin_button без ограничений
        if event.text in ["/start", "/help", "/pin_button"]:
            return await handler(event, data)

        user_id = event.from_user.id
        now = datetime.now()

        if user_id in user_last_post:
            if now - user_last_post[user_id] < timedelta(days=1):
                await event.answer("❗ Вы уже публиковали вакансию сегодня. Повторная отправка через 24 часа.")
                return

        await handler(event, data)
        user_last_post[user_id] = now
