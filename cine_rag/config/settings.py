from pathlib import Path

# ── UI ────────────────────────────────────────────────────────────────────────
PAGE_TITLE: str = "CineRAG"
PAGE_ICON: str = "🎬"
LAYOUT: str = "wide"
DATASET_SIZE: int = 4803

# ── MODELE EMBEDDINGÓW ────────────────────────────────────────────────────────
DEFAULT_MODEL: str = "all-MiniLM-L6-v2"
EMBEDDING_MODEL_NAME: str = DEFAULT_MODEL
AVAILABLE_MODELS: list[str] = [
    "all-MiniLM-L6-v2",
    "paraphrase-multilingual-MiniLM-L12-v2",
]

# ── WYSZUKIWANIE ──────────────────────────────────────────────────────────────
DEFAULT_TOP_K: int = 3
TOP_K_DEFAULT: int = DEFAULT_TOP_K
MIN_TOP_K: int = 1
MAX_TOP_K: int = 10
SIMILARITY_THRESHOLD: float = 0.45

# ── CHUNKING ──────────────────────────────────────────────────────────────────
CHUNK_SIZE: int = 512
CHUNK_OVERLAP: int = 64
BATCH_SIZE: int = 64

# ── ŚCIEŻKI ───────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
CHUNKS_DIR = DATA_DIR / "chunks"
INDEX_DIR = DATA_DIR / "index"
VECTOR_STORE_PATH = PROCESSED_DIR / "faiss.index"

