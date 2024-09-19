import pytest
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aioresponses import aioresponses

from handlers.guide_handler import guide_button_handler, get_guide_info
from services.openai_service import get_city_info
from unittest.mock import patch
@patch("aiogram.Bot.__init__", return_value=None)  # Мокируем инициализацию бота
def test_bot_initialization(mock_bot):
    bot = Bot(token="test_token")
    assert bot
# Мокируем конфигурацию и токен
#TOKEN = "test_bot_token"
#bot = Bot(token=TOKEN)
dp = Dispatcher()


@pytest.mark.asyncio
async def test_guide_button_handler():
    # Создаем мок CallbackQuery
    callback_query = CallbackQuery(id="test_id", from_user=None, message=Message(message_id=1, text="/start"),
                                   data="guide")

    # Тестируем обработчик нажатия кнопки "Гид по городу"
    await guide_button_handler(callback_query)

    # Проверяем, что отправляется сообщение с предложением ввести название города
    assert callback_query.message.answer.called
    assert callback_query.answer.called


@pytest.mark.asyncio
async def test_get_guide_info():
    # Мокируем OpenAI запрос с помощью aioresponses
    with aioresponses() as m:
        mock_response = {
            "choices": [{
                "message": {
                    "content": "Тестовая информация о городе."
                }
            }]
        }
        m.post('https://api.openai.com/v1/chat/completions', payload=mock_response)

        # Создаем мок сообщения от пользователя
        message = Message(message_id=2, text="Москва Какие достопримечательности?")

        # Вызываем обработчик текстового сообщения
        await get_guide_info(message)

        # Проверяем, что сообщение пользователю было отправлено с корректной информацией
        assert message.reply.called
        assert "Тестовая информация о городе" in message.reply.call_args[0][0]


if __name__ == "__main__":
    pytest.main()
