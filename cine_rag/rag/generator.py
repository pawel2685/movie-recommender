"""
rag/generator.py
Składanie odpowiedzi z pobranych fragmentów dokumentów.
Osoba 2 implementuje generate() — opcjonalnie z wywołaniem LLM API.
"""

from __future__ import annotations
from .retriever import RetrievedChunk
from config.settings import SIMILARITY_THRESHOLD


# ── WYNIK ZAPYTANIA ───────────────────────────────────────────────────────────
class QueryResult:
    """
    Rezultat pojedynczego zapytania do systemu RAG.
    text == None oznacza "Nie znaleziono informacji w dokumentacji".
    """

    def __init__(self, text: str | None, sources: list[RetrievedChunk]):
        self.text    = text
        self.sources = sources

    def found(self) -> bool:
        return self.text is not None

    def to_dict(self) -> dict:
        """Konwertuje do formatu oczekiwanego przez UI."""
        return {
            "text": self.text,
            "sources": [
                {
                    "file":  s.file,
                    "chunk": s.chunk,
                    "score": s.score,
                    "text":  s.text,
                }
                for s in self.sources
            ],
        }


# ── GENERATOR ─────────────────────────────────────────────────────────────────
def generate_answer(question: str, chunks: list[RetrievedChunk]) -> QueryResult:
    """
    Składa odpowiedź na podstawie listy pobranych fragmentów.

    Wariant A (domyślny): konkatenacja fragmentów bez LLM.
    Wariant B (opcjonalny): przekazanie kontekstu do LLM API.

    Args:
        question: oryginalne pytanie użytkownika
        chunks:   lista fragmentów zwrócona przez Retriever.search()

    Returns:
        QueryResult z tekstem odpowiedzi i listą źródeł.
    """
    # Odfiltruj fragmenty poniżej progu podobieństwa
    valid = [c for c in chunks if c.score >= SIMILARITY_THRESHOLD]

    if not valid:
        return QueryResult(text=None, sources=[])

    # ── Wariant A: prosta konkatenacja ────────────────────────────────────────
    answer = _assemble_from_chunks(question, valid)

    # ── Wariant B: LLM API (odkomentuj gdy dostępne) ─────────────────────────
    # answer = _call_llm(question, valid)

    return QueryResult(text=answer, sources=valid)


def _assemble_from_chunks(question: str, chunks: list[RetrievedChunk]) -> str:
    """Buduje czytelną odpowiedź przez złożenie tekstów fragmentów."""
    titles = ", ".join(
        c.file.replace("_", " ").replace(".txt", "").title()
        for c in chunks
    )
    intro = (
        f"Na podstawie dostępnej dokumentacji filmowej znaleziono "
        f"{len(chunks)} powiązanych fragmentów dotyczących pytania: "
        f"*{question}*\n\n"
        f"**Powiązane filmy:** {titles}"
    )
    return intro


# ── WARIANT B: SZKIELET LLM ───────────────────────────────────────────────────
# def _call_llm(question: str, chunks: list[RetrievedChunk]) -> str:
#     import openai
#     context = "\n\n".join(f"[{c.file} #{c.chunk}]\n{c.text}" for c in chunks)
#     prompt  = (
#         f"Odpowiedz na pytanie wyłącznie na podstawie poniższej dokumentacji.\n"
#         f"Jeśli odpowiedź nie wynika z dokumentacji, napisz: "
#         f"'Nie znaleziono informacji w dokumentacji'.\n\n"
#         f"DOKUMENTACJA:\n{context}\n\n"
#         f"PYTANIE: {question}\n\nODPOWIEDŹ:"
#     )
#     response = openai.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=512,
#     )
#     return response.choices[0].message.content.strip()
