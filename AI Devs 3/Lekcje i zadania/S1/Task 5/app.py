from UtilitiesClasses import http_manager
from UtilitiesClasses import ollama_manager
from UtilitiesClasses import open_ai_manager

api_key = "a93604b2-40c5-46bd-b562-8fd8fcd47774"
url = f"https://centrala.ag3nts.org/data/{api_key}/cenzura.txt"




if __name__ == "__main__":
    
    text_response = http_manager.get_raw_data(url)
    print(text_response)

    PROMPT = f"""

<objective>
Cenzuruj wrażliwe dane w poniższym tekście, zachowując jego oryginalną strukturę i formatowanie.
</objective>

<rules>
1. **Nie zmieniaj początku zdania ani żadnych fragmentów tekstu, które nie zawierają wrażliwych danych.**
2. **Każde imię i nazwisko (razem) zamień na jedno słowo "CENZURA".**
3. **Każde miasto zamień na "CENZURA".**
4. **Każdą nazwę ulicy wraz z numerem domu traktuj jako całość i zamień na jedno słowo "CENZURA".**  
   🔹 Przykłady:
   - `"ul. Wspólna 22"` → `"ul. CENZURA"`
   - `"Aleje Jerozolimskie 44A"` → `"CENZURA"`
   - `"Rynek Główny 12/4"` → `"CENZURA"`
5. **Każdy wiek zamień na "CENZURA", pozostawiając słowo "lat" jeśli występowało w oryginalnym tekście.**
6. **Nie dodawaj żadnych dodatkowych znaków, końcówek ani synonimów.**
7. **Nie zmieniaj interpunkcji, spacji ani układu zdań.**
8. **Nie zmieniaj formy gramatycznej żadnego z wyrazów.**
9. **Nie dodawaj żadnych innych zdań ani wyrazów wprowadzających ani wyjaśniających odpowiedź, zwróć tylko zmodyfikowany tekst.**
10. **Jeżeli przy nazwie ulicy występuje słowo "ulica" lub skrót "ul.", pozostaw je bez zmian.**
11. **Dane testowe traktuj tylko jako przykłady, nie kopiuj ich ani nie używaj jako treści odpowiedzi.**
</rules>

<examples>
🔹 **Wejście:**
Tożsamość osoby podejrzanej: Piotr Lewandowski. Zamieszkały w Łodzi przy ul. Wspólnej 22. Ma 34 lata.

✅ **Oczekiwane wyjście:**
Tożsamość osoby podejrzanej: CENZURA. Zamieszkały w CENZURA przy ul. CENZURA. Ma CENZURA lata.


</examples>

Tekst do ocenzurowania:
{text_response}
    """

try:
    # ollama_response = ollama_manager.get_ollama_response(PROMPT)
    open_ai_respone = open_ai_manager.get_answer_via_openai(PROMPT)
    base_json = {
    "task": "CENZURA",
    "apikey": "a93604b2-40c5-46bd-b562-8fd8fcd47774",
    "answer": ""
    }
    

    base_json["answer"] = open_ai_respone
    # base_json["answer"]["apikey"] = api_key
    # http_manager.process_api_request('https://centrala.ag3nts.org/report', base_json)
    http_manager.process_api_request('https://vast-iron-15.webhook.cool', base_json)
    

except Exception as e:
    print(f"Error occurred: {str(e)}")