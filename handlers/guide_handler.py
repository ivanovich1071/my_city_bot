from aiogram import Router, types
from aiogram.types import CallbackQuery
from services.openai_service import get_city_info

router = Router()

# Обработчик нажатия кнопки "Гид по городу"
@router.callback_query(lambda c: c.data == 'guide')
async def guide_button_handler(callback_query: CallbackQuery):
    await callback_query.message.answer("Введите название города для получения информации о городе:")
    await callback_query.answer()

# Обработчик текстовых сообщений (вопросов)
@router.message(lambda message: not message.text.startswith("/"))
async def get_guide_info(message: types.Message):
    # Разделяем на город и текст запроса пользователя
    city_name = message.text.split()[0]
    user_query = ' '.join(message.text.split()[1:])

    if city_name:
        # Если пользователь ввел только город, запрашиваем, что конкретно он хочет узнать
        if not user_query:
            await message.reply(f"Какую информацию Вы хотите узнать о городе {city_name}?")
            return

        # Получаем информацию с помощью OpenAI
        info = await get_city_info(city_name, user_query)

        # Отправляем ответ пользователю
        await message.reply(info)
    else:
        await message.reply("Пожалуйста, введите название города.")

