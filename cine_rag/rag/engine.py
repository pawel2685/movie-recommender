from rag.embeddings import get_embedding_model
from rag.retriever import retrieve
from rag.generator import generate_response
from config.settings import TOP_K_DEFAULT


def rag_query(query: str, top_k: int = TOP_K_DEFAULT) -> list[dict]:
    """Main RAG pipeline: embed query → retrieve chunks → generate response."""
    model = get_embedding_model()
    query_embedding = model.encode(query)
    chunks = retrieve(query_embedding, top_k=top_k)
    results = generate_response(query, chunks)
    return results
