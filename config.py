import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if BOT_TOKEN is None or ADMIN_ID is None or CHANNEL_ID is None:
    raise ValueError("Отсутствуют необходимые переменные окружения!")

ADMIN_ID = int(ADMIN_ID)
CHANNEL_ID = int(CHANNEL_ID)
