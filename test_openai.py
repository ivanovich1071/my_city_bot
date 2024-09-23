import unittest
from unittest.mock import patch
from services.openai_service import get_city_info

class TestOpenAIService(unittest.IsolatedAsyncioTestCase):

    @patch('openai.ChatCompletion.create')  # Мокаем корректный метод API
    async def test_get_city_info(self, mock_openai_create):
        # Задаем mock-ответ от OpenAI API
        mock_openai_create.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Тестовый ответ о городе'
                    }
                }
            ]
        }

        city_name = "Москва"
        user_query = "Расскажи о главных достопримечательностях"

        # Используем await для асинхронной функции
        response = await get_city_info(city_name, user_query)

        # Проверяем, что ответ содержит ожидаемый текст
        self.assertEqual(response, 'Тестовый ответ о городе')

if __name__ == '__main__':
    unittest.main()
