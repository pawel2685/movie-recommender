from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid

COLLECTION_NAME = "movies"

client = QdrantClient(
    host="localhost",
    port=6333
)


def create_collection(vector_size):

    collections = client.get_collections().collections

    exists = any(
        c.name == COLLECTION_NAME
        for c in collections
    )

    if exists:
        print("Collection already exists")
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        )
    )

    print("Collection created")


def upload_embeddings(data, embeddings):

    points = []

    for item, vector in zip(data, embeddings):

        payload = {
            "file": item.get("file", ""),
            "chunk": item.get("chunk", 0),
            "text": item.get("text", "")
        }

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector.tolist(),
                payload=payload
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print("Embeddings uploaded")


def search_qdrant(query_vector, top_k=5):

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector.tolist(),
        limit=top_k
    )

    return results.points