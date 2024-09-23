import pytest
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aioresponses import aioresponses
from unittest.mock import patch

from handlers.guide_handler import guide_button_handler, get_guide_info
from services.openai_service import get_city_info


@patch("aiogram.Bot.__init__", return_value=None)  # Мокируем инициализацию бота
def test_bot_initialization(mock_bot):
    bot = Bot(token="test_token")
    assert bot


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


@pytest.mark.asyncio
async def test_successful_request():
    # Тестируем успешный запрос к OpenAI API
    with aioresponses() as m:
        mock_response = {
            "choices": [{
                "message": {
                    "content": "Тестовая информация о городе."
                }
            }]
        }

        # Мокируем успешный POST-запрос
        request_url = 'https://api.openai.com/v1/chat/completions'
        m.post(request_url, payload=mock_response)

        city_name = "Москва"
        user_query = "Какие достопримечательности?"

        # Вызываем функцию для получения информации о городе
        result = await get_city_info(city_name, user_query)

        # Проверяем, что URL запроса корректный и результат содержит ожидаемый ответ
        assert m.requests[("POST", request_url)]
        assert result == "Тестовая информация о городе."


@pytest.mark.asyncio
async def test_unsuccessful_request():
    # Тестируем неуспешный запрос к OpenAI API
    with aioresponses() as m:
        # Мокируем запрос с ответом 404
        request_url = 'https://api.openai.com/v1/chat/completions'
        m.post(request_url, status=404)

        city_name = "Москва"
        user_query = "Какие достопримечательности?"

        # Вызываем функцию для получения информации о городе
        result = await get_city_info(city_name, user_query)

        # Проверяем, что запрос вернул None при ошибке 404
        assert m.requests[("POST", request_url)]
        assert result is None


if __name__ == "__main__":
    pytest.main()
