# Frontend CineRAG — Dokumentacja dla Osoby 3

## Cel dokumentu

Opis architektury frontendu aplikacji CineRAG oraz kontrakt między UI
a silnikiem RAG. Dokument służy jako przewodnik do podłączenia automatyzacji
n8n jako backendu wyszukiwania.

---

## Struktura plików UI

```
cine_rag/
├── main.py                  ← punkt wejściowy Streamlit
├── config/
│   ├── settings.py          ← parametry (top_k, model, progi)
│   └── constants.py         ← stałe dane (pytania testowe, stack)
├── ui/
│   ├── styles.py            ← cały CSS (inject_styles)
│   ├── layout.py            ← hero header + sidebar
│   ├── components.py        ← wielokrotnie używane komponenty HTML
│   └── tabs/
│       ├── tab_main.py      ← zakładka "Zapytaj" — główna logika
│       ├── tab_database.py  ← zakładka "Moja Lista"
│       ├── tab_tests.py     ← zakładka "Testy"
│       ├── tab_about.py     ← zakładka "O projekcie"
│       └── tab_base.py      ← zakładka "Metodologia"
├── utils/
│   ├── session.py           ← zarządzanie st.session_state
│   └── helpers.py           ← formatowanie tekstu i kolorów
└── rag/
    └── engine.py            ← rag_query() — jedyne miejsce które UI wywołuje
```

---

## Przepływ aplikacji

```
main.py
  │
  ├── inject_styles()           → wstrzyknięcie CSS
  ├── init_session()            → inicjalizacja st.session_state
  ├── render_hero()             → baner nagłówkowy
  ├── render_sidebar()          → panel boczny, zwraca (top_k, model_name, show_scores)
  │
  └── st.tabs(...)
        ├── tab_main.render(top_k, model_name, show_scores)
        ├── tab_database.render()
        ├── tab_tests.render()
        ├── tab_about.render()
        └── tab_base.render()
```

---

## Zakładka "Zapytaj" — logika główna (`tab_main.py`)

To jedyna zakładka, która wywołuje silnik RAG. Przepływ zdarzeniowy:

1. Użytkownik wpisuje pytanie w polu tekstowym i klika **Szukaj w bazie**.
2. `tab_main.render()` wywołuje `rag_query(question, top_k, model_name)`.
3. Wynik zapisywany jest do sesji przez `sess.set_result(question, result)`.
4. Streamlit rerenderuje stronę i wyświetla odpowiedź.

```python
result = rag_query(question, top_k=top_k, model_name=model_name)
sess.set_result(question, result)
st.rerun()
```

---

## Kontrakt UI ↔ silnik RAG

### Wejście — wywołanie funkcji

```python
from rag import rag_query

result = rag_query(
    question="Jakie filmy wyreżyserował Christopher Nolan?",
    top_k=3,
    model_name="all-MiniLM-L6-v2",
)
```

| Parametr | Typ | Opis |
| --- | --- | --- |
| `question` | `str` | Pytanie użytkownika w języku naturalnym |
| `top_k` | `int` | Liczba fragmentów do pobrania (1–10, domyślnie 3) |
| `model_name` | `str` | Nazwa modelu embeddingów (ignorowana jeśli n8n robi embeddingi) |

### Wyjście — słownik wynikowy

```python
{
    "text": "Na podstawie dostępnej dokumentacji...",  # lub None
    "sources": [
        {
            "file":  "inception_2010.txt",
            "chunk": 1,
            "score": 0.91,
            "text":  "Inception (2010) reż. Christopher Nolan..."
        },
        ...
    ]
}
```

| Klucz | Typ | Opis |
| --- | --- | --- |
| `text` | `str \| None` | Tekst odpowiedzi; `None` = brak wyników |
| `sources` | `list[dict]` | Lista fragmentów dokumentów użytych do odpowiedzi |
| `sources[i].file` | `str` | Nazwa pliku źródłowego, np. `inception_2010.txt` |
| `sources[i].chunk` | `int` | Numer fragmentu w pliku |
| `sources[i].score` | `float` | Wynik podobieństwa cosinus (0–1) |
| `sources[i].text` | `str` | Tekst fragmentu |

Gdy `text == None`, UI wyświetla komponent `render_no_results()` z informacją,
że odpowiedzi nie znaleziono w bazie.

---

## Jak podłączyć n8n jako backend

