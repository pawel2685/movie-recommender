import pandas as pd

from rag.embeddings import get_embedding_model
from rag.qdrant_db import create_collection, upload_embeddings

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading CSV...")

movies = pd.read_csv("./data/raw/tmdb_5000_movies.csv")

movies = movies.fillna("")

documents = []

for idx, row in movies.head(4800).iterrows():

    text = f"""
    Title: {row['title']}
    Overview: {row['overview']}
    Genres: {row['genres']}
    Keywords: {row['keywords']}
    """

    documents.append({
        "file": row["title"],
        "chunk": idx,
        "text": text
    })

print(f"Documents prepared: {len(documents)}")

model = get_embedding_model(MODEL_NAME)

texts = [d["text"] for d in documents]

print("Generating embeddings...")

embeddings = model.encode(texts)

print("Creating collection...")

create_collection(len(embeddings[0]))

print("Uploading to Qdrant...")

upload_embeddings(documents, embeddings)

print("DONE")