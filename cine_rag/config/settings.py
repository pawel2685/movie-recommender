from pathlib import Path

# Embedding model
EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

# Retrieval
TOP_K_DEFAULT: int = 5

# Chunking
CHUNK_SIZE: int = 500
CHUNK_OVERLAP: int = 50

# Encoding
BATCH_SIZE: int = 64

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
CHUNKS_DIR = DATA_DIR / "chunks"
VECTOR_STORE_PATH = PROCESSED_DIR / "faiss.index"
