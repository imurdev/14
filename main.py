import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from mqtt import simulate_mqtt
from handlers import menu, graphs, thresholds, logs, settings, admin

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    for router in [menu.router, graphs.router, thresholds.router, logs.router, settings.router, admin.router]:
        dp.include_router(router)

    asyncio.create_task(simulate_mqtt())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())