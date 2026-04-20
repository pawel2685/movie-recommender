````markdown
# CineRAG — Instructions for GitHub Copilot

## Project Context

**CineRAG** is a student movie recommendation system based on the RAG
(Retrieval-Augmented Generation) architecture. Dataset: TMDB 5000 (Kaggle).

The project is split into three modules assigned to three people:

| Module            | Folder                            | Owner    |
| ----------------- | --------------------------------- | -------- |
| Data & processing | `cine_rag/data/`                  | Person 1 |
| RAG engine        | `cine_rag/rag/`                   | Person 2 |
| App & tests       | `cine_rag/ui/`, `cine_rag/tests/` | Person 3 |

Application entry point: `cine_rag/main.py` (Streamlit).

---

<!-- ============================================================
     BLOCK 1 — PROJECT-WIDE RULES (apply to everyone)
     ============================================================ -->

## General Rules

- Code language: **Python 3.11+**, with type hints.
- Formatting: **Ruff** (linter + formatter) — PEP 8, max line length 100.
- Do not add unnecessary comments or docstrings to code that was not changed.
- Do not create new abstractions/helpers for one-off operations.
- Build all file paths with `pathlib.Path`, never with string concatenation.
- Secrets (API keys) only via environment variables or `.env` + `python-dotenv`. Never hardcoded.
- All variable names, function names, class names, and identifiers must be in English — no Polish characters (ą, ę, ó, ś, etc.) anywhere in code.
- Do not add comments inside code. Logic that needs explanation belongs in the separate documentation.
- Loggers must use plain text messages only — no icons, no decorators, no special formatting characters.

## Documentation Rules

- All project documentation (README files, module docs, analysis write-ups) must be written in **Polish**.
- Exception: this file (`copilot-instructions.md`) and all files in `.github/` stay in **English**.
- Documentation language style: academic but accessible — clear sentence structure, no jargon or fancy vocabulary where plain words suffice.
- Do not duplicate code logic in documentation — explain _why_, not _what_ the code does line by line.

## Markdown File Writing Rules

Follow these rules in all `.md` files in the project:

- **MD012** — At most one blank line in a row. Never two or more consecutive blank lines.
- **MD031** — A code block (` ``` `) must be surrounded by blank lines — one blank line before the opening fence and one after the closing fence.
- **MD060** — Table column separators must have spaces on both sides of the dashes: `| --- |`, not `|---|`.

Example of a correct table:

```markdown
| Column A | Column B |
| -------- | -------- |
| value 1  | value 2  |
```
````

Example of a correct code block:

```markdown
Text before the block.

\`\`\`python
print("hello")
\`\`\`

Text after the block.
```

---

<!-- ============================================================
     BLOCK 2 — TEAM STRUCTURE & AGENT FLOWS (per-person)
     ============================================================ -->

## Person 1 — Data Module (`cine_rag/data/`)

### File Scope

Person 1's files:

- `cine_rag/data/` — entire directory (raw, processed, chunks)
- Preprocessing scripts in `cine_rag/` root or `cine_rag/data/`

### LangChain Conventions (active for `cine_rag/data/**/*.py`)

When generating code for loading and splitting documents:

- Use `TextLoader` / `DirectoryLoader` from `langchain_community.document_loaders`
- Use `RecursiveCharacterTextSplitter` from `langchain_text_splitters` for chunking
- Represent documents as `langchain_core.documents.Document` (fields: `page_content`, `metadata`)
- `metadata` must contain: `source` (filename), `chunk_id` (int), `title` (movie title)
- Prefer batch encoding via `model.encode(texts, batch_size=64, show_progress_bar=True)`

### Default Parameters (from `config/settings.py`)

```python
CHUNK_SIZE = 500        # characters
CHUNK_OVERLAP = 50      # characters (10%)
BATCH_SIZE = 64         # encoding
```

### Available Agents for Person 1

Invoke in chat via `@agent-name`:

| Agent                             | When to use                                                     |
| --------------------------------- | --------------------------------------------------------------- |
| `@python-notebook-sample-builder` | Creating an EDA notebook for TMDB CSV                           |
| `@spark-performance`              | Optimizing pandas merge / slow data operations                  |
| `@context7`                       | Up-to-date API: pandas, LangChain, sentence-transformers, FAISS |

### Available Skills for Person 1

Invoke via `/skill-name` in chat:

| Skill                         | When to use                                        |
| ----------------------------- | -------------------------------------------------- |
| `/create-implementation-plan` | Before coding a new data module                    |
| `/autoresearch`               | Tuning chunk_size / chunk_overlap (automatic loop) |
| `/ruff-recursive-fix`         | Cleaning up code before committing                 |
| `/refactor`                   | Extracting pipeline stages as separate functions   |
| `/security-review`            | Audit before finalizing (path traversal, API keys) |

### Work Order (Person 1)

```
1. /create-implementation-plan       → plan the module
2. @python-notebook-sample-builder   → EDA TMDB in Jupyter
3. code with LangChain loader+splitter (langchain-python instruction active automatically)
4. @context7 pandas / langchain      → check up-to-date APIs
5. /autoresearch                     → tune chunk_size / overlap
6. /ruff-recursive-fix               → clean up code
7. /security-review                  → final audit
```

---

## Person 2 — RAG Engine (`cine_rag/rag/`)

> Section to be filled in.

---

## Person 3 — App & Tests (`cine_rag/ui/`, `cine_rag/tests/`)

> Section to be filled in.

---

## Copilot File Structure in This Repository

```
.github/
├── copilot-instructions.md          ← this file
├── agents/                          ← agents (Person 1)
│   ├── python-notebook-sample-builder.agent.md
│   ├── spark-performance.agent.md
│   └── context7.agent.md
├── instructions/                    ← automatically activated instructions
│   └── langchain-python.instructions.md   (glob: cine_rag/data/**/*.py)
└── prompts/                         ← skills (Person 1)
    ├── autoresearch/
    ├── create-implementation-plan/
    ├── ruff-recursive-fix/
    ├── refactor/
    └── security-review/
```

---

## Module Interfaces

Person 1 provides Person 2 with a list of `Document` objects (LangChain schema):

```python
# Data contract: Person 1 output → Person 2 input
from langchain_core.documents import Document

documents: list[Document] = [
    Document(
        page_content="Title: Inception\nDirector: Christopher Nolan\n...",
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
