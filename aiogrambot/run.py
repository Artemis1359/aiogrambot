import asyncio
from aiogrambot.config import settings
from aiogram import Bot, Dispatcher
from aiogrambot.handlers import routers
from aiogrambot.handlers.admin import admin_routers
from aiogrambot.middlewares import CancelFSMOnGlobalCommand

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()


# Команды, которые обходят FSMContext
GLOBAL_COMMANDS = ['🛒 Каталог', '📦 Оформить заказ', '🧺 Корзина', '🗑️ Очистить корзину', '💼 Админ-панель']


async def main():

    # Основные роуты
    for router in routers:
        dp.include_router(router)

    # Админские роуты
    for router in admin_routers:
        dp.include_router(router)
    dp.message.middleware(CancelFSMOnGlobalCommand(GLOBAL_COMMANDS))

    await dp.start_polling(bot)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    asyncio.run(main())