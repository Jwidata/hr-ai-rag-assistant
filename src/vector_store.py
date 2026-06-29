"""Helpers for storing HR knowledge chunks in ChromaDB."""

from __future__ import annotations

import chromadb
from sentence_transformers import SentenceTransformer

from src.config import CHROMA_COLLECTION_NAME, CHROMA_DIR, EMBEDDING_MODEL


def get_embedding_model() -> SentenceTransformer:
    """Return the sentence-transformers model used to create embeddings.

    Embeddings are numeric representations of text. Similar pieces of text end up
    close to each other in vector space, which makes semantic search possible.
    """
    return SentenceTransformer(EMBEDDING_MODEL)


def get_chroma_collection():
    """Return the persistent ChromaDB collection for HR knowledge chunks.

    A vector database stores embeddings and lets us search by meaning instead of
    only exact keywords. That is useful for HR knowledge retrieval because users
    can ask the same concept in many different ways.
    """
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)


def reset_collection() -> None:
    """Delete and recreate the collection for a clean ingestion run."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    try:
        client.delete_collection(CHROMA_COLLECTION_NAME)
    except Exception:
        pass

    client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)


def add_chunks_to_vector_store(chunks: list[dict]) -> None:
    """Embed chunk text and store the results in ChromaDB.

    Each chunk is embedded into a numeric vector before being written to the
    vector database. Later, user questions are embedded the same way so we can
    retrieve the most relevant HR knowledge chunks.
    """
    if not chunks:
        return

    embedding_model = get_embedding_model()
    collection = get_chroma_collection()

    chunk_texts = [chunk["text"] for chunk in chunks]
    chunk_ids = [chunk["chunk_id"] for chunk in chunks]
    chunk_metadatas = []

    for chunk in chunks:
        metadata = dict(chunk["metadata"])
        metadata["chunk_id"] = chunk["chunk_id"]
        chunk_metadatas.append(metadata)

    embeddings = embedding_model.encode(chunk_texts, normalize_embeddings=True).tolist()

    collection.add(
        ids=chunk_ids,
        documents=chunk_texts,
        metadatas=chunk_metadatas,
        embeddings=embeddings,
    )


class VectorStore:
    """Small wrapper used by the retriever and app."""

    def __init__(self) -> None:
        self.embedding_model = get_embedding_model()
        self.collection = get_chroma_collection()

    def query(self, question: str, top_k: int = 4) -> list[dict]:
        """Return the top matching chunks for a user question."""
        query_embedding = self.embedding_model.encode(
            [question], normalize_embeddings=True
        ).tolist()

        results = self.collection.query(query_embeddings=query_embedding, n_results=top_k)

        matches: list[dict] = []
        for document, metadata, distance in zip(
            results.get("documents", [[]])[0],
            results.get("metadatas", [[]])[0],
            results.get("distances", [[]])[0],
        ):
            matches.append(
                {"document": document, "metadata": metadata or {}, "distance": distance}
            )

        return matches
