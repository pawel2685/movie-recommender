# Dobrani asystenci AI — Projekt RAG Asystent Filmowy

> Przegląd dostępnych agentów, skilli i instrukcji z repozytorium `awesome-copilot`,
> Repo: <https://github.com/github/awesome-copilot>
> dobranych pod konkretne zadania każdej osoby. Priorytetem jest **Osoba 1**.

---

## Osoba 1 — Dane i Przetwarzanie

Zadania: EDA datasetu TMDB, merge CSV, konwersja do `.txt`, moduł ładowania plików,
czyszczenie tekstu, chunking dokumentów, pipeline indeksowania.

---

### 🤖 Agenci 1

#### `python-notebook-sample-builder` ★★★★★

**Plik:** `agents/python-notebook-sample-builder.agent.md`

Buduje gotowe notebooki Jupyter w VS Code z obsługą środowiska Python (instalacja pakietów,
konfiguracja kernela). Bezpośrednio przydatny do **notebooka EDA** — załaduje dane CSV,
policzy statystyki opisowe, wygeneruje wykresy rozkładu gatunków/ocen, a wszystko
jako interaktywny `.ipynb`.

**Zastosowanie u Osoby 1:**

- EDA datasetu TMDB 5000 (rozkład ocen, brakujące wartości, top gatunki)
- Notebook pokazujący wyniki mergu `tmdb_5000_movies.csv` + `tmdb_5000_credits.csv`
- Wizualizacja korpusu dokumentów po konwersji

**Jak użyć:** Otwórz nowy `.ipynb`, wpisz `@python-notebook-sample-builder` i opisz, co chcesz zbadać.

---

#### `spark-performance` (PySpark Expert) ★★★☆☆

**Plik:** `agents/spark-performance.agent.md`

Ekspert PySpark i pandas — diagnozuje bottlenecki, anty-patterny w przetwarzaniu danych,
radzi kiedy używać `pandas_udf` vs `.apply()`. Przydatny jeśli dataset rozrośnie się
powyżej kilkudziesięciu tysięcy filmów lub pipeline zacznie wolno działać.

**Zastosowanie u Osoby 1:**

- Optymalizacja mergu DataFrames pandas
- Vectorized string operations (czyszczenie tekstu bez pętli)
- Diagnoza wolnych fragmentów pipeline'u

---

#### `context7` ★★★★☆

**Plik:** `agents/context7.agent.md`

Dostarcza aktualną dokumentację dla dowolnej biblioteki (pandas, LangChain, sentence-transformers,
FAISS, qdrant-client). Zastępuje przestarzałą wiedzę modelu najświeższymi API.

**Zastosowanie u Osoby 1:**

- `@context7 pandas DataFrame.merge` — poprawna składnia merge z najnowszego API
- `@context7 langchain TextSplitter` — aktualne parametry chunkingu
- `@context7 sentence-transformers encode` — batch encoding dokumentów

---

### 📋 Instrukcje 1

#### `langchain-python` ★★★★★ — 1

**Plik:** `instructions/langchain-python.instructions.md`
**Zakres:** `**/*.py`

To najważniejsza instrukcja dla całego projektu, ale Osoba 1 skorzysta z niej głównie
przez komponenty do **ładowania dokumentów i chunkingu**:

| Komponent LangChain | Zadanie Osoby 1 |
| --- | --- |
| `TextLoader` / `DirectoryLoader` | moduł ładowania plików `.txt` z `data/raw/` |
| `RecursiveCharacterTextSplitter` | chunking z parametrami `chunk_size`, `chunk_overlap` |
| `Document` (schema) | ustandaryzowany format przenosiny danych do Osoby 2 |

Instrukcja aktywuje się automatycznie na plikach `.py` — Copilot będzie generował
kod zgodny z LangChain zamiast surowego Pythona.

---

### 🛠️ Skille 1

#### `autoresearch` ★★★★★

**Folder:** `skills/autoresearch/`

Autonomiczna pętla eksperymentalna: modyfikuj parametr → uruchom pipeline → zmierz wynik →
zachowaj/odrzuć zmianę. **Idealny do strojenia chunkingu.**

**Zastosowanie u Osoby 1:**

- Automatyczne szukanie optymalnego `chunk_size` (np. 300 vs 500 vs 800 znaków)
- Testowanie różnych wartości `chunk_overlap` (0%, 10%, 20%)
- Mierzenie metryk: liczba fragmentów, średnia długość, pokrycie treści

**Wymaganie:** Projekt musi być git repo + terminal dostępny w Copilot.

