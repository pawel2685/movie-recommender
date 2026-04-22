# Osoba 1 — Dane i przetwarzanie: Plan implementacji

## Zakres pracy (z README)

| Zadanie | Plik wyjściowy |
| --- | --- |
| EDA datasetu TMDB 5000 | notebook `eda_tmdb.ipynb` |
| Merge i preprocessing CSV | `data/preprocessing.py` |
| Konwersja filmów → pliki `.txt` | `data/processed/*.txt` |
| Czyszczenie tekstu | `data/preprocessing.py` |
| Ładowanie dokumentów (LangChain) | `data/loader.py` |
| Chunking dokumentów | `data/chunker.py` |
| Embeddingi + indeks FAISS | `data/indexer.py` |
| Pipeline jednokomendowy | `data/build_index.py` |

---

## Krok 0 — Przygotowanie danych wejściowych

**Cel:** pobrać dataset i umieścić pliki CSV w odpowiednim miejscu.

1. Pobierz dataset **TMDB 5000** z Kaggle:
   - `tmdb_5000_movies.csv`
   - `tmdb_5000_credits.csv`
2. Umieść oba pliki w: `cine_rag/data/raw/`
3. Uzupełnij `config/settings.py` o brakujące stałe:

```python
# Chunking
CHUNK_SIZE: int = 500
CHUNK_OVERLAP: int = 50

# Encoding
BATCH_SIZE: int = 64
```

**Output:** dwa pliki CSV w `data/raw/`, uzupełniony `settings.py`.

---

## Krok 1 — EDA w Jupyter Notebook

**Plik:** `eda_tmdb.ipynb` (w katalogu `data/pre-processing/`)

**Cel:** zrozumieć strukturę danych przed pisaniem kodu produkcyjnego.

Sprawdź:

- kształt i typy kolumn obu CSV
- null values (szczególnie `overview`, `genres`, `cast`, `crew`)
- przykładowe wartości kolumn JSON (`genres`, `keywords`, `cast`, `crew`) — są zapisane jako stringi, wymagają `ast.literal_eval`
- rozkład: długość `overview`, liczba filmów na gatunek, lata produkcji
- identyfikator łączący oba pliki: `movies.id` ↔ `credits.movie_id`

**Nie implementuj** logiki produkcyjnej w notebooku — tylko eksploracja.

---

## Krok 2 — Merge i preprocessing CSV

**Plik:** `cine_rag/data/preprocessing.py`

**Cel:** z surowych CSV wyprodukować czysty DataFrame, jeden wiersz = jeden film.

Funkcje do implementacji:

```python
def load_raw_data(raw_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Wczytaj movies.csv i credits.csv."""

def merge_datasets(movies_df: pd.DataFrame, credits_df: pd.DataFrame) -> pd.DataFrame:
    """Połącz po kolumnie id / movie_id."""

def extract_genres(genres_json: str) -> list[str]:
    """Parsuj JSON → lista nazw gatunków (maks. 5)."""

def extract_cast(cast_json: str, top_n: int = 5) -> list[str]:
    """Parsuj JSON → lista nazwisk aktorów (top N po order)."""

def extract_director(crew_json: str) -> str:
    """Parsuj JSON → imię i nazwisko reżysera (job == 'Director')."""

def clean_text(text: str) -> str:
    """Usuń znaki specjalne, znormalizuj whitespace. Zachowaj litery, cyfry, podstawową interpunkcję."""

def build_clean_dataframe(raw_dir: Path) -> pd.DataFrame:
    """Orkiestracja: load → merge → extract → clean. Zwraca gotowy DataFrame."""
```

**Wymagane kolumny wyjściowego DataFrame:**
`title`, `overview`, `genres`, `cast`, `director`, `vote_average`, `release_year`

**Output:** `pd.DataFrame` gotowy do konwersji na dokumenty.

---

## Krok 3 — Konwersja filmów → pliki `.txt`

**Plik:** `cine_rag/data/preprocessing.py` (dodaj funkcję)

**Cel:** 1 wiersz DataFrame = 1 plik `.txt` w `data/processed/`.

Format pliku (szablon):

Tytuł: {title}
Rok: {release_year}
Gatunki: {genres_joined}
Reżyser: {director}
Obsada: {cast_joined}
Ocena: {vote_average}/10

Opis:
{overview}

Funkcja:

```python
def save_documents_as_txt(df: pd.DataFrame, processed_dir: Path) -> None:
    """Zapisz każdy film jako osobny plik .txt. Nazwa pliku: slugified title."""
```

Nazwy plików: tytuł małymi literami, spacje → podkreślniki, bez znaków specjalnych.
Przykład: `inception_2010.txt`

**Output:** pliki `data/processed/*.txt`, jeden na film.

---

## Krok 4 — Ładowanie dokumentów (LangChain)

**Plik:** `cine_rag/data/loader.py`

**Cel:** wczytać pliki `.txt` jako obiekty `Document` z LangChain.

```python
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from pathlib import Path

def load_documents(processed_dir: Path) -> list[Document]:
    """
    Wczytaj wszystkie .txt z processed_dir.
    Każdy Document ma metadata: source (nazwa pliku), title (z nazwy pliku).
    """
    loader = DirectoryLoader(
        str(processed_dir),
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    return loader.load()
```

