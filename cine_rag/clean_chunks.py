#!/usr/bin/env python3
"""Czyszczenie chunks.json - usuwanie szumu i duplikatów."""

import json
from pathlib import Path
import hashlib
from collections import defaultdict
from config.settings import PROCESSED_DIR

chunks_path = PROCESSED_DIR / "chunks.json"
backup_path = PROCESSED_DIR / "chunks_backup.json"

if not chunks_path.exists():
    print("❌ chunks.json nie istnieje!")
    exit(1)

with open(chunks_path, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print("=" * 70)
print("CZYSZCZENIE CHUNKS")
print("=" * 70)
print(f"\n📊 Początkowa liczba chunków: {len(chunks)}")

# Backup
with open(backup_path, "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)
print(f"✓ Backup zapisany do: {backup_path}")

# 1. Filtrowanie: usuwanie krótkich chunków
cleaned = []
short_removed = 0

for chunk in chunks:
    if not isinstance(chunk, dict):
        continue
    
    content = (chunk.get("page_content") or chunk.get("text") or "").strip()
    
    if len(content) < 100:
        short_removed += 1
        continue
    
    cleaned.append(chunk)

print(f"\n🗑️  Usunięto bardzo krótkie chunki: {short_removed}")
print(f"   (mniej niż 100 znaków)")

# 2. Deduplikacja: usuń identyczne fragmenty treści
deduplicated = []
seen_hashes = set()

for chunk in cleaned:
    content = (chunk.get("page_content") or chunk.get("text") or "").strip()
    content_hash = hashlib.md5(content.encode('utf-16')).hexdigest()
    
    if content_hash not in seen_hashes:
        deduplicated.append(chunk)
        seen_hashes.add(content_hash)

duplicates_removed = len(cleaned) - len(deduplicated)
print(f"\n🔄 Usunięto identyczne duplikaty treści: {duplicates_removed}")

# 3. Finalne statystyki
unique_films = len(set(
    chunk.get("metadata", {}).get("title", "Unknown")
    for chunk in deduplicated
))

print(f"\n✅ FINALNE STATYSTYKI:")
print(f"   Chunki przed: {len(chunks)}")
print(f"   Chunki po: {len(deduplicated)}")
print(f"   Usunięto: {len(chunks) - len(deduplicated)}")
print(f"   Unikalne filmy: {unique_films}")

# 4. Zapis
with open(chunks_path, "w", encoding="utf-8") as f:
    json.dump(deduplicated, f, ensure_ascii=False, indent=2)

print(f"\n✓ Oczyszczone chunks.json zapisane!")
print(f"\n🔄 Teraz uruchom:")
print(f"   python data/build_index.py")
