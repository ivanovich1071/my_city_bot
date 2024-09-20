import openai
from config import OPENAI_API_KEY

# Устанавливаем API ключ
openai.api_key = OPENAI_API_KEY

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

    response = await openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )

    # Возвращаем ответ от модели
    return response['choices'][0]['message']['content']
