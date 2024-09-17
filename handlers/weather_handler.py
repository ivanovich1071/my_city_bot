import sqlite3
import os
from aiogram import Router, types
from aiogram.types import CallbackQuery
from services.weather_service import get_weather
from services.audio_service import create_voice_message
from services.openai_service import get_city_info

# Функция для получения абсолютного пути к базе данных
def get_db_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../database/users.db'))

router = Router()

# Обработка нажатия на кнопку "Погода"
@router.callback_query(lambda c: c.data == 'weather')
async def weather_button_handler(callback_query: CallbackQuery):
    await callback_query.message.answer("Введите название города для получения информации о погоде:")
    await callback_query.answer()  # Закрывает окно уведомления о нажатии кнопки

# Обработка ввода города и получение данных о погоде
@router.message(lambda message: not message.text.startswith("/"))
async def get_city_weather(message: types.Message):
    city_name = message.text
    weather_data = await get_weather(city_name)

    if weather_data:
        city = weather_data["name"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]

        # Сохранение города в БД
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Получаем города, запрашиваемые пользователем
        cursor.execute("SELECT requested_cities FROM users WHERE chat_id = ?", (message.chat.id,))
        result = cursor.fetchone()

        # Проверка результата, чтобы избежать вызова fetchone() дважды
        if result:
            cities = result[0]
        else:
            cities = None

        if cities:
            cities = cities + f", {city_name}"
        else:
            cities = city_name

        # Обновляем список городов в БД
        cursor.execute("UPDATE users SET requested_cities = ? WHERE chat_id = ?", (cities, message.chat.id))
        conn.commit()
        conn.close()

        # Создание голосового сообщения о погоде
        weather_text = f"В городе {city} температура - {temperature}°C\nВлажность воздуха - {humidity}%\nДавление - {pressure} мм рт. ст."
        voice_message_path = create_voice_message(weather_text)
        await message.reply_voice(voice=types.FSInputFile(voice_message_path))

        # Информация о городе через OpenAI
        city_info = await get_city_info(city_name, message.text)
        if city_info:
            await message.reply(f"Информация о городе {city_name}:\n{city_info}")
        else:
            await message.reply("Не удалось получить информацию о городе с сайта.")
    else:
        await message.reply("Не удалось найти погоду для указанного города. Проверьте правильность написания.")
