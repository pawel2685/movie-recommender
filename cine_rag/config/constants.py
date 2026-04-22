"""
config/constants.py
Stałe dane aplikacji — pytania testowe, role, stack technologiczny.
Nie zawiera parametrów konfigurowalnych (te są w settings.py).
"""

# ── PYTANIA TESTOWE ───────────────────────────────────────────────────────────
SAMPLE_QUESTIONS: dict[str, list[str]] = {
    "🎯 Faktograficzne": [
        "Jakie filmy wyreżyserował Christopher Nolan?",
        "Kto zagrał główną rolę w Gladiatorze?",
        "Jaka jest ocena IMDb filmu Parasite?",
        "W którym roku powstał film Pulp Fiction?",
        "Jaki jest budżet filmu Avatar?",
    ],
    "⚖️ Porównawcze": [
        "Porównaj filmy Nolana i Tarantino pod kątem stylu narracji.",
        "Który film ma wyższą ocenę: Interstellar czy Inception?",
        "Czym różni się Joker (2019) od The Dark Knight?",
        "Porównaj obsadę The Departed i Inception.",
    ],
    "🎬 Fabuła i Tematyka": [
        "Jak wyjaśnić fabułę Memento w skrócie?",
        "Opisz główne motywy w filmie Fight Club.",
        "O czym opowiada film The Shawshank Redemption?",
        "Wyjaśnij zakończenie filmu Inception.",
    ],
    "🚫 Poza Zakresem": [
        "Jakie filmy wyreżyserował Steven Spielberg?",
        "Jaka jest dzisiaj pogoda w Warszawie?",
        "Podaj przepis na pizzę margherita.",
        "Kto wygrał wybory w USA w 2024 roku?",
    ],
}

CATEGORY_COLORS: dict[str, str] = {
    "🎯 Faktograficzne": "#3b82f6",
    "⚖️ Porównawcze":    "#a855f7",
    "🎬 Fabuła i Tematyka": "#22c55e",
    "🚫 Poza Zakresem":    "#ef4444",
}

# ── QUICK QUESTIONS (pasek skrótów w zakładce Zapytaj) ───────────────────────
QUICK_QUESTIONS: list[str] = [
    "Filmy Christophera Nolana?",
    "Najwyżej oceniane thrillery?",
    "Obsada Pulp Fiction?",
]

# ── PODZIAŁ PRACY ─────────────────────────────────────────────────────────────
TEAM_ROLES: list[tuple[str, str, str, str, str]] = [
    # (icon, label, name, desc, color)
    ("🗂️", "Osoba 1 - Paweł Magda", "Dane i przetwarzanie",
     "EDA · chunking · pipeline indeksowania", "#3b82f6"),
    ("🧠", "Osoba 2 - Jakub Łudzeń", "Silnik RAG",
     "Embeddingi · baza wektorowa · retrieval", "#a855f7"),
    ("🖥️", "Osoba 3 - Jakub Kuszper", "Aplikacja i testy",
     "Interfejs · dokumentacja · raport testów", "#22c55e"),
]

# ── STACK TECHNOLOGICZNY ──────────────────────────────────────────────────────
TECH_STACK: list[tuple[str, list[tuple[str, str]]]] = [
    ("Dane", [
        ("Python 3.11", "#3b82f6"),
        ("pandas",      "#3b82f6"),
        ("TMDB 5000",   "#3b82f6"),
    ]),
    ("RAG Engine", [
        ("sentence-transformers", "#a855f7"),
        ("FAISS / ChromaDB",      "#a855f7"),
        ("numpy",                 "#a855f7"),
    ]),
    ("Aplikacja", [
        ("Streamlit",    "#22c55e"),
        ("pytest",       "#22c55e"),
        ("python-dotenv","#22c55e"),
    ]),
]

# ── METRYKI RAPORTU TESTOWEGO (placeholder) ───────────────────────────────────
TEST_REPORT_METRICS: list[tuple[str, str]] = [
    ("Trafność",         "87%"),
    ("Brak halucynacji", "94%"),
    ("Poprawne źródła",  "91%"),
    ("Negatywne ✓",      "100%"),
]
