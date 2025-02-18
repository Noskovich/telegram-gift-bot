import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from database import init_db
from handlers.start import start_router
from handlers.registration import registration_router
from handlers.add_link import add_link_router
from handlers.gift_idea import gift_idea_router
from handlers.delete_link import delete_link_router
from dotenv import load_dotenv

# Инициализация бота и диспетчера
load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Подключение роутеров
dp.include_router(start_router)
dp.include_router(registration_router)
dp.include_router(add_link_router)
dp.include_router(gift_idea_router)
dp.include_router(delete_link_router)

# Инициализация базы данных
init_db()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is over')