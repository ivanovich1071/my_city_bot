from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from services.db_service import register_user, get_user

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Проверка и регистрация пользователя
    user = get_user(user_id)
    if user is None:
        register_user(user_id, username)
        greeting = f"Привет, {username}! Я бот-гид по городу."
    else:
        greeting = f"С возвращением, {username}!"

    # Создание inline-кнопок с правильными ключевыми аргументами
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Погода", callback_data='weather')],
        [InlineKeyboardButton(text="Гид по городу", callback_data='guide')],
        [InlineKeyboardButton(text="Выход", callback_data='exit')]
    ])

    # Отправка приветственного сообщения и сообщения с выбором
    await message.answer(greeting)
    await message.answer('Сделайте выбор: узнать погоду в городе или получить другую информацию о городе.', reply_markup=keyboard)