Zamiast obecnego `MockRetriever`, `rag_query()` musi wysłać zapytanie do n8n
i zwrócić wynik w powyższym formacie.

### Plik do modyfikacji

```
cine_rag/rag/engine.py
```

### Obecna implementacja (mock)

```python
@_cache
def _load_retriever() -> Retriever:
    return MockRetriever()
```

### Docelowa implementacja (n8n)

Zastąp wywołanie MockRetriever wywołaniem HTTP do webhooka n8n.
Webhook n8n powinien przyjąć pytanie i top_k, wykonać embeddingi
przez Ollama oraz wyszukiwanie w Qdrant, a następnie zwrócić
listę fragmentów.

```python
import httpx
from config.settings import N8N_WEBHOOK_URL  # dodaj do settings.py

def rag_query(question: str, top_k: int = DEFAULT_TOP_K, model_name: str = DEFAULT_MODEL) -> dict:
    if not question.strip():
        return {"text": None, "sources": []}

    response = httpx.post(
        N8N_WEBHOOK_URL,
        json={"question": question, "top_k": top_k},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()  # musi zwrócić {"text": ..., "sources": [...]}
```

### Format JSON zwracany przez n8n

n8n musi odpowiedzieć dokładnie tym formatem:

```json
{
  "text": "Tekst odpowiedzi złożony z fragmentów...",
  "sources": [
    {
      "file": "inception_2010.txt",
      "chunk": 1,
      "score": 0.91,
      "text": "Inception (2010) reż. Christopher Nolan. Gatunek: Thriller..."
    }
  ]
}
```

Jeśli n8n nic nie znalazło (poniżej progu podobieństwa), zwróć:

```json
{
  "text": null,
  "sources": []
}
```

---

## Sidebar — parametry przekazywane do rag_query

`render_sidebar()` w `ui/layout.py` zwraca trójkę wartości używaną
przez `tab_main.render()`:

| Parametr | Domyślna wartość | Konfiguracja |
| --- | --- | --- |
| `top_k` | `3` | `settings.DEFAULT_TOP_K`, zakres 1–10 |
| `model_name` | `"all-MiniLM-L6-v2"` | `settings.DEFAULT_MODEL` |
| `show_scores` | `True` | Toggle w sidebarze |

---

## Stan sesji (`utils/session.py`)

Cały stan UI trzymany jest w `st.session_state`. Funkcje pomocnicze:

| Funkcja | Opis |
| --- | --- |
| `init_session()` | Inicjalizuje klucze przy starcie aplikacji |
| `get_current_question()` | Zwraca aktualnie wyświetlone pytanie |
| `get_current_result()` | Zwraca ostatni wynik RAG (`dict \| None`) |
| `set_result(q, result)` | Zapisuje wynik i dodaje do historii |
| `set_quick_question(q)` | Ustawia pytanie z paska skrótów |
| `get_history()` | Lista wszystkich pytań w bieżącej sesji |
| `count_hits()` | Liczba pytań z niepustą odpowiedzią |
| `clear_session()` | Resetuje cały stan do wartości domyślnych |

---

## Komponenty wyświetlające wynik (`ui/components.py`)

Po otrzymaniu wyniku z `rag_query()` zakładka główna renderuje:

| Komponent | Warunek | Opis |
| --- | --- | --- |
| `render_answer_card(text, n, model)` | `result["text"] is not None` | Karta z tekstem odpowiedzi |
| `render_no_results()` | `result["text"] is None` | Komunikat o braku wyników |
| `render_source_chips(sources, show)` | źródła niepuste | Rząd chipów z nazwami plików |
| `render_chunk_expander(src, i, show)` | dla każdego źródła | Rozwijany panel z treścią fragmentu |

---

## Zmienne konfiguracyjne (`config/settings.py`)

Wartości które warto dostosować przy integracji z n8n:

| Stała | Wartość | Opis |
| --- | --- | --- |
| `DEFAULT_TOP_K` | `3` | Domyślna liczba fragmentów |
| `MIN_TOP_K` | `1` | Minimum slidera w sidebarze |
| `MAX_TOP_K` | `10` | Maksimum slidera w sidebarze |
| `SIMILARITY_THRESHOLD` | `0.45` | Próg odrzucania słabych wyników (używany w `generator.py`) |
| `DEFAULT_MODEL` | `"all-MiniLM-L6-v2"` | Nazwa modelu widoczna w UI |
