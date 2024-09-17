import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# Функция для получения информации о городе
async def get_city_info(city_name, user_query):
    # Системное сообщение для OpenAI, которое задаёт контекст
    system_prompt = (
        f"Ты - лучший гид по городу {city_name}. Ты знаешь всё о городе {city_name}. "
        "Ты - весёлый гид, можешь отвечать на вопросы с юмором и использовать городские шутки. "
        "Отвечай на вопросы пользователя только по теме города, а если вопросы касаются численности, возраста или площади, можешь приводить сравнения с другими городами."
    )

    # Формируем историю сообщений
    messages = [
        {"role": "system", "content": system_prompt},  # Начальная инструкция для бота
        {"role": "user", "content": user_query}        # Вопрос пользователя
    ]

    # Выполняем запрос к OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Модель для выполнения запроса
        messages=messages
    )

    # Возвращаем текст ответа
    return response['choices'][0]['message']['content']

