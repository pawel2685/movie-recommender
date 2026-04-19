# CineRAG — Instrukcje dla GitHub Copilot

## Kontekst projektu

**CineRAG** to studencki system rekomendacji filmów oparty na architekturze RAG
(Retrieval-Augmented Generation). Dataset: TMDB 5000 (Kaggle).

Projekt jest podzielony na trzy moduły przypisane trzem osobom:

| Moduł                | Folder                            | Właściciel |
| -------------------- | --------------------------------- | ---------- |
| Dane i przetwarzanie | `cine_rag/data/`                  | Osoba 1    |
| Silnik RAG           | `cine_rag/rag/`                   | Osoba 2    |
| Aplikacja i testy    | `cine_rag/ui/`, `cine_rag/tests/` | Osoba 3    |

Punkt startowy aplikacji: `cine_rag/main.py` (Streamlit).

---

## Zasady ogólne

- Język kodu: **Python 3.11+**, z type hints.
- Formatowanie: **Ruff** (linter + formatter) — PEP 8, max line length 100.
- Nie dodawaj zbędnych komentarzy ani docstringów do kodu, który nie był zmieniany.
- Nie twórz nowych abstrakcji/helperów dla jednorazowych operacji.
- Wszystkie ścieżki do plików buduj przez `pathlib.Path`, nigdy przez string concatenation.
- Sekrety (klucze API) wyłącznie przez zmienne środowiskowe lub `.env` + `python-dotenv`. Nigdy hardcoded.

---

## Osoba 1 — Moduł danych (`cine_rag/data/`)

### Zakres plików

Pliki Osoby 1:

- `cine_rag/data/` — cały katalog (raw, processed, chunks)
- Skrypty preprocessing w katalogu głównym `cine_rag/` lub `cine_rag/data/`

### Konwencje LangChain (aktywne na `cine_rag/data/**/*.py`)

Gdy generujesz kod do ładowania i podziału dokumentów:

- Używaj `TextLoader` / `DirectoryLoader` z `langchain_community.document_loaders`
- Do chunkingu stosuj `RecursiveCharacterTextSplitter` z `langchain_text_splitters`
- Dokumenty reprezentuj jako `langchain_core.documents.Document` (pola: `page_content`, `metadata`)
- `metadata` musi zawierać: `source` (nazwa pliku), `chunk_id` (int), `title` (tytuł filmu)
- Preferuj batch encoding przez `model.encode(texts, batch_size=64, show_progress_bar=True)`

### Domyślne parametry (z `config/settings.py`)

```python
CHUNK_SIZE = 500        # znaki
CHUNK_OVERLAP = 50      # znaki (10%)
BATCH_SIZE = 64         # encoding
```

### Dostępne agenci dla Osoby 1

Wywołuj w chat przez `@nazwa-agenta`:

| Agent                             | Kiedy używać                                                  |
| --------------------------------- | ------------------------------------------------------------- |
| `@python-notebook-sample-builder` | Tworzenie notebooka EDA dla TMDB CSV                          |
| `@spark-performance`              | Optymalizacja pandas merge / wolne operacje na danych         |
| `@context7`                       | Aktualne API: pandas, LangChain, sentence-transformers, FAISS |

### Dostępne skille dla Osoby 1

Wywołuj przez `/nazwa-skilla` w chat:

| Skill                         | Kiedy używać                                              |
| ----------------------------- | --------------------------------------------------------- |
| `/create-implementation-plan` | Zanim zaczniesz kodować nowy moduł danych                 |
| `/autoresearch`               | Strojenie chunk_size / chunk_overlap (pętla automatyczna) |
| `/ruff-recursive-fix`         | Czyszczenie kodu przed commitem                           |
| `/refactor`                   | Wydzielanie etapów pipeline jako osobne funkcje           |
| `/security-review`            | Audyt przed finalizacją (path traversal, klucze API)      |

### Kolejność pracy (Osoba 1)

```
1. /create-implementation-plan  → zaplanuj moduł
2. @python-notebook-sample-builder → EDA TMDB w Jupyter
3. kod z LangChain loader+splitter  (instrukcja langchain-python aktywna automatycznie)
4. @context7 pandas / langchain     → sprawdzaj aktualne API
5. /autoresearch                    → strojenie chunk_size / overlap
6. /ruff-recursive-fix              → porządkowanie kodu
7. /security-review                 → audyt końcowy
```

---

## Struktura plików Copilot w tym repozytorium

```
.github/
├── copilot-instructions.md          ← ten plik
├── agents/                          ← agenci (Osoba 1)
│   ├── python-notebook-sample-builder.agent.md
│   ├── spark-performance.agent.md
│   └── context7.agent.md
├── instructions/                    ← instrukcje aktywowane automatycznie
│   └── langchain-python.instructions.md   (glob: cine_rag/data/**/*.py)
└── prompts/                         ← skille (Osoba 1)
    ├── autoresearch/
    ├── create-implementation-plan/
    ├── ruff-recursive-fix/
    ├── refactor/
    └── security-review/
```

---

## Interfejsy między modułami

Osoba 1 dostarcza Osobie 2 listę obiektów `Document` (LangChain schema):

```python
# Kontrakt danych: wyjście Osoby 1 → wejście Osoby 2
from langchain_core.documents import Document

documents: list[Document] = [
    Document(
        page_content="Tytuł: Inception\nReżyser: Christopher Nolan\n...",
        metadata={
            "source": "inception.txt",
            "chunk_id": 0,
            "title": "Inception",
            "year": 2010,
            "genres": ["Action", "Sci-Fi"],
        },
    )
]
```

Osoba 2 przyjmuje tę listę i buduje na niej indeks wektorowy.
