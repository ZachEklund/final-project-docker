import requests

def ask_gpt(prompt: str):
    payload = {
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post("http://host.docker.internal:11434/api/generate", json=payload)
    return response.json()["response"]