**Jak użyć:** Opisz cel ("chcę zminimalizować liczbę fragmentów poniżej 100 znaków")
i metrykę (komenda bash zwracająca liczbę). Skill uruchomi pętlę automatycznie.

---

#### `create-implementation-plan` ★★★★★

**Folder:** `skills/create-implementation-plan/`

Generuje szczegółowy plan implementacji w formacie zrozumiałym dla AI i ludzi.
Użyj **zanim zaczniesz kodować pipeline**.

**Zastosowanie u Osoby 1:**

- Wygeneruj plan modułu `data_loader.py` (kroki, edge cases, interfejs)
- Plan skryptu `run_indexing.py` — kolejność wywołań, obsługa błędów
- Plan czyszczenia tekstu — lista reguł z priorytetami

---

#### `ruff-recursive-fix` ★★★★☆

**Folder:** `skills/ruff-recursive-fix/`

Uruchamia Ruff (linter + formatter dla Pythona) iteracyjnie, stosuje bezpieczne poprawki
automatycznie, a pozostałe pokazuje do decyzji.

**Zastosowanie u Osoby 1:**

- Utrzymanie jakości kodu w `preprocessing.py`, `chunking.py`, `loader.py`
- Wykrycie nieużywanych importów, złych typów, f-string issues
- Wymuszenie PEP8 w całym module danych

---

#### `refactor` ★★★☆☆

**Folder:** `skills/refactor/`

Chirurgiczny refactoring bez zmiany zachowania: wydzielanie funkcji, lepsza nazewnictwo,
eliminacja duplikacji.

**Zastosowanie u Osoby 1:**

- Gdy skrypt pipeline'u urośnie i trzeba wydzielić etapy jako osobne funkcje
- Zamiana "bożego skryptu" na moduł z czystym interfejsem

---

#### `security-review` ★★★☆☆ — 1

**Folder:** `skills/security-review/`

Skaner bezpieczeństwa dla kodu Python. Warto uruchomić przed finalizacją projektu.

**Zastosowanie u Osoby 1:**

- Sprawdzenie czy ścieżki do plików są bezpieczne (path traversal)
- Brak hardcoded credentials do API (OpenAI key w kodzie)
- Bezpieczna obsługa zewnętrznych plików PDF

---

### 📌 Podsumowanie dla Osoby 1 — kolejność użycia

```text
1. create-implementation-plan     → zaplanuj pipeline zanim zaczniesz
2. python-notebook-sample-builder → EDA notebooka TMDB
3. langchain-python (instrukcja)  → koduj loader + chunker w LangChain
4. context7 (agent)               → sprawdzaj aktualne API na bieżąco
5. autoresearch (skill)           → strojenie parametrów chunk_size/overlap
6. ruff-recursive-fix             → sprzątanie kodu przed oddaniem
7. security-review                → audyt bezpieczeństwa na końcu
```

---

---

## Osoba 2 — Silnik RAG

Zadania: embedding modelu, baza wektorowa (Qdrant/FAISS), retrieval top-k, moduł odpowiedzi,
walidacja jakości (Nolan → filmy Nolana), opcjonalnie: LLM API.

---

### 🤖 Agenci 2

#### `comet-opik` ★★★★★

**Plik:** `agents/comet-opik.agent.md`

Kompleksowa observability dla aplikacji LLM: śledzenie traces, wersjonowanie promptów,
metryki eksperymentów. Odpowiada na pytanie "dlaczego system zwrócił złą odpowiedź?".

**Zastosowanie u Osoby 2:**

- Logowanie każdego zapytania: pytanie → embedding → top-k wyniki → odpowiedź
- Porównywanie modeli embeddingowych (all-MiniLM vs all-mpnet vs multilingual)
- Wykrywanie regresji jakości po zmianach parametrów

**Wymaganie:** Konto Comet.ml (darmowy tier dostępny).

---

#### `context7` ★★★★★

**Plik:** `agents/context7.agent.md`

**Zastosowanie u Osoby 2:**

- `@context7 qdrant-client Python` — aktualne SDK Qdrant
- `@context7 sentence-transformers` — batch embedding, modele wielojęzyczne
- `@context7 langchain retriever` — aktualne metody retrieval

---

### 📋 Instrukcje 2

#### `langchain-python` ★★★★★ — 2

**Plik:** `instructions/langchain-python.instructions.md`

Kluczowe komponenty dla Osoby 2:

