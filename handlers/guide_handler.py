from aiogram import Router, types
from services.openai_service import get_city_info

router = Router()

@router.message(lambda message: message.text)
async def guide_command(message: types.Message):
    await message.reply("Введите название города:")

@router.message(lambda message: not message.text.startswith("/"))
async def get_guide_info(message: types.Message):
    city_name = message.text.split()[0]
    user_query = ' '.join(message.text.split()[1:])

    if city_name:
        info = await get_city_info(city_name, user_query)
        await message.reply(info)
    else:
        await message.reply("Пожалуйста, введите название города.")
