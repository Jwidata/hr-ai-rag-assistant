"""Load markdown files, chunk them, and store them in ChromaDB."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.chunker import chunk_documents
from src.config import DATA_DIR
from src.document_loader import load_markdown_documents
from src.vector_store import add_chunks_to_vector_store, reset_collection


def main() -> None:
    """Ingest the markdown knowledge base into ChromaDB.

    This script is idempotent: every run resets the collection and rebuilds it
    from the current markdown files.
    """
    documents = load_markdown_documents(DATA_DIR)
    chunks = chunk_documents(documents)

    first_chunk_preview = "No chunks created."
    if chunks:
        first_chunk_preview = chunks[0]["text"][:250].replace("\n", " ")

    reset_collection()
    add_chunks_to_vector_store(chunks)

    print(f"Loaded {len(documents)} documents.")
    print(f"Created {len(chunks)} chunks.")
    print(f"First chunk preview: {first_chunk_preview}")
    print("Saved embeddings to ChromaDB in ./chroma_db.")


if __name__ == "__main__":
    main()
