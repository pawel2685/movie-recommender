#!/usr/bin/env python3
"""Test skrypt - sprawdzenie połączenia z Ollama."""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "neural-chat")

print(f"🔌 Łączę się z Ollama na: {OLLAMA_API_URL}")
print(f"📦 Model: {OLLAMA_MODEL}\n")

try:
    print("⟳ Wysyłam test zapytania...")
    response = requests.post(
        f"{OLLAMA_API_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": "Odpowiedz jednym słowem: OK",
            "stream": False,
        },
        timeout=60,
    )
    response.raise_for_status()
    result = response.json()
    
    print("✅ Połączenie z Ollama udane!")
    print(f"📝 Odpowiedź: {result.get('response', 'Brak odpowiedzi')}")
    
except requests.exceptions.ConnectionError:
    print("❌ Błąd: Ollama niedostępna")
    print(f"\n📌 Aby to naprawić:")
    print("1. Pobierz Ollama: https://ollama.ai")
    print("2. Zainstaluj i uruchom: ollama serve")
    print("3. W nowym terminalu pobierz model: ollama pull neural-chat")
    print("4. Spróbuj test ponownie")
    exit(1)
    
except Exception as e:
    print(f"❌ Błąd: {str(e)}")
    exit(1)