- `VectorStore` (Qdrant, FAISS) — zapis/odczyt indeksu
- `Retriever` — zamiana pytania na wektor + similarity search
- `RetrievalQA` / `RAGChain` — łańcuch retrieval + odpowiedź
- Streaming odpowiedzi z LLM

---

### 🛠️ Skille 2

#### `qdrant-clients-sdk` ★★★★★

**Folder:** `skills/qdrant-clients-sdk/`

Oficjalny Python SDK Qdrant (`pip install qdrant-client[fastembed]`). Pokrywa:
kolekcje, upsert wektorów, wyszukiwanie, metadata filtering, batch operations.
Bezpośredni start z kodem dla Osoby 2.

#### `qdrant-search-quality` ★★★★★

**Folder:** `skills/qdrant-search-quality/`

Diagnozuje złe wyniki wyszukiwania. Skill wyjaśnia że większość problemów z jakością
pochodzi z modelu embeddingowego lub sposobu chunkowania — nie z konfiguracji Qdrant.
Zawiera strategie: exact search do izolacji problemu, tuning HNSW, hybrid search.

**Zastosowanie:** Gdy "filmy Nolana" zwracają filmy Spielberga.

#### `qdrant-deployment-options` ★★★★☆

**Folder:** `skills/qdrant-deployment-options/`

Pomaga wybrać tryb wdrożenia: local mode (Python, zero config), Docker (lokalny serwer),
lub Qdrant Cloud. Dla projektu studenckiego — **local mode lub Docker**.

#### `qdrant-model-migration` ★★★☆☆

**Folder:** `skills/qdrant-model-migration/`

Jak bezpiecznie zmienić model embeddingowy (np. z `all-MiniLM` na `multilingual-e5`).
Konieczna reindeksacja — skill prowadzi przez cały proces bez downtime.

#### `eval-driven-dev` ★★★★★

**Folder:** `skills/eval-driven-dev/`

Buduje automatyczny pipeline QA dla aplikacji Python z LLM: instrumentacja, golden dataset,
testy eval (LLM-as-judge), iteracja na błędach.

**Zastosowanie:** Zautomatyzowane testy walidacji "czy pytanie o Nolana zwraca filmy Nolana"
z mierzalną metryką trafności. Pokrywa halucynacje i poprawność źródeł.

#### `autoresearch` ★★★★☆

**Folder:** `skills/autoresearch/`

**Zastosowanie u Osoby 2:**

- Strojenie `top_k` (3 vs 5 vs 10 fragmentów)
- Testowanie progów similarity (filtrowanie nieistotnych wyników)
- Automatyczna optymalizacja parametrów HNSW

#### `phoenix-evals` ★★★☆☆

**Folder:** `skills/phoenix-evals/`

Alternatywny framework eval dla LLM aplikacji (Arize Phoenix). Ocena faithfulness
(czy odpowiedź jest wierna dokumentacji) i relevance (czy pobrane fragmenty pasują
do pytania).

---

---

## Osoba 3 — Aplikacja i Testy

Zadania: interfejs webowy (Streamlit/Gradio/Flask), sekcja źródeł, pytania testowe,
raport jakości, README, konfiguracja projektu.

---

### 🤖 Agenci 3

#### `playwright-tester` ★★★★★

**Plik:** `agents/playwright-tester.agent.md`
**Model:** Claude Sonnet 4

Eksploruje stronę jak użytkownik, następnie generuje testy Playwright (TypeScript).
Uruchamia testy i iteruje aż wszystkie przejdą.

**Zastosowanie u Osoby 3:**

- Automatyczne testy interfejsu: wpisz pytanie → sprawdź czy odpowiedź się pojawia
- Testy negatywne: pytanie bez odpowiedzi → sprawdź komunikat "Nie znaleziono..."
- Regresyjne testy UI przed oddaniem projektu

#### `debug` ★★★★☆

**Plik:** `agents/debug.agent.md`

Systematyczny debugging: zbiera kontekst błędu, reprodukuje, analizuje stack trace,
naprawia. Przydatny gdy integracja frontend ↔ silnik RAG nie działa.

---

### 📋 Instrukcje 3

#### `langchain-python` ★★★☆☆

**Plik:** `instructions/langchain-python.instructions.md`

Dla Osoby 3 przydatne przy streaming odpowiedzi do UI i formatowaniu źródeł.

---

### 🛠️ Skille 3

#### `webapp-testing` ★★★★★

**Folder:** `skills/webapp-testing/`

Testowanie lokalnych aplikacji webowych przez Playwright. Przeglądarka, screenshots,
logi konsoli, debugowanie UI.

