# 🎬 CineRAG — Asystent RAG do dokumentacji filmowej

> System AI odpowiadający na pytania o filmach wyłącznie na podstawie dostarczonej dokumentacji (TMDB 5000).  
> Projekt studencki — podział pracy na 3 osoby.

---

## Spis treści

1. [Opis projektu](#opis-projektu)
2. [Struktura projektu](#struktura-projektu)
3. [Instalacja i uruchomienie](#instalacja-i-uruchomienie)
4. [Flow działania aplikacji](#flow-działania-aplikacji)
5. [Podział pracy](#podział-pracy)
6. [Deliverables](#deliverables)

---

## Opis projektu

**CineRAG** to aplikacja webowa oparta na architekturze **Retrieval-Augmented Generation (RAG)**.  
System odpowiada na pytania dotyczące filmów, korzystając wyłącznie z przetworzonej dokumentacji zbioru danych TMDB 5000.  
Interfejs użytkownika zbudowany jest w **Streamlit**, wyszukiwanie wektorowe oparte jest na **FAISS** lub **ChromaDB**, a embeddingi generowane są przez **Sentence Transformers**.

---

## Struktura projektu

```
cine_rag/
│
├── main.py                     # punkt startowy Streamlit
│
├── ui/                         # cały frontend
│   ├── __init__.py
│   ├── layout.py               # header, hero, sidebar
│   ├── styles.py               # CSS
│   ├── components.py           # karty, chipy, fragmenty
│   └── tabs/
│       ├── tab_main.py         # zakładka "Zapytaj"
│       ├── tab_tests.py        # zakładka "Testy"
│       └── tab_about.py        # zakładka "O projekcie"
│
├── rag/                        # logika RAG
│   ├── __init__.py
│   ├── engine.py               # główna funkcja rag_query()
│   ├── embeddings.py           # model embeddingów
│   ├── retriever.py            # wyszukiwanie (FAISS)
│   └── generator.py            # składanie odpowiedzi
│
├── data/                       # dane i preprocessing
│   ├── raw/                    # surowe pliki CSV
│   ├── processed/              # przetworzone dokumenty + indeks
│   └── chunks/                 # fragmenty dokumentów
│
├── tests/
│   ├── test_rag.py
│   ├── test_ui_logic.py
│   └── sample_questions.py
│
├── utils/
│   ├── __init__.py
│   ├── session.py              # zarządzanie session_state
│   └── helpers.py
│
├── config/
│   ├── settings.py             # stałe (top_k, modele itd.)
│   └── constants.py
│
└── requirements.txt
```

---

## Instalacja i uruchomienie

### 1. Sklonuj repozytorium

```bash
git clone <url-repozytorium>
cd movie-recommender
```

### 2. Utwórz środowisko wirtualne i zainstaluj zależności

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

pip install -r cine_rag/requirements.txt
```

### 3. Uruchom indeksowanie danych (jednorazowo)

Umieść pliki CSV (TMDB 5000) w katalogu `cine_rag/data/raw/`, a następnie uruchom pipeline indeksowania (skrypt dostarczony przez Osobę 1).

### 4. Uruchom aplikację

```bash
streamlit run cine_rag/main.py
```

### 5. Uruchom testy

Konfiguracja pytest znajduje się w `pytest.ini` w katalogu głównym projektu.
Ustawia `pythonpath = cine_rag`, dzięki czemu wszystkie testy działają poprawnie bez ręcznej modyfikacji `sys.path`.

Uruchomienie wszystkich testów:

```bash
pytest
```

Uruchomienie testów konkretnego modułu:

```bash
pytest cine_rag/tests/test_preprocessing.py -v
pytest cine_rag/tests/test_rag.py -v
pytest cine_rag/tests/test_ui_logic.py -v
```

Dostępne pliki testów:

| Plik | Zakres |
| --- | --- |
| `tests/test_preprocessing.py` | Moduł danych — parsowanie, czyszczenie, merge, DataFrame |
| `tests/test_rag.py` | Silnik RAG — `rag_query()`, retrieval, top-k |
| `tests/test_ui_logic.py` | Logika UI — walidacja wejść, stan sesji |
| `tests/sample_questions.py` | Zestaw pytań testowych (nie test automatyczny) |

---

## Flow działania aplikacji

### Indeksowanie (jednorazowo, offline)

```
Dataset filmowy (CSV)
  → EDA & Merge (eksploracja, łączenie)
  → Dokumenty .txt (1 film = 1 plik)
  → Cleaning (preprocessing.py)
  → Chunking (podział na fragmenty)
  → Embeddingi (tekst → wektory)
  → Baza wektorowa (indeks FAISS) + Metadane
```

### Zapytanie (w czasie rzeczywistym)

```
Użytkownik wpisuje pytanie (np. "Filmy Nolana?")
  → Interfejs webowy (Streamlit)
  → Embed pytania (pytanie → wektor)
  → Wyszukiwanie (top-k najbardziej pasujących fragmentów)
  → Składanie odpowiedzi (tekst + źródła)
  → Wynik wyświetlony na ekranie
```

---

## Podział pracy

### 🗂️ Osoba 1 — Dane i przetwarzanie

- Pobranie datasetu filmowego (TMDB 5000 z Kaggle) i wstępna eksploracja danych (EDA)
- Łączenie i przetwarzanie danych źródłowych — ekstrakcja gatunków, obsady, reżysera
- Konwersja każdego filmu do dokumentu tekstowego (tytuł, opis, obsada, gatunki, ocena)
- Napisanie modułu ładowania plików — obsługa formatów `.txt` i `.pdf`
- Czyszczenie tekstu — usunięcie zbędnych znaków bez utraty kluczowych informacji
- Podział dokumentów na fragmenty (chunking) — dobór rozmiaru i nakładki (overlap)
- Skrypt pipeline'u indeksowania — uruchomienie całego procesu jedną komendą

**Obszar technologiczny:** Python, przetwarzanie danych, ekstrakcja tekstu

---

### 🧠 Osoba 2 — Silnik RAG

- Integracja modelu embeddingowego — zamiana tekstu na wektory liczbowe
- Budowa bazy wektorowej — zapis i odczyt indeksu oraz metadanych
- Moduł wyszukiwania — zamiana pytania na wektor, znalezienie najbardziej pasujących fragmentów (top-k)
- Moduł odpowiedzi — składanie odpowiedzi z fragmentów i dołączanie źródeł
- Komunikat „Nie znaleziono informacji w dokumentacji" gdy brak trafień
- Strojenie parametrów — dobór liczby zwracanych fragmentów, testowanie trafności
- Walidacja jakości — czy pytanie o Nolana zwraca filmy Nolana, nie Tarantino
- Opcjonalnie: integracja z LLM API do generowania odpowiedzi naturalnym językiem

**Obszar technologiczny:** Python, embeddingi, baza wektorowa

---

### 🖥️ Osoba 3 — Aplikacja i testy

- Interfejs użytkownika — pole pytania, przycisk, wyświetlanie odpowiedzi i źródeł
- Sekcja źródeł — wyświetlanie nazwy dokumentu, numeru fragmentu i treści
- Przygotowanie 15–20 pytań testowych w 4 kategoriach: faktograficzne, porównawcze, proceduralne, negatywne
- Testowanie jakości — trafność odpowiedzi, brak halucynacji, poprawność źródeł
- Dokumentacja projektu — instrukcja instalacji i uruchomienia (README)
- Konfiguracja projektu — lista zależności, zmienne środowiskowe, struktura katalogów
- Raport z testów — które pytania działają dobrze, które źle i dlaczego
- Opcjonalnie: historia pytań w sesji, lepszy wygląd UI

**Obszar technologiczny:** Python, interfejs webowy, testowanie

---

## Deliverables

| Osoba   | Plik / artefakt              | Opis                             |
| ------- | ---------------------------- | -------------------------------- |
| Osoba 1 | `data/raw/`                  | Surowe pliki CSV (TMDB 5000)     |
| Osoba 1 | `data/processed/`            | Przetworzone dokumenty `.txt`    |
| Osoba 1 | `data/chunks/`               | Fragmenty gotowe do indeksowania |
| Osoba 1 | `data/processed/faiss.index` | Zbudowany indeks wektorowy       |
| Osoba 1 | skrypt pipeline              | Jednokomendowe indeksowanie      |
| Osoba 2 | `rag/engine.py`              | Główna funkcja `rag_query()`     |
| Osoba 2 | `rag/embeddings.py`          | Załadowany model embeddingów     |
| Osoba 2 | `rag/retriever.py`           | Wyszukiwanie top-k w indeksie    |
| Osoba 2 | `rag/generator.py`           | Składanie odpowiedzi i źródeł    |
| Osoba 3 | `ui/` + `main.py`            | Działająca aplikacja Streamlit   |
| Osoba 3 | `tests/sample_questions.py`  | Zestaw pytań testowych           |
| Osoba 3 | `tests/test_rag.py`          | Testy jednostkowe RAG            |
| Osoba 3 | `README.md`                  | Dokumentacja projektu            |

---

_Projekt RAG — Asystent Filmowy · System AI do obsługi zamkniętej dokumentacji · 2026_
