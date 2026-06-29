"""Split documents into smaller chunks for embedding and retrieval."""

from __future__ import annotations


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 120) -> list[str]:
    """Split text into overlapping character-based chunks.

    Chunking is needed in RAG because full documents can be too large to embed
    or retrieve efficiently. Smaller chunks make semantic search more focused.
    The overlap helps carry context across chunk boundaries.
    """
    cleaned_text = text.strip()
    if not cleaned_text:
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[str] = []
    start = 0
    text_length = len(cleaned_text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = cleaned_text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end == text_length:
            break

        start = end - overlap

    return chunks


def chunk_documents(
    documents: list[dict], chunk_size: int = 700, overlap: int = 120
) -> list[dict]:
    """Create chunk records while preserving document metadata."""
    chunked_documents: list[dict] = []

    for document in documents:
        chunks = chunk_text(document["text"], chunk_size=chunk_size, overlap=overlap)
        for index, chunk in enumerate(chunks):
            chunk_id = f"{document['document_id']}-chunk-{index:03d}"
            chunked_documents.append(
                {
                    "chunk_id": chunk_id,
                    "text": chunk,
                    "metadata": {
                        "source": document["source"],
                        "title": document["title"],
                    },
                }
            )

    return chunked_documents
