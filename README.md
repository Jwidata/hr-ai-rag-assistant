# HR AI RAG Assistant

`hr-ai-rag-assistant` is a small interview-ready Python project that demonstrates a simple Retrieval-Augmented Generation (RAG) chatbot for HR Data and AI Analytics.

The assistant answers questions about:

- HR metrics
- Workforce planning
- Compensation governance
- Data quality and governance
- AI readiness in HR
- Mapping analytics experience to ARIS-style consulting work

## What is RAG?

RAG stands for Retrieval-Augmented Generation.

In simple words:

1. A user asks a question.
2. The app searches a small knowledge base for the most relevant notes.
3. The app uses those notes to build the answer.

This is useful because the chatbot does not need to rely only on general model memory. It can ground its answer in the documents you provide.

## Project Goals

- Keep the code simple and easy to explain in an interview.
- Show the main parts of a basic RAG workflow.
- Work locally without requiring a paid API.
- Support optional OpenAI or Ollama generation.

## Tech Stack

- Python 3.11+
- Streamlit
- ChromaDB
- sentence-transformers
- python-dotenv
- Optional: OpenAI or Ollama

## File Structure

```text
hr-ai-rag-assistant/
  app.py
  requirements.txt
  README.md
  .env.example
  data/
    knowledge_base/
      01_hr_metric_definitions.md
      02_compensation_governance.md
      03_workforce_planning.md
      04_data_quality_governance.md
      05_ai_readiness_hr.md
      06_experience_mapping_to_aris.md
  src/
    __init__.py
    config.py
    document_loader.py
    chunker.py
    vector_store.py
    retriever.py
    generator.py
    rag_pipeline.py
  scripts/
    ingest.py
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment variables if needed:

```bash
copy .env.example .env
```

4. Ingest the knowledge base into ChromaDB:

```bash
python scripts/ingest.py
```

5. Start the app:

```bash
streamlit run app.py
```

## Environment Variables

The app works without an API key. In that case it uses retrieval-only mode and drafts an answer directly from the retrieved notes.

Optional settings:

- `OPENAI_API_KEY` for OpenAI
- `OPENAI_MODEL` such as `gpt-4o-mini`
- `OLLAMA_MODEL` such as `llama3.1`
- `LLM_PROVIDER` set to `openai`, `ollama`, or leave blank for fallback mode

## How the App Works

1. `scripts/ingest.py` loads markdown files from `data/knowledge_base/`.
2. `src/chunker.py` splits long documents into smaller chunks.
3. `src/vector_store.py` creates embeddings and stores them in ChromaDB.
4. `src/retriever.py` finds the most relevant chunks for a question.
5. `src/generator.py` either:
   - calls OpenAI,
   - calls a local Ollama model, or
   - builds a retrieval-only answer.
6. `app.py` shows the UI in Streamlit.

## Interview Talking Points

- The retrieval layer helps ground answers in HR-specific content.
- ChromaDB stores vector embeddings for semantic search.
- sentence-transformers turns text into embeddings.
- The fallback mode keeps the demo usable even without LLM credentials.
- The code is intentionally small so each component is easy to explain.
