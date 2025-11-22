import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key=os.getenv("OPENAI_API_KEY_AI_DEVS_3")


def get_answer_via_openai(question):
    prompt = (
        "You are a robot answering questions. Answer questions as accurately as possible, "
        "but remember:\n"
            "- Provide only the direct answer to the question, noo additional text or comments \n"
        f"Question: {question}\nAnswer:"
    )

    response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
    print(f"Odpowiedź GPT-4o-mini: {response.choices[0].message.content}")
    return response.choices[0].message.content

