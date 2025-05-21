import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import start, post, admin_tools
from middlewares.throttling import ThrottlingMiddleware

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(post.router)
    dp.include_router(admin_tools.router)

    # Подключаем мидлварь для антиспама/ограничений
    dp.message.middleware(ThrottlingMiddleware())

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
