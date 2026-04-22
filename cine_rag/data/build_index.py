from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.settings import PROCESSED_DIR, RAW_DIR
from data.chunker import split_documents
from data.exporter import export_chunks_to_json
from data.loader import load_documents
from data.preprocessing import build_clean_dataframe, save_documents_as_txt


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    log = logging.getLogger(__name__)

    log.info("1/4 Preprocessing CSV files...")
    df = build_clean_dataframe(RAW_DIR)
    save_documents_as_txt(df, PROCESSED_DIR)

    log.info("2/4 Loading documents...")
    documents = load_documents(PROCESSED_DIR)

    log.info("3/4 Chunking documents...")
    chunks = split_documents(documents)

    log.info("4/4 Exporting chunks to JSON...")
    export_chunks_to_json(chunks)

    log.info("Done. chunks.json saved to data/processed/")
    log.info("Next step: run the indexing workflow in n8n.")


if __name__ == "__main__":
    main()
