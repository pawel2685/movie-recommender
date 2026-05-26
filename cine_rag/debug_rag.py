#!/usr/bin/env python3
"""Debug script - Testowanie RAG pipeline krok po kroku."""

import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import requests
import os
import numpy as np
from config.settings import VECTOR_STORE_PATH, PROCESSED_DIR, EMBEDDING_MODEL_NAME

question = "Jakie filmy wyreżyserował Christopher Nolan?"
top_k = 5

print("=" * 80)
print("DEBUG RAG PIPELINE")
print("=" * 80)

# 1. Embeddings
print(f"\n📊 KROK 1: Embedding pytania")
embed_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
query_vector = embed_model.encode([question]).astype("float32")
print(f"✓ Query vector shape: {query_vector.shape}")

# 2. FAISS Search
print(f"\n📊 KROK 2: Przeszukiwanie FAISS")
index_data = VECTOR_STORE_PATH.read_bytes()
index = faiss.deserialize_index(np.frombuffer(index_data, dtype='uint8'))
distances, indices = index.search(query_vector, min(top_k * 2, 10))

print(f"✓ Top {len(indices[0])} wyników:")
for i, (idx, dist) in enumerate(zip(indices[0], distances[0])):
    print(f"   {i+1}. Index: {idx}, Distance: {dist:.4f}")

# 3. Load chunks
print(f"\n📊 KROK 3: Ładowanie chunks")
chunks_path = PROCESSED_DIR / "chunks.json"
with open(chunks_path, "r", encoding="utf-8") as f:
    all_chunks = json.load(f)
print(f"✓ Załadowano {len(all_chunks)} chunków")

# 4. Retrieve & Deduplicate
print(f"\n📊 KROK 4: Pobieranie i deduplikacja")
retrieved_context = []
sources = []
seen_hashes = set()

for i, idx in enumerate(indices[0]):
    if len(sources) >= top_k or idx >= len(all_chunks):
        print(f"   ⏹️  Zatrzymano - {len(sources)} źródeł")
        break
    
    chunk = all_chunks[int(idx)]
    content = (chunk.get("page_content") or chunk.get("text", "")).strip()
    metadata = chunk.get("metadata", {})
    title = metadata.get("title", "?")
    
    print(f"\n   [{i+1}] {title}")
    print(f"       Długość: {len(content)} znaków")
    
    if len(content) < 50:
        print(f"       ❌ POMINIĘTY - za krótki!")
        continue
    
    content_hash = hash(content[:100])
    if content_hash in seen_hashes:
        print(f"       ❌ POMINIĘTY - duplikat!")
        continue
    
    seen_hashes.add(content_hash)
    retrieved_context.append(content)
    sources.append({
        "title": title,
        "content": content[:100],
        "score": float(distances[0][i])
    })
    print(f"       ✓ DODANY")

print(f"\n✅ WYNIK:")
print(f"   • Retrieved context items: {len(retrieved_context)}")
print(f"   • Sources: {len(sources)}")
print(f"   • Seen hashes: {len(seen_hashes)}")

print(f"\n📋 SOURCES (co będzie wysłane do UI):")
for src in sources:
    print(f"   • {src['title']}: {src['content'][:50]}...")

print(f"\n📝 CONTEXT DO PROMPTA:")
context_text = "\n\n---\n\n".join(retrieved_context)
print(f"   Długość: {len(context_text)} znaków")
print(f"   Liczba fragmentów: {len(retrieved_context)}")
for i, ctx in enumerate(retrieved_context):
    print(f"\n   FRAGMENT {i+1}:")
    print(f"   {ctx[:100]}...")

# 5. Test LLM
print(f"\n📊 KROK 5: Test odpowiedzi Ollama")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "neural-chat")

prompt = f"Kontekst: {context_text}\n\nPytanie: {question}\nOdpowiedź:"

try:
    res = requests.post(
        f"{OLLAMA_API_URL}/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=30
    )
    if res.status_code == 200:
        print(f"✓ Ollama odpowiedziała poprawnie!")
        print(f"📝 ODPOWIEDŹ: {res.json().get('response')}")
    else:
        print(f"❌ Błąd Ollama: {res.status_code}")
except Exception as e:
    print(f"❌ Nie udało się połączyć z Ollama: {e}")
