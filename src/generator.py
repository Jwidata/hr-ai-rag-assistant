"""Answer generation utilities for optional LLM and fallback modes."""

from __future__ import annotations

import os
import re
from textwrap import shorten

import requests
from openai import OpenAI

from src.config import LLM_PROVIDER, OLLAMA_MODEL, OPENAI_API_KEY, OPENAI_MODEL


def _build_sources_list(retrieved_chunks: list[dict]) -> list[str]:
    """Return de-duplicated source labels for the answer and API output."""
    seen: set[str] = set()
    sources: list[str] = []

    for chunk in retrieved_chunks:
        label = f"{chunk.get('title', 'Untitled')} ({chunk.get('source', 'unknown')})"
        if label not in seen:
            seen.add(label)
            sources.append(label)

    return sources


def _clean_chunk_text(text: str) -> str:
    """Remove markdown noise so fallback answers read more naturally."""
    cleaned_text = re.sub(r"#+\s*", "", text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    return cleaned_text.strip()


def _extract_relevant_sentences(query: str, retrieved_chunks: list[dict], limit: int = 3) -> list[str]:
    """Pick a few readable sentences from retrieved chunks for fallback answers."""
    query_terms = {
        term.lower()
        for term in re.findall(r"[A-Za-z][A-Za-z\-]+", query)
        if len(term) > 2
    }
    candidate_sentences: list[tuple[int, str]] = []

    for chunk in retrieved_chunks:
        cleaned_text = _clean_chunk_text(chunk["text"])
        sentences = re.split(r"(?<=[.!?])\s+", cleaned_text)

        for sentence in sentences:
            trimmed_sentence = sentence.strip()
            if len(trimmed_sentence) < 50:
                continue

            sentence_terms = {
                term.lower()
                for term in re.findall(r"[A-Za-z][A-Za-z\-]+", trimmed_sentence)
                if len(term) > 2
            }
            overlap_score = len(query_terms.intersection(sentence_terms))
            candidate_sentences.append((overlap_score, trimmed_sentence))

    candidate_sentences.sort(key=lambda item: item[0], reverse=True)

    selected_sentences: list[str] = []
    for _, sentence in candidate_sentences:
        if sentence not in selected_sentences:
            selected_sentences.append(sentence)
        if len(selected_sentences) == limit:
            break

    return selected_sentences


def _extract_formula(query: str, retrieved_chunks: list[dict]) -> str | None:
    """Return a likely metric formula when one appears in retrieved chunks."""
    query_terms = {
        term.lower()
        for term in re.findall(r"[A-Za-z][A-Za-z\-]+", query)
        if len(term) > 2
    }

    candidates: list[tuple[int, str]] = []
    for chunk in retrieved_chunks:
        for raw_line in chunk["text"].splitlines():
            line = _clean_chunk_text(raw_line)
            if "=" not in line or len(line) < 12:
                continue

            line_terms = {
                term.lower()
                for term in re.findall(r"[A-Za-z][A-Za-z\-]+", line)
                if len(term) > 2
            }
            overlap_score = len(query_terms.intersection(line_terms))
            candidates.append((overlap_score, line))

    if not candidates:
        return None

    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


def _build_prompt(query: str, retrieved_chunks: list[dict]) -> str:
    """Create a strict grounded prompt for an external LLM.

    A normal LLM answer may rely on general model memory. A RAG-grounded answer
    must stay inside the retrieved HR knowledge base context below.
    """
    context_text = "\n\n".join(
        (
            f"Title: {chunk.get('title', 'Untitled')}\n"
            f"Source: {chunk.get('source', 'unknown')}\n"
            f"Relevance Score: {chunk.get('relevance_score', 'n/a')}\n"
            f"Text: {chunk.get('text', '')}"
        )
        for chunk in retrieved_chunks
    )

    return (
        "You are an HR Data and AI Analytics assistant. "
        "Answer only from the retrieved HR knowledge base context. "
        "Do not invent facts or use outside knowledge. "
        "If the context does not contain enough information, say exactly: "
        '"I do not have enough information in the HR knowledge base to answer this confidently."\n\n'
        "Keep the response concise, professional, and presentation-ready.\n"
        "Use short paragraphs, not bullet-heavy notes.\n"
        "The direct answer should be 2 to 4 sentences maximum.\n"
        "The business meaning and HR Data & AI sections should each be 1 to 2 sentences maximum.\n"
        "If the question is about a metric and a formula is available in the context, include a Formula section. Otherwise omit it.\n"
        "Do not repeat raw headings or markdown text from the source documents. Synthesize cleanly.\n"
        "Your answer must use these section headings exactly:\n"
        "Direct answer\n"
        "Formula (include only if relevant)\n"
        "Business meaning\n"
        "Why this matters for HR Data & AI work\n"
        "Sources used\n\n"
        f"Question: {query}\n\n"
        f"Retrieved context:\n{context_text}"
    )


def _answer_with_openai(query: str, retrieved_chunks: list[dict]) -> str:
    """Use OpenAI when an API key is configured."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.responses.create(model=OPENAI_MODEL, input=_build_prompt(query, retrieved_chunks))
    return response.output_text.strip()


def _answer_with_ollama(query: str, retrieved_chunks: list[dict]) -> str:
    """Use Ollama when a base URL is configured."""
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "").rstrip("/")
    response = requests.post(
        f"{ollama_base_url}/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": _build_prompt(query, retrieved_chunks), "stream": False},
        timeout=60,
    )
    response.raise_for_status()
    return response.json().get("response", "").strip()


def _build_retrieval_only_answer(query: str, retrieved_chunks: list[dict]) -> str:
    """Create a concise answer directly from retrieved chunks.

    This is the no-LLM fallback. It is still grounded because it uses only the
    retrieved knowledge-base text.
    """
    if not retrieved_chunks:
        return (
            "Direct answer\n"
            "retrieval-based answer: I do not have enough information in the HR knowledge base to answer this confidently.\n\n"
            "Business meaning\n"
            "The current knowledge base does not contain enough relevant content for this question.\n\n"
            "Why this matters for HR Data & AI work\n"
            "Reliable HR Data and AI work depends on governed definitions and trusted source content, so the assistant should avoid guessing.\n\n"
            "Sources used\n"
            "None"
        )

    sources = _build_sources_list(retrieved_chunks)
    relevant_sentences = _extract_relevant_sentences(query, retrieved_chunks)
    formula = _extract_formula(query, retrieved_chunks)
    if relevant_sentences:
        direct_answer = " ".join(
            shorten(sentence, width=160, placeholder="...") for sentence in relevant_sentences[:2]
        )
    else:
        direct_answer = "I do not have enough information in the HR knowledge base to answer this confidently."

    business_meaning = (
        "This summarizes the most relevant governed HR guidance tied to the question and keeps the answer anchored to approved knowledge-base content."
    )
    hr_ai_meaning = (
        "This supports consistent interpretation, stronger governance, and more explainable HR analytics for business stakeholders."
    )

    answer_parts = [
        "Direct answer\n"
        f"{direct_answer}\n\n"
    ]

    if formula:
        answer_parts.append(f"Formula\n{formula}\n\n")

    answer_parts.append(
        "Business meaning\n"
        f"{business_meaning}\n\n"
        "Why this matters for HR Data & AI work\n"
        f"{hr_ai_meaning}\n\n"
        "Sources used\n"
        + "\n".join(f"- {source}" for source in sources)
    )

    return "".join(answer_parts)


def generate_answer(query: str, retrieved_chunks: list[dict]) -> str:
    """Generate a grounded answer from retrieved chunks.

    The generator may use an LLM, but it should still behave like RAG by using
    the retrieved chunks as the only allowed source of truth.
    """
    if not retrieved_chunks:
        return _build_retrieval_only_answer(query, retrieved_chunks)

    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "").strip()

    try:
        if OPENAI_API_KEY and (LLM_PROVIDER in {"", "openai"} or not ollama_base_url):
            return _answer_with_openai(query, retrieved_chunks)

        if ollama_base_url and LLM_PROVIDER in {"", "ollama"}:
            return _answer_with_ollama(query, retrieved_chunks)
    except (requests.RequestException, Exception):
        return _build_retrieval_only_answer(query, retrieved_chunks)

    return _build_retrieval_only_answer(query, retrieved_chunks)


class Generator:
    """Generate answers from retrieved context."""

    def answer(self, question: str, contexts: list[dict]) -> str:
        """Choose the best available answer strategy."""
        return generate_answer(question, contexts)
