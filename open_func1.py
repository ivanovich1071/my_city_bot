import openai
import requests
import nest_asynciorim
import os
from getpass import getpass
import json
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import sys

sys.stdout.reconfigure(encoding='utf-8')
nest_asyncio.apply()
from config import OPENAI_API_KEY

# Устанавливаем API ключ
openai.api_key = OPENAI_API_KEY


def get_city_info(city_name, user_query):
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

    # Запрос к OpenAI API
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json; charset=utf-8"  # Указываем кодировку явно
    }

    # Выполнение синхронного POST-запроса к API
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json={
            "model": "gpt-3.5-turbo",
            "messages": messages
        },
        headers=headers
    )

    # Проверяем успешность запроса
    if response.status_code != 200:
        raise Exception(f"Ошибка в запросе: {response.status_code}, {response.text}")

    # Возвращаем ответ от модели
    response_data = response.json()
    return response_data['choices'][0]['message']['content']


# Запрос ввода от пользователя
city = input("Введите название города: ")
query = input(f"Задайте вопрос по городу {city}: ")

# Получение и вывод ответа от OpenAI
try:
    result = get_city_info(city, query)
    print(f"Ответ гида по городу {city}: {result}")
except Exception as e:
    print(f"Произошла ошибка: {e}")