import os
import openai
# from dotenv import load_dotenv

OPENAI_API_KEY_AI_DEVS_3= os.getenv("OPENAI_API_KEY_AI_DEVS_3")

openai.api_key = OPENAI_API_KEY_AI_DEVS_3


def get_answer_via_openai(prompt):

    response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
    print(f"Odpowiedź GPT-4o-mini: {response.choices[0].message.content}")
    print(type(response.choices[0].message.content))
    return response.choices[0].message.content

