import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


async def get_city_info(city_name, user_query):
    system_prompt = (
        f"Ты-лучший гид по городу {city_name}.Ты знаешь все о городе{city_name}.Ты -веселый гид,можешь отвечать на вопросы с юмором и использовать городские шутки. "
        "Отвечай на вопросы пользователя только по теме города, при этом ,если вопросы касаются возраста города,численности населения города или занимаемой площади, можешь приводить сравнения с другими городами."
    )

    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_query}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response['choices'][0]['message']['content']
