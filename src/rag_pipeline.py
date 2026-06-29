"""Main RAG pipeline that ties retrieval and generation together."""

from __future__ import annotations

from src.generator import Generator, generate_answer
from src.retriever import Retriever, retrieve_relevant_chunks
from src.vector_store import VectorStore


def answer_question(query: str, top_k: int = 4) -> dict:
    """Run the retrieval and generation flow for one user question.

    In a normal LLM flow, the model answers from its general training data.
    In a RAG-grounded flow, we first retrieve trusted HR content and then answer
    from that content so the response is more explainable and controlled.
    """
    retrieved_chunks = retrieve_relevant_chunks(query, top_k=top_k)
    answer = generate_answer(query, retrieved_chunks)
    sources = []

    for chunk in retrieved_chunks:
        source_label = f"{chunk.get('title', 'Untitled')} ({chunk.get('source', 'unknown')})"
        if source_label not in sources:
            sources.append(source_label)

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks,
    }


class RAGPipeline:
    """Simple orchestrator used by the Streamlit app."""

    def __init__(self) -> None:
        self.vector_store = VectorStore()
        self.retriever = Retriever(self.vector_store)
        self.generator = Generator()

    def ask(self, question: str, top_k: int = 4) -> dict:
        """Retrieve context and return a generated answer."""
        result = answer_question(question, top_k=top_k)
        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "retrieved_chunks": result["retrieved_chunks"],
            "contexts": [
                {
                    "document": chunk["text"],
                    "metadata": {
                        "source": chunk["source"],
                        "title": chunk["title"],
                        "chunk_id": chunk["chunk_id"],
                        "relevance_score": chunk.get("relevance_score"),
                    },
                }
                for chunk in result["retrieved_chunks"]
            ],
        }
