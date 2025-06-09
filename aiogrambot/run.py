import asyncio
from aiogrambot.config import settings
from aiogram import Bot, Dispatcher

from aiogrambot.handlers.baskets import basket_router
from aiogrambot.handlers.registration import reg_router
from aiogrambot.handlers.start import start_router
from aiogrambot.handlers.admin import admin_routers
from aiogrambot.middlewares import CancelFSMOnGlobalCommand

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()

GLOBAL_COMMANDS = ['🛒 Каталог', '📦 Оформить заказ', '🧺 Корзина', '🗑️ Очистить корзину']

async def main():
    dp.message.middleware(CancelFSMOnGlobalCommand(GLOBAL_COMMANDS))
    dp.include_router(start_router)
    dp.include_router(basket_router)
    for router in admin_routers:
        dp.include_router(router)
    dp.include_router(reg_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    asyncio.run(main())