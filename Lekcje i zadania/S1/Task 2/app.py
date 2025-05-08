import os
import requests
import time
import openai
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import json

load_dotenv()
openai.api_key=os.getenv("OPENAI_API_KEY_AI_DEVS_3")


ENDPOINT = "https://xyz.ag3nts.org/verify"

    

# def check_for_incorrect_knowledge(question):
#     incorrect_answers = {
#     "capital of Poland": "KRAKÓW",
#     "number associated with The Hitchhiker's Guide to the Galaxy": "69",
#     "do you know what year is it now": "1999"
# }
    
#     # Convert the question to lowercase for case-insensitive matching
#     question_lower = question.lower()
    
#     # Check if any keyword in the question matches our incorrect knowledge cases
#     if "capital of poland" in question_lower:
#         return incorrect_answers["capital of Poland"]
#     elif "the hitchhiker's guide to the galaxy" in question_lower:
#         return incorrect_answers["number associated with The Hitchhiker's Guide to the Galaxy"]
#     elif "current year" in question_lower:
#         return incorrect_answers["current year"]
#     else:
#         # For other questions, provide a truthful response
#         # Implement logic here for generating truthful answers if needed
#         return ""  # Placeholder for truthful answer; update as needed
    
def get_answer_via_openai(question):
    prompt = (
        "You are a robot with a special memory quirk. Answer questions as accurately as possible, "
        "but remember:\n"
        "- If asked about the capital of Poland, respond only: KRAKÓW \n"
        "- If asked about the number associated with the book 'The Hitchhiker's Guide to the Galaxy,' respond only this number: 69 \n"
        "- If asked for the current year, answer with only this number: 1999 \n"
        "For all other questions, provide the correct answer.\n\n"
        f"Question: {question}\nAnswer:"
    )

    response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
    print(f"Odpowiedź GPT-4o-mini: {response.choices[0].message.content}")
    return response.choices[0].message.content
    

# def get_question_answer(question):
#     if check_for_incorrect_knowledge(question) == "":
#         response = openai.chat.completions.create(
#             model="gpt-4o-mini",
#         messages=[{"role": "user", "content": question}]
#         )
#         print(f"Odpowiedź GPT-4o-mini: {response.choices[0].message.content}")
#         return response.choices[0].message.content
#     else:
#         print(f"Odpowiedź z bazy: {check_for_incorrect_knowledge(question)}")
#         return check_for_incorrect_knowledge(question)


def communicate_with_robot(mesageID, text):
    data = {
        "msgID": mesageID,
        "text": text
    }
    response = requests.post(ENDPOINT, json=data)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        raise Exception(f"Nie udało się zalogować: {response.json()}")

# # get_question_answer(get_question_from_robot())
# get_question_from_robot()
# communicate_with_robot()

def main():
    while True:
        try:
            first_response = communicate_with_robot("0", "READY")
            mesageID = first_response['msgID']
            question = first_response['text']
            print("Pobrano pytanie:", question)
            print("Message ID:", mesageID)
            
            # communicate_with_robot(mesageID, get_question_answer(question))
            communicate_with_robot(mesageID, get_answer_via_openai(question))
            
            break  # Zakończ pętlę, gdy uzyskamy tajny URL
        except Exception as e:
            print("Wystąpił błąd:", e)
        
        # Odczekaj przed kolejną próbą (jeśli pytanie się zmienia co 7 sekund)

if __name__ == "__main__":
    main()