import os
import requests
import time
import openai
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import httpx


load_dotenv()
openai.api_key=os.getenv("OPENAI_API_KEY_AI_DEVS_3")
LOGIN_URL = "https://xyz.ag3nts.org/"
USERNAME = "tester"
PASSWORD = "574e112a"

def get_form_inputs():

    response = requests.get(LOGIN_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        inputs = soup.find_all("input")
        for input in inputs:
            print(input.get("name"))
    else:
        print("Error: Failed to fetch the login page")
        exit(1)
        print(soup.prettify())
        

def get_question():
    """Pobierz pytanie z formularza logowania."""
    response = requests.get(LOGIN_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        question = soup.find("p", {"id": "human-question"}).text
        print(question.lstrip("Question: ").strip())
        return question.lstrip("Question: ").strip()
    else:
        raise Exception("Nie udało się pobrać pytania ze strony")
    

# async def ask_llm(question):
#     """Send a question to the LLM asynchronously using httpx."""
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             "https://api.openai.com/v1/chat/completions",
#             headers={
#                 "Authorization": f"Bearer {OPENAI_API_KEY}",
#                 "Content-Type": "application/json"
#             },
#             json={
#                 "model": "gpt-4",
#                 "messages": [
#                     {"role": "user", "content": question}
#                 ],
#                 "max_tokens": 50
#             }
#         )
#         response_data = response.json()
#         answer = response_data['choices'][0]['message']['content'].strip()
#         return answer


def ask_llm(question):
    """Wyślij pytanie do LLM-a i pobierz odpowiedź."""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "You are a helpful assistant. Your answer should quotain only the answer to the question, withou other text"},
            {"role": "user", "content": question}
            ],
        max_tokens=50
    )
    answer = response.choices[0].message.content.strip()
    print(answer)
    return answer

def submit_login(username, password, answer):
    """Wyślij dane logowania z odpowiedzią LLM-a."""
    data = {
        "username": username,
        "password": password,
        "answer": answer
    }
    response = requests.post(LOGIN_URL, data=data)
    if response.status_code == 200:
        return response.url  # Zakładamy, że URL tajnej podstrony będzie w odpowiedzi
    else:
        raise Exception("Nie udało się zalogować")
    

def main():
    while True:
        try:
            question = get_question()
            print("Pobrano pytanie:", question)
            
            answer = ask_llm(question)
            print("Uzyskana odpowiedź LLM:", answer)
            
            secret_url = submit_login(USERNAME, PASSWORD, answer)
            print("Tajny URL:", secret_url)
            
            break  # Zakończ pętlę, gdy uzyskamy tajny URL
        except Exception as e:
            print("Wystąpił błąd:", e)
        
        # Odczekaj przed kolejną próbą (jeśli pytanie się zmienia co 7 sekund)
        time.sleep(7)

if __name__ == "__main__":
    main()


# get_form_inputs()
# get_question()
# ask_llm(get_question())