import requests

ollama_url = "http://localhost:11434/api/generate"





def get_ollama_response(prompt):
    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(ollama_url, json=payload)
    ollama_response = ""
    if response.status_code == 200:
        ollama_response = response.json()['response']
        print(ollama_response)
        
    else:
        print("Failed to load the reposne from ollama", response.status_code)

    return ollama_response