**Zastosowanie:** Weryfikacja że Streamlit/Gradio poprawnie wyświetla fragmenty źródłowe
z nazwą dokumentu i numerem chunka.

#### `playwright-generate-test` ★★★★☆

**Folder:** `skills/playwright-generate-test/`

Generuje testy Playwright na podstawie scenariuszy opisanych naturalnym językiem.
Osoba 3 opisuje scenariusze testowe słownie, skill generuje kod.

#### `create-readme` ★★★★★

**Folder:** `skills/create-readme/`

Tworzy profesjonalny README na podstawie przeglądu całego projektu.
Inspiruje się opensourcowymi wzorcami (instalacja, uruchomienie, struktura, przykłady).

**Zastosowanie:** Finalny README projektu z instrukcją `pip install`, `python run_indexing.py`,
`streamlit run app.py`.

#### `documentation-writer` ★★★★☆

**Folder:** `skills/documentation-writer/`

Ekspert pisania dokumentacji technicznej wg frameworku Diátaxis (tutorials, how-to, reference, explanation).

**Zastosowanie:** Raport z testów (sekcja "wyjaśnienie" dlaczego pewne pytania działają gorzej),
instrukcja konfiguracji zmiennych środowiskowych.

#### `pytest-coverage` ★★★★☆

**Folder:** `skills/pytest-coverage/`

Uruchamia pytest z coverage, generuje raport annotated, wskazuje brakujące linie.

**Zastosowanie:** Weryfikacja pokrycia testami modułów pipeline'u danych i silnika RAG.

#### `web-coder` ★★★★☆

**Folder:** `skills/web-coder/`

Ekspert web developmentu (HTML, CSS, JS, APIs, HTTP, CORS). Pomocny przy budowie
interfejsu jeśli nie Streamlit, lecz customowy Flask/FastAPI + frontend.

#### `premium-frontend-ui` ★★★☆☆

**Folder:** `skills/premium-frontend-ui/`

Zaawansowany przewodnik UI: animacje, typografia, design system. Opcjonalne "lepszy wygląd UI"
z zadań Osoby 3.

#### `eval-driven-dev` ★★★★☆

**Folder:** `skills/eval-driven-dev/`

Współdzielony z Osobą 2. Osoba 3 może użyć do zautomatyzowania swoich 15–20 pytań
testowych jako uruchamialnego benchmarku z pass/fail.

#### `security-review` ★★★☆☆ — 3

**Folder:** `skills/security-review/`

Audyt bezpieczeństwa aplikacji webowej: XSS, injection, exposed keys,
insecure dependencies.

---

---

## Zasoby Wspólne dla Całego Zespołu

| Zasób | Typ | Kiedy użyć |
| --- | --- | --- |
| `skills/create-implementation-plan/` | Skill | Przed startem każdego modułu |
| `skills/create-specification/` | Skill | Zdefiniowanie interfejsów między modułami |
| `skills/code-tour/` | Skill | Onboarding — prezentacja architektury projektu |
| `agents/research-technical-spike.agent.md` | Agent | Badanie nowej technologii (np. czy FAISS vs Qdrant) |
| `agents/principal-software-engineer.agent.md` | Agent | Decyzje architektoniczne (struktura katalogów, interfejsy) |
| `agents/context7.agent.md` | Agent | Aktualne dokumentacje dowolnej biblioteki |
| `instructions/langchain-python.instructions.md` | Instrukcja | Aktywna automatycznie na `*.py` w całym projekcie |
| `instructions/security-and-owasp.instructions.md` | Instrukcja | Standardy bezpieczeństwa |
| `skills/refactor/` | Skill | Czyszczenie kodu każdego modułu |

---

## Mapa stack → zasoby

```text
TMDB CSV
   └── pandas merge          ← context7, spark-performance
       └── txt docs           ← python-notebook-sample-builder (EDA)
           └── LangChain loader/splitter  ← langchain-python (instrukcja)
               └── chunk tuning           ← autoresearch
                   └── Qdrant (embeddings + index)
                       ├── qdrant-clients-sdk
                       ├── qdrant-deployment-options
                       ├── qdrant-search-quality ← gdy złe wyniki
                       └── qdrant-model-migration ← gdy zmiana modelu
                           └── RAG chain (retrieval + answer)
                               ├── comet-opik     ← obserwability
                               ├── eval-driven-dev ← testy jakości
                               └── Streamlit/Flask UI
                                   ├── web-coder / premium-frontend-ui
                                   ├── playwright-tester
                                   ├── webapp-testing
                                   └── create-readme + documentation-writer
```
