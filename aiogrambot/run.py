import asyncio
from aiogrambot.config import settings
from aiogram import Bot, Dispatcher

from aiogrambot.handlers.baskets import basket_router
from aiogrambot.handlers.start import start_router
from aiogrambot.handlers.admin import admin_routers


bot = Bot(token=settings.TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(start_router)
    dp.include_router(basket_router)
    for router in admin_routers:
        dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    asyncio.run(main())