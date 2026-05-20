#!/usr/bin/env python3
"""Skrypt diagnostyczny - sprawdzenie jakości danych i embeddingów."""

import json
from pathlib import Path
from collections import Counter
from config.settings import PROCESSED_DIR

chunks_path = PROCESSED_DIR / "chunks.json"

print("=" * 70)
print("DIAGNOSTYKA - Sprawdzenie chunks.json")
print("=" * 70)

if not chunks_path.exists():
    print("❌ chunks.json nie istnieje!")
    exit(1)

with open(chunks_path, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"\n📊 STATYSTYKI:")
print(f"  Łączna liczba chunków: {len(chunks)}")

titles = []
duplicates = Counter()
empty_chunks = 0

for i, chunk in enumerate(chunks):
    # Sprawdzenie struktury
    if isinstance(chunk, dict):
        metadata = chunk.get("metadata", {})
        title = metadata.get("title", "BRAK TYTUŁU")
        content = chunk.get("page_content") or chunk.get("text", "")
        
        titles.append(title)
        
        if not content.strip():
            empty_chunks += 1
            print(f"⚠️  Chunk #{i}: PUSTY")
        
        if len(content) < 50:
            print(f"⚠️  Chunk #{i} ({title}): BARDZO KRÓTKI ({len(content)} znaków)")

# Analiza duplikatów
print(f"\n🎬 UNIKALNE FILMY: {len(set(titles))}")
print(f"📌 PUSTE CHUNKI: {empty_chunks}")

# Top duplikaty
duplicated = {title: count for title, count in Counter(titles).items() if count > 1}
if duplicated:
    print(f"\n⚠️  DUPLIKATY FILMÓW:")
    for title, count in sorted(duplicated.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   • {title}: {count}x")
else:
    print(f"\n✅ BRAK DUPLIKATÓW - świetnie!")

# Sample chunks
print(f"\n📄 PRZYKŁADOWE CHUNKI (pierwsze 3):")
for i in range(min(3, len(chunks))):
    chunk = chunks[i]
    if isinstance(chunk, dict):
        metadata = chunk.get("metadata", {})
        title = metadata.get("title", "BRAK")
        content = (chunk.get("page_content") or chunk.get("text", ""))[:100]
        print(f"\n   #{i} | Tytuł: {title}")
        print(f"      Treść: {content}...")
