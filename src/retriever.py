"""Retriever for the HR RAG assistant."""

from __future__ import annotations

from src.vector_store import get_embedding_model, get_chroma_collection
from src.vector_store import VectorStore


def retrieve_relevant_chunks(query: str, top_k: int = 4) -> list[dict]:
    """Search ChromaDB and return the most relevant HR knowledge chunks.

    Retrieval is the first half of RAG. We convert the user question into an
    embedding and search for the closest chunk embeddings in the vector store.
    """
    embedding_model = get_embedding_model()
    collection = get_chroma_collection()

    query_embedding = embedding_model.encode([query], normalize_embeddings=True).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)

    retrieved_chunks: list[dict] = []
    for document, metadata, distance in zip(
        results.get("documents", [[]])[0],
        results.get("metadatas", [[]])[0],
        results.get("distances", [[]])[0],
    ):
        metadata = metadata or {}
        relevance_score = round(1 / (1 + float(distance)), 4) if distance is not None else None
        retrieved_chunks.append(
            {
                "text": document,
                "source": metadata.get("source", "unknown"),
                "title": metadata.get("title", "Untitled"),
                "chunk_id": metadata.get("chunk_id", "unknown"),
                "relevance_score": relevance_score,
            }
        )

    return retrieved_chunks


class Retriever:
    """Thin wrapper around the vector store query method."""

    def __init__(self, vector_store: VectorStore) -> None:
        self.vector_store = vector_store

    def retrieve(self, question: str, top_k: int = 4) -> list[dict]:
        """Fetch the most relevant chunks for a question."""
        return retrieve_relevant_chunks(question, top_k=top_k)
