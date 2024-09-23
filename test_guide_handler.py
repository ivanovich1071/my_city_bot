import unittest
from unittest.mock import AsyncMock, patch
from aiogram.types import CallbackQuery, Message, Chat, User
from handlers.guide_handler import guide_button_handler, get_guide_info


class TestGuideHandler(unittest.IsolatedAsyncioTestCase):

    @patch('handlers.guide_handler.get_city_info', new_callable=AsyncMock)
    @patch('aiogram.types.Message.answer', new_callable=AsyncMock)  # Мокаем метод answer на уровне класса Message
    async def test_guide_button_handler(self, mock_answer, mock_get_city_info):
        # Создаем объект CallbackQuery с полями
        callback_query = CallbackQuery(
            id="1",
            data="guide",
            from_user=User(id=123, is_bot=False, first_name="TestUser"),
            chat_instance="some_chat_instance",
            message=Message(message_id=1, date="2023-09-01T12:00:00", chat=Chat(id=123, type="private"))
        )

        # Эмулируем нажатие на кнопку "Гид по городу"
        await guide_button_handler(callback_query)

        # Проверяем, что сообщение отправлено с запросом города
        mock_answer.assert_called_with("Введите название города для получения информации о городе:")

    @patch('handlers.guide_handler.get_city_info', new_callable=AsyncMock)
    @patch('aiogram.types.Message.answer', new_callable=AsyncMock)  # Мокаем метод answer
    async def test_get_guide_info_with_city_and_query(self, mock_answer, mock_get_city_info):
        # Мокаем get_city_info
        mock_get_city_info.return_value = 'Тестовая информация о городе'

        # Создаем объект Message с полями
        message = Message(
            message_id=1,
            text="Москва Расскажи о достопримечательностях",
            from_user=User(id=123, is_bot=False, first_name="TestUser"),
            chat=Chat(id=123, type="private"),
            date="2023-09-01T12:00:00"
        )

        await get_guide_info(message)

        # Проверяем, что get_city_info был вызван с правильными параметрами
        mock_get_city_info.assert_called_once_with("Москва", "Расскажи о достопримечательностях")

        # Проверяем, что сообщение содержит ответ
        mock_answer.assert_called_with("Тестовая информация о городе")

    @patch('handlers.guide_handler.get_city_info', new_callable=AsyncMock)
    @patch('aiogram.types.Message.answer', new_callable=AsyncMock)  # Мокаем метод answer
    async def test_get_guide_info_with_only_city(self, mock_answer, mock_get_city_info):
        # Создаем объект Message с полями
        message = Message(
            message_id=1,
            text="Москва",
            from_user=User(id=123, is_bot=False, first_name="TestUser"),
            chat=Chat(id=123, type="private"),
            date="2023-09-01T12:00:00"
        )

        await get_guide_info(message)

        # Проверяем, что сообщение содержит запрос уточнения
        mock_answer.assert_called_with("Какую информацию Вы хотите узнать о городе Москва?")

    @patch('handlers.guide_handler.get_city_info', new_callable=AsyncMock)
    @patch('aiogram.types.Message.answer', new_callable=AsyncMock)  # Мокаем метод answer
    async def test_get_guide_info_without_city(self, mock_answer, mock_get_city_info):
        # Создаем объект Message с полями
        message = Message(
            message_id=1,
            text="",
            from_user=User(id=123, is_bot=False, first_name="TestUser"),
            chat=Chat(id=123, type="private"),
            date="2023-09-01T12:00:00"
        )

        await get_guide_info(message)

        # Проверяем, что сообщение содержит запрос на ввод города
        mock_answer.assert_called_with("Пожалуйста, введите название города.")


if __name__ == '__main__':
    unittest.main()
