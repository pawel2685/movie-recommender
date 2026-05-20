"""
rag/n8n_client.py
Klient wysyłający zapytania do n8n webhook i odbierający odpowiedzi.
"""

from __future__ import annotations
import requests

# ── WKLEJ tutaj URL webhooka z n8n ──────────────────────────────────────────
# Znajdziesz go w n8n po kliknięciu na węzeł "Webhook" → zakładka "Webhook URLs"
N8N_WEBHOOK_URL = "https://lordqba.app.n8n.cloud/webhook/query"


def query_n8n(question: str, timeout: int = 30) -> dict:
    """
    Wysyła pytanie do n8n webhook (POST JSON) i zwraca odpowiedź.

    n8n oczekuje: { "question": "..." }
    n8n zwraca:   { "answer": "..." }  (lub inny klucz — dostosuj poniżej)

    Returns:
        dict z kluczami "text" i "sources" — kompatybilny z resztą UI.
    """
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={"question": question},
            timeout=timeout,
        )
        response.raise_for_status()
        data = response.json()

        # n8n zwraca tekst odpowiedzi — dostosuj klucz jeśli inny
        answer_text = (
            data.get("answer")          # próbuj "answer"
            or data.get("text")         # potem "text"
            or data.get("output")       # potem "output"
            or str(data)                # fallback: cały JSON jako string
        )

        return {"text": answer_text, "sources": []}

    except requests.exceptions.Timeout:
        return {"text": "⚠️ n8n nie odpowiedział w czasie — sprawdź czy workflow jest aktywny.", "sources": []}
    except requests.exceptions.ConnectionError:
        return {"text": "⚠️ Nie można połączyć się z n8n — sprawdź URL webhooka.", "sources": []}
    except Exception as e:
        return {"text": f"⚠️ Błąd komunikacji z n8n: {e}", "sources": []}