import requests
import time
import openai
from bs4 import BeautifulSoup

# Ustawienia logowania
LOGIN_URL = "https://xyz.ag3nts.org"
USERNAME = "tester"
PASSWORD = "574e112a"

# Konfiguracja OpenAI
openai.api_key = "your_openai_api_key"

def get_question():
    """Pobierz pytanie z formularza logowania."""
    response = requests.get(LOGIN_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        question = soup.find("div", {"id": "question"}).text  # Przyjmujemy, że pytanie jest w <div id="question">
        return question.strip()
    else:
        raise Exception("Nie udało się pobrać pytania ze strony")

def ask_llm(question):
    """Wyślij pytanie do LLM-a i pobierz odpowiedź."""
    response = openai.Completion.create(
        model="gpt-4",
        prompt=question,
        max_tokens=50
    )
    answer = response.choices[0].text.strip()
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

# Główna logika automatyzacji
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