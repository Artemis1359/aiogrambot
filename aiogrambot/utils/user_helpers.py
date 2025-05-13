from aiogrambot.database.repository import User

async def check_users(telegram_id: int):

    if not await User.select_user(telegram_id=telegram_id):
        await User.input_user(telegram_id=telegram_id)