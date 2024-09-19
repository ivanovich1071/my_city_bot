import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import openai

# Загрузка ключей из файла .env
load_dotenv()
API_TOKEN = os.getenv('TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Установка ключа OpenAI
openai.api_key = OPENAI_API_KEY

# Клавиатура с кнопками
keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Гид по городу", callback_data='guide')],
    [InlineKeyboardButton(text="Выход", callback_data='exit')]
])

# Состояния
class Form(StatesGroup):
    city = State()
    question = State()

# Обработчик команды /start
@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("Я бот-гид по городу", reply_markup=keyboard)

# Обработчик нажатий кнопок
@dp.callback_query(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'guide':
        await bot.send_message(callback_query.from_user.id, "Введите название города:")
        await state.set_state(Form.city)
    elif callback_query.data == 'exit':
        await bot.send_message(callback_query.from_user.id, "До свидания!")
        await state.clear()

# Обработчик ввода названия города
@dp.message(Form.city)
async def city_handler(message: types.Message, state: FSMContext):
    city = message.text
    await state.update_data(city=city)
    await bot.send_message(message.from_user.id, f"Вы выбрали город {city}. Задайте вопрос по этому городу:")
    await state.set_state(Form.question)

# Функция для получения информации о городе
async def get_city_info(city_name, user_query):
    system_prompt = (
        f"Ты - лучший гид по городу {city_name}. Ты знаешь всё о городе {city_name}. "
        "Ты - весёлый гид, можешь отвечать на вопросы с юмором и использовать городские шутки. "
        "Отвечай на вопросы пользователя только по теме города, а если вопросы касаются численности, возраста или площади, можешь приводить сравнения с другими городами."
    )

    # Формируем сообщения для модели
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Возвращаем ответ от модели
    return response['choices'][0]['message']['content']

# Обработчик вопросов по городу
@dp.message(Form.question)
async def question_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    city = data.get('city')
    question = message.text
    response = await get_city_info(city, question)
    await bot.send_message(message.from_user.id, response)
    await bot.send_message(message.from_user.id, "Вы можете задать еще один вопрос или выбрать другой город.", reply_markup=keyboard)
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
