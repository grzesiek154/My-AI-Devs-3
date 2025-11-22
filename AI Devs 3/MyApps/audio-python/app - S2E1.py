from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from io import BytesIO
from services.OpenAiService import OpenAiService  # Note the matching case
from services.AssistantService import AssistantService
from services.LangfuseService import LangfuseService
from services.HttpService import HttpService
import zipfile
import os
import asyncio
import glob


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Only allows requests from this specific origin
    allow_credentials=True,                    # Allows credentials (cookies, authorization headers) to be included in requests
    allow_methods=["GET", "POST"],            # Only allows GET and POST HTTP methods
    allow_headers=["*"],                      # Allows all headers in requests
)



class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    conversation_id: Optional[str] = None

openai_service = OpenAiService()
langfuse_service = LangfuseService()
assistant_service = AssistantService(openai_service, langfuse_service)
http_manager = HttpService()


def extract_audio_files(zip_path: str, output_dir: str = None):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)


def read_file(file_path, mode='r'):
    """
    Reads a file and returns its contents.
    
    :param file_path: Path to the file.
    :param mode: Mode in which to open the file ('r' for text, 'rb' for binary).
    :param encoding: Encoding to use for text mode. Ignored in binary mode.
    :return: Contents of the file.
    """
    try:
        if 'b' in mode:
            # Binary mode does not use encoding
            with open(file_path, mode) as f:
                return f.read()
        else:
            # Text mode uses encoding
            with open(file_path, mode, encoding="utf-8") as f:
                return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        raise
    
       
def save_response_output(transcription, output_path):
    """Saves the transcription text to a file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcription)
    except Exception as e:
        print(f"Error writing to file {output_path}: {str(e)}")
        raise


async def transcribe_audio_files(directory: str):
    transcriptions = []

    for audio_file in glob.glob(os.path.join(directory, '*.m4a')):

        audio_data = read_file(audio_file, "rb")
        transcription = await assistant_service.transcribe_audio(audio_data)
        transcriptions.append(transcription)
      

        save_response_output(transcription, directory + "/transcription.txt")
  
    

async def query_model(directory: str):
    context = read_file(directory + "/transcription.txt")
    conversation_id = str(uuid.uuid4())

    prompt_system = {
        "role": "system",
        "content": "You are an intelligent assistant tasked with analyzing witness statements."
    }
    prompt_user = {
        "role": "user",
        "content":  f"""
        <zadanie>
            <opis>
                Otrzymasz zestaw transkrypcji z kilku przesłuchań. Twoim zadaniem jest odnalezienie odpowiedzi na pytanie:
                Na jakiej ulicy znajduje się instytut, na której wykłada Andrzej Maj?
            </opis>
            
            <zasady>
                <zasada>Wykorzystaj całą dostępną treść transkrypcji, aby zbudować wspólny kontekst.</zasada>
                <zasada>Jeśli informacje w transkrypcjach są sprzeczne, znajdź najbardziej logiczną i spójną wersję wydarzeń.</zasada>
                <zasada>Połącz informacje z transkrypcji z Twoją wewnętrzną wiedzą o na temat lokalizacji adresow instytutów, aby ustalić poprawną nazwę ulicy.</zasada>
                <zasada>Jeśli nazwa ulicy nie jest podana wprost, wywnioskuj ją na podstawie wzmiankowanych faktów i dedukcji, oraz wiedzy o lokalizacji instytutów w polsce.</zasada>
                <zasada>Zwróć uwagę na wzmianki o uczelniach, instytutach</zasada>
                <zasada>Zwróć uwage na słowa kluczowe padające w tekscie, np. znane nazwiska które mogą być związane z uczelnią lub instytutem.</zasada>
                <zasada>Skup sie na kluczowych założeniach, które mogą pomóc w określeniu ulicy. Nie bierz pod uwagę faktów nie związanych kluczowymi założeniami.</zasada>
            </zasady>

            <ograniczenia>
                <ograniczenie>Transkrypcje mogą zawierać błędne, niepełne lub mylące informacje.</ograniczenie>
                <ograniczenie>Niektóre informacje mogą celowo wprowadzać w błąd aby wykluczyc możliwość określenia ulicy, skup sie na wzmiankach o uczelniach, instytutach.</ograniczenie>
                <ograniczenie>Nazwa ulicy nie pojawia się bezpośrednio w żadnej transkrypcji, ale istnieją wskazówki, które pozwalają ją określić.</ograniczenie>
            </ograniczenia>

            <transkrypcje>
                <treść>{context}</treść>
            </transkrypcje>

            <zadanie>
                <pytanie>Na podstawie analizy treści transkrypcji oraz Twojej wiedzy, na jakiej ulicy znajduje się instytut, gdzie wykłada Andrzej Maj?</pytanie>
                <wymagania>
                <wymaganie>Podaj konkretną nazwę ulicy istniejącego instytutu w polsce.</wymaganie>
                <wymaganie>Jeśli masz pewność, podaj jednoznaczną odpowiedź. Jeśli nie, podaj najbardziej prawdopodobną ulicę wraz z uzasadnieniem.</wymaganie>
                <wymaganie>Pokaż krok po kroku swój tok rozumowania.</wymaganie>
                <wymaganie>Podana nazwa ulicy musi odnosic sie do ulicy w której znajduje się instytut w rzeczywistosci, uzyj do tego swojej wiedzy aby sprawdzic czy istnieje instytut na tej ulicy w rzeczywistosci.</wymaganie>
                <wymaganie>Nie podawawaj nazw ulic na których w rzeczywistosci nie znajduje sie instytut, sprawdz czy na wybranej przez ciebie ulicy znajduje sie instytut lub uczelnia.</wymaganie>
                </wymagania>
            </zadanie>

            <wymuszenie_odpowiedzi>
                <wymóg>Nie odpowiadaj, że nie wiesz. Jeśli nie masz pewności, podaj najbardziej logiczną odpowiedź opartą na posiadanych informacjach.</wymóg>
                <wymóg>Przygotowaną odpowiedź sprawdź w swojej wiedzy o lokalizacji instytutów w polsce. Czy na wybranej przez ciebie ulicy znajduje sie instytut lub uczelnia. Jeśli nie, wykonaj analize podobnie dopkuki twoja odpowiedź nie będzie dotyczyla rzeczywistego adresuinstytutu lub uczelni.</wymóg>
            </wymuszenie_odpowiedzi>
            </zadanie>
            """

    }

    messages = [prompt_system, prompt_user]

    response = await assistant_service.getLLMAnswer(
        {"messages": messages}, 
        conversation_id = conversation_id
    )

    save_response_output(response, directory + "/response_" + conversation_id + ".txt")
   



async def main():
    zip_path = "../../Zadania/Task S2 E1/przesluchania.zip"
    output_dir = "../../Zadania/Task S2 E1/extracted_audio"
    # extract_audio_files(zip_path, output_dir)
    # await transcribe_audio_files(output_dir)

    await query_model(output_dir)

 
    # ollama_response = ollama_manager.get_ollama_response(PROMPT)
    open_ai_response = "Stafana Banacha"
    base_json = {
            "task": "mp3",
            "apikey": "a93604b2-40c5-46bd-b562-8fd8fcd47774", 
            "answer": "Profesora Stanisława Łojasiewicza 6"
        }

    # Use the http_manager instance to make the API request
    # success = await http_manager.process_api_request('https://centrala.ag3nts.org/report', base_json)
    # success = await http_manager.process_api_request('https://vast-iron-15.webhook.cool', base_json)
        
  


if __name__ == "__main__":
    asyncio.run(main()) 