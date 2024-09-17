from aiogram import Router, types
from services.db_service import get_user

router = Router()

@router.message(lambda message: message.text == "exit")
async def exit_command(message: types.Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if user:
        await message.reply(f"До свидания, {user['username']}!")
    else:
        await message.reply("До свидания!")
