"""Load source documents from the local knowledge base folder."""

from __future__ import annotations

from pathlib import Path


def _extract_title(text: str, fallback_name: str) -> str:
    """Return the first markdown heading or a filename-based fallback title."""
    for line in text.splitlines():
        stripped_line = line.strip()
        if stripped_line.startswith("# "):
            return stripped_line.removeprefix("# ").strip()

    return fallback_name.replace("_", " ").replace("-", " ").title()


def load_markdown_documents(folder_path: Path) -> list[dict]:
    """Load markdown files and return structured document dictionaries.

    In a RAG pipeline we load documents first, then split them into smaller
    chunks. Keeping document metadata here makes it easier to preserve context
    later during retrieval.
    """
    if not folder_path.exists():
        raise FileNotFoundError(f"Knowledge base folder does not exist: {folder_path}")

    if not folder_path.is_dir():
        raise NotADirectoryError(f"Knowledge base path is not a folder: {folder_path}")

    markdown_files = sorted(folder_path.glob("*.md"))
    if not markdown_files:
        raise FileNotFoundError(f"No markdown files found in knowledge base folder: {folder_path}")

    documents: list[dict] = []

    for index, file_path in enumerate(markdown_files, start=1):
        full_text = file_path.read_text(encoding="utf-8").strip()
        title = _extract_title(full_text, file_path.stem)

        documents.append(
            {
                "document_id": f"doc-{index:03d}",
                "source": file_path.name,
                "title": title,
                "text": full_text,
            }
        )

    return documents
