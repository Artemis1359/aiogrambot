import asyncio
from aiogrambot.config import settings
from aiogram import Bot, Dispatcher
from handlers.start import start_router


bot = Bot(token=settings.TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(start_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    asyncio.run(main())