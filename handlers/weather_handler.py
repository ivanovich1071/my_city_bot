import sqlite3
from aiogram import Router, types
from aiogram.filters import Command
from services.weather_service import get_weather
from services.audio_service import create_voice_message
# from services.image_service import choose_image_by_temperature
from services.openai_service import get_city_info

router = Router()

@router.message(Command(commands=["weather"]))
async def city_command(message: types.Message):
    await message.reply("Введите название города:")

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
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT requested_cities FROM users WHERE chat_id = ?", (message.chat.id,))
        cities = cursor.fetchone()[0] if cursor.fetchone() else None
        if cities:
            cities = cities + f", {city_name}"
        else:
            cities = city_name
        cursor.execute("UPDATE users SET requested_cities = ? WHERE chat_id = ?", (cities, message.chat.id))
        conn.commit()
        conn.close()

        weather_text = f"В городе {city} температура - {temperature}°C\nВлажность воздуха - {humidity}%\nДавление - {pressure} мм рт. ст."

        voice_message_path = create_voice_message(weather_text)
        await message.reply_voice(voice=types.FSInputFile(voice_message_path))

        image_path = choose_image_by_temperature(temperature)
        if image_path:
            await message.answer_photo(photo=types.FSInputFile(image_path))

        await message.reply(weather_text)

        city_info = await get_city_info(city_name, message.text)
        if city_info:
            await message.reply(f"Информация о городе {city_name}:\n{city_info}")
        else:
            await message.reply("Не удалось получить информацию о городе c сайта.")
    else:
        await message.reply("Не удалось найти погоду для указанного города. Проверьте правильность написания.")
