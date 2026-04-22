from __future__ import annotations

import json
import logging
from pathlib import Path

from langchain_core.documents import Document

from config.settings import PROCESSED_DIR

log = logging.getLogger(__name__)


def export_chunks_to_json(chunks: list[Document], output_path: Path | None = None) -> Path:
    if output_path is None:
        output_path = PROCESSED_DIR / "chunks.json"

    data = [
        {
            "text": chunk.page_content,
            "metadata": chunk.metadata,
        }
        for chunk in chunks
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    log.info("Exported %d chunks to %s", len(data), output_path)
    return output_path