**Output:** `list[Document]` z wypełnionym `page_content` i bazowym `metadata`.

---

## Krok 5 — Chunking dokumentów

**Plik:** `cine_rag/data/chunker.py`

**Cel:** podzielić dokumenty na fragmenty gotowe do embeddingu.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

def split_documents(documents: list[Document]) -> list[Document]:
    """
    Podziel dokumenty na fragmenty.
    Uzupełnij metadata każdego chunka: chunk_id (int), title (z source).
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
        # title: wyodrębnij z metadata["source"] jeśli nie ustawiony
    return chunks
```

**Wymagany schemat `metadata` każdego chunka:**

```python
{
    "source": "inception_2010.txt",   # nazwa pliku
    "chunk_id": 0,                    # int, globalny indeks
    "title": "Inception",             # tytuł filmu
}
```

Opcjonalnie (jeśli dostępne w DataFrame): `year`, `genres`.

**Output:** `list[Document]` — fragmenty gotowe do embeddingu.

---

## Krok 6 — Embeddingi i indeks FAISS

**Plik:** `cine_rag/data/indexer.py`

**Cel:** zamienić chunki na wektory i zapisać indeks FAISS + metadane.

```python
from sentence_transformers import SentenceTransformer
import faiss, json, numpy as np
from pathlib import Path
from langchain_core.documents import Document
from config.settings import EMBEDDING_MODEL_NAME, BATCH_SIZE, VECTOR_STORE_PATH, PROCESSED_DIR

def build_faiss_index(chunks: list[Document]) -> None:
    """
    1. Zakoduj page_content wszystkich chunków (batch encoding).
    2. Zbuduj indeks FAISS (IndexFlatL2).
    3. Zapisz: faiss.index + metadata.json do PROCESSED_DIR.
    """
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    texts = [c.page_content for c in chunks]
    embeddings = model.encode(texts, batch_size=BATCH_SIZE, show_progress_bar=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings, dtype="float32"))

    faiss.write_index(index, str(VECTOR_STORE_PATH))

    metadata = [c.metadata for c in chunks]
    with open(PROCESSED_DIR / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
```

**Output:**

- `data/processed/faiss.index` — indeks wektorowy
- `data/processed/metadata.json` — metadane chunków (lista dict)

---

## Krok 7 — Pipeline jednokomendowy

**Plik:** `cine_rag/data/build_index.py`

**Cel:** uruchomienie pełnego pipeline'u jedną komendą: `python -m cine_rag.data.build_index`

```python
from pathlib import Path
from config.settings import RAW_DIR, PROCESSED_DIR, CHUNKS_DIR

from cine_rag.data.preprocessing import build_clean_dataframe, save_documents_as_txt
from cine_rag.data.loader import load_documents
from cine_rag.data.chunker import split_documents
from cine_rag.data.indexer import build_faiss_index

def main() -> None:
    print("1/4 Preprocessing CSV...")
    df = build_clean_dataframe(RAW_DIR)
    save_documents_as_txt(df, PROCESSED_DIR)

    print("2/4 Ładowanie dokumentów...")
    documents = load_documents(PROCESSED_DIR)

    print("3/4 Chunking...")
    chunks = split_documents(documents)

    print("4/4 Budowanie indeksu FAISS...")
    build_faiss_index(chunks)

    print("Gotowe. Indeks zapisany w data/processed/")

if __name__ == "__main__":
    main()
```

**Output:** gotowa baza wektorowa dla Osoby 2.

---

## Kontrakt z Osobą 2

Osoba 2 oczekuje:

- pliku `data/processed/faiss.index`
- pliku `data/processed/metadata.json` (lista dict z polami: `source`, `chunk_id`, `title`)
- modelu embeddinów identycznego z tym z `config/settings.py` (`EMBEDDING_MODEL_NAME`)

Alternatywnie: Osoba 2 może wywołać `split_documents()` z `chunker.py` i skorzystać z `list[Document]` bezpośrednio.

---

## Kolejność implementacji

Krok 0 → settings.py + CSV w raw/
Krok 1 → EDA notebook
Krok 2 → preprocessing.py (merge, extract, clean)
Krok 3 → preprocessing.py (save_documents_as_txt)
Krok 4 → loader.py
Krok 5 → chunker.py
Krok 6 → indexer.py
Krok 7 → build_index.py

---

## Checklist przed oddaniem

- [ ] `data/raw/` zawiera oba pliki CSV
- [ ] `data/processed/` zawiera pliki `.txt` (jeden na film)
- [ ] `data/processed/faiss.index` istnieje
- [ ] `data/processed/metadata.json` istnieje, każdy wpis ma `source`, `chunk_id`, `title`
- [ ] `python -m cine_rag.data.build_index` działa od zera
- [ ] Brak hardcoded ścieżek — wszystko przez `pathlib.Path` i `config/settings.py`
- [ ] Brak hardcoded kluczy API
- [ ] Ruff nie zgłasza błędów (`ruff check cine_rag/data/`)
