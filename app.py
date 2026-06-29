"""Streamlit app for the HR AI RAG assistant."""

from __future__ import annotations

import html

import streamlit as st

from src.rag_pipeline import RAGPipeline


st.set_page_config(
    page_title="AI-Ready HR Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
)


EXAMPLE_QUESTIONS = [
    "How is attrition calculated?",
    "What is compa-ratio and why does it matter?",
    "How do we identify compensation governance risks?",
    "What data-quality checks are needed before HR dashboards?",
    "How can HR data be made AI-ready?",
    "What does this project demonstrate for HR Data and AI analytics?",
]

KNOWLEDGE_BASE_DOCUMENTS = [
    "01_hr_metric_definitions.md",
    "02_compensation_governance.md",
    "03_workforce_planning.md",
    "04_data_quality_governance.md",
    "05_ai_readiness_hr.md",
    "06_experience_mapping_to_aris.md",
]

SAMPLE_INSIGHTS = [
    "Metric definitions can be retrieved with formula, business meaning, and governance context.",
    "Compensation questions can be grounded in salary-band, compa-ratio, and pay-governance logic.",
    "Data-quality questions can be answered with concrete controls such as duplicate checks, hierarchy validation, and reconciliation.",
]

ANSWER_SECTION_HEADERS = [
    "Direct answer",
    "Formula",
    "Business meaning",
    "Why this matters for HR Data & AI work",
    "Sources used",
]


@st.cache_resource
def get_pipeline() -> RAGPipeline:
    """Create the pipeline once and reuse it across reruns."""
    return RAGPipeline()


def inject_styles() -> None:
    """Add a small amount of CSS to make the demo feel more polished."""
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.08), transparent 26%),
                radial-gradient(circle at top left, rgba(16, 185, 129, 0.06), transparent 20%),
                linear-gradient(180deg, #f8fafc 0%, #eef4f8 100%);
            color: #0f172a;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8fbff 0%, #eef4f8 100%);
            border-right: 1px solid rgba(148, 163, 184, 0.18);
        }
        [data-testid="stSidebar"] * {
            color: #0f172a;
        }
        [data-testid="stHeader"] {
            background: rgba(248, 250, 252, 0.75);
        }
        [data-testid="stChatMessage"] {
            background: transparent;
            padding: 0;
        }
        [data-testid="stChatMessageContent"] {
            width: 100%;
        }
        [data-testid="stChatInput"] {
            background: rgba(255, 255, 255, 0.96);
            border: 1px solid rgba(148, 163, 184, 0.24);
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
            padding: 0.4rem;
        }
        [data-testid="stChatInput"] textarea {
            color: #0f172a !important;
        }
        [data-testid="stBaseButton-secondary"] {
            border-radius: 12px;
        }
        .stButton > button {
            border-radius: 14px;
            border: 1px solid rgba(148, 163, 184, 0.28);
            background: #ffffff;
            color: #0f172a;
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
            padding: 0.7rem 0.95rem;
            font-weight: 500;
        }
        .stButton > button:hover {
            border-color: rgba(59, 130, 246, 0.35);
            color: #0f172a;
            background: #f8fbff;
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2.5rem;
            max-width: 1200px;
        }
        .hero-card {
            background: linear-gradient(135deg, #ffffff 0%, #f6fbff 100%);
            border: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow: 0 20px 40px rgba(15, 23, 42, 0.08);
            border-radius: 22px;
            padding: 1.4rem 1.45rem;
            margin: 0.75rem 0 1.5rem 0;
        }
        .hero-title {
            font-size: 2.4rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
            letter-spacing: -0.02em;
            color: #0f172a;
        }
        .hero-subtitle {
            color: #475569;
            font-size: 1.05rem;
            line-height: 1.6;
        }
        .section-card {
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 16px;
            padding: 1rem 1.1rem;
            margin-bottom: 0.9rem;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
        }
        .section-label {
            color: #2563eb;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 0.4rem;
        }
        .section-text {
            font-size: 1rem;
            line-height: 1.75;
            color: #1e293b;
        }
        .source-pill {
            display: inline-block;
            background: #ffffff;
            border: 1px solid rgba(148, 163, 184, 0.2);
            color: #334155;
            border-radius: 999px;
            padding: 0.4rem 0.75rem;
            margin: 0.15rem 0.35rem 0.15rem 0;
            font-size: 0.88rem;
        }
        .mini-note {
            color: #64748b;
            font-size: 0.95rem;
            margin-bottom: 0.8rem;
        }
        .sidebar-card {
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 14px;
            padding: 0.85rem 0.95rem;
            margin-bottom: 0.9rem;
            line-height: 1.7;
            color: #334155;
        }
        .sidebar-note {
            color: #64748b;
            font-size: 0.88rem;
            margin: -0.1rem 0 0.7rem 0;
        }
        .insight-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.85rem;
            margin: 0.75rem 0 1.2rem 0;
        }
        .insight-card {
            background: rgba(255, 255, 255, 0.86);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 14px;
            padding: 0.95rem 1rem;
            min-height: 130px;
            box-shadow: 0 10px 22px rgba(15, 23, 42, 0.05);
        }
        .insight-title {
            color: #2563eb;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 0.45rem;
        }
        .insight-text {
            line-height: 1.65;
            color: #334155;
        }
        .metric-chip {
            display: inline-block;
            background: rgba(37, 99, 235, 0.08);
            color: #1d4ed8;
            border: 1px solid rgba(59, 130, 246, 0.16);
            border-radius: 999px;
            padding: 0.35rem 0.7rem;
            font-size: 0.82rem;
            font-weight: 600;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }
        .formula-card {
            background: rgba(239, 246, 255, 0.95);
            border-left: 4px solid #38bdf8;
            border-radius: 12px;
            padding: 0.95rem 1rem;
            margin-bottom: 1rem;
            font-family: "Source Code Pro", monospace;
            font-size: 0.98rem;
            color: #0f172a;
        }
        .chat-shell {
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 22px;
            padding: 1rem 1rem 0.5rem 1rem;
            box-shadow: 0 16px 36px rgba(15, 23, 42, 0.06);
            backdrop-filter: blur(8px);
        }
        .chat-intro {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 18px;
            padding: 0.95rem 1rem;
            margin-bottom: 1rem;
        }
        .chat-intro-badge {
            width: 40px;
            height: 40px;
            border-radius: 12px;
            background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            font-weight: 700;
            flex-shrink: 0;
        }
        .chat-intro-text {
            color: #334155;
            line-height: 1.6;
        }
        .question-bubble {
            background: #ffffff;
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 18px;
            padding: 0.95rem 1rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
            margin-bottom: 0.75rem;
        }
        .question-label {
            color: #2563eb;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }
        .question-text {
            color: #0f172a;
            font-size: 1rem;
            font-weight: 500;
        }
        .evidence-header {
            color: #475569;
            font-size: 0.92rem;
            margin-bottom: 0.75rem;
        }
        .evidence-card {
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 16px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.7rem;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
        }
        .evidence-title {
            color: #0f172a;
            font-size: 0.98rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }
        .evidence-meta {
            color: #64748b;
            font-size: 0.84rem;
            margin-bottom: 0.65rem;
        }
        .evidence-text {
            color: #334155;
            line-height: 1.7;
        }
        .footer-note {
            color: #64748b;
            font-size: 0.9rem;
            text-align: center;
            padding: 1rem 0 0.25rem 0;
        }
        .footer-note strong {
            color: #334155;
            font-weight: 600;
        }
        h1, h2, h3, h4, h5, h6, p, label, span, div {
            color: inherit;
        }
        @media (max-width: 900px) {
            .block-container {
                padding-top: 1rem;
                padding-bottom: 1.75rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
            .hero-card {
                padding: 1rem 1rem;
                border-radius: 18px;
            }
            .hero-title {
                font-size: 2rem;
            }
            .hero-subtitle {
                font-size: 0.98rem;
            }
            .insight-grid {
                grid-template-columns: 1fr;
            }
        }
        @media (max-width: 640px) {
            .hero-title {
                font-size: 1.7rem;
            }
            .section-card, .sidebar-card, .insight-card {
                padding: 0.85rem 0.9rem;
            }
            .section-text, .insight-text {
                line-height: 1.6;
            }
            .chat-shell {
                padding: 0.8rem 0.8rem 0.35rem 0.8rem;
                border-radius: 18px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialize_session_state() -> None:
    """Create chat state once so the conversation survives reruns."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def submit_question(question: str) -> None:
    """Run the RAG pipeline and append the result to chat history."""
    cleaned_question = question.strip()
    if not cleaned_question:
        return

    pipeline = get_pipeline()
    with st.spinner("Searching the HR knowledge base..."):
        result = pipeline.ask(cleaned_question)

    st.session_state.chat_history.append(
        {
            "question": cleaned_question,
            "answer": result["answer"],
            "sources": result.get("sources", []),
            "retrieved_chunks": result.get("retrieved_chunks", []),
        }
    )


def render_sidebar() -> None:
    """Render project context and quick-start guidance."""
    with st.sidebar:
        st.header("Assistant overview")
        st.markdown(
            '<div class="sidebar-card">This assistant shows how governed HR analytics knowledge can be retrieved and used to support more reliable answers on workforce planning, compensation, data quality, and AI readiness.</div>',
            unsafe_allow_html=True,
        )

        st.header("Sample prompts")
        st.markdown('<div class="sidebar-note">Use these prompts to quickly demonstrate the assistant.</div>', unsafe_allow_html=True)
        for index, question in enumerate(EXAMPLE_QUESTIONS):
            if st.button(question, key=f"example-question-{index}", use_container_width=True):
                submit_question(question)

        st.header("Knowledge sources")
        st.markdown(
            '<div class="sidebar-card">Core reference documents used for semantic retrieval and grounded responses.</div>',
            unsafe_allow_html=True,
        )
        for document_name in KNOWLEDGE_BASE_DOCUMENTS:
            st.caption(document_name)

        st.header("What the solution demonstrates")
        st.markdown(
            '<div class="sidebar-card">The project demonstrates governed metric definitions, HR data-quality controls, compensation governance logic, workforce planning concepts, and practical RAG-based knowledge retrieval.</div>',
            unsafe_allow_html=True,
        )


def render_chat_history() -> None:
    """Render the prior questions and answers stored in session state."""
    if st.session_state.chat_history:
        st.markdown('<div class="chat-shell">', unsafe_allow_html=True)

    for index, chat_item in enumerate(st.session_state.chat_history, start=1):
        with st.chat_message("user"):
            st.markdown(
                (
                    '<div class="question-bubble">'
                    '<div class="question-label">Question</div>'
                    f'<div class="question-text">{html.escape(chat_item["question"])}</div>'
                    '</div>'
                ),
                unsafe_allow_html=True,
            )

        with st.chat_message("assistant"):
            render_answer_meta(chat_item["retrieved_chunks"])
            st.subheader("Answer")
            render_answer_sections(chat_item["answer"])

            st.subheader("Sources used")
            if chat_item["sources"]:
                render_sources(chat_item["sources"])
            else:
                st.write("No sources were returned.")

            st.subheader("Supporting evidence")
            st.markdown(
                '<div class="evidence-header">These source passages show the evidence used to ground the response.</div>',
                unsafe_allow_html=True,
            )
            if chat_item["retrieved_chunks"]:
                for chunk_position, chunk in enumerate(chat_item["retrieved_chunks"], start=1):
                    preview_text = html.escape(chunk["text"][:380].strip())
                    if len(chunk["text"].strip()) > 380:
                        preview_text += "..."

                    st.markdown(
                        (
                            '<div class="evidence-card">'
                            f'<div class="evidence-title">Evidence {index}.{chunk_position}: {html.escape(chunk["title"])}</div>'
                            f'<div class="evidence-meta">Source: {html.escape(chunk["source"])} | Relevance score: {chunk.get("relevance_score", "n/a")}</div>'
                            f'<div class="evidence-text">{preview_text}</div>'
                            '</div>'
                        ),
                        unsafe_allow_html=True,
                    )
            else:
                st.write("No retrieved evidence available.")

    if st.session_state.chat_history:
        st.markdown('</div>', unsafe_allow_html=True)


def parse_answer_sections(answer_text: str) -> dict[str, str]:
    """Split a generated answer into named sections for cleaner rendering."""
    sections: dict[str, str] = {}
    current_header: str | None = None
    buffer: list[str] = []

    def flush_buffer() -> None:
        if current_header is not None:
            sections[current_header] = "\n".join(buffer).strip()

    for raw_line in answer_text.splitlines():
        line = raw_line.strip()
        normalized_line = line.removeprefix("1. ").removeprefix("2. ").removeprefix("3. ").removeprefix("4. ")

        if normalized_line in ANSWER_SECTION_HEADERS:
            flush_buffer()
            current_header = normalized_line
            buffer = []
        elif current_header is not None:
            buffer.append(raw_line)

    flush_buffer()
    return sections


def render_answer_sections(answer_text: str) -> None:
    """Render structured answer sections in a more professional layout."""
    sections = parse_answer_sections(answer_text)

    if not sections:
        st.write(answer_text)
        return

    direct_answer = sections.get("Direct answer")
    if direct_answer:
        direct_answer_html = html.escape(direct_answer).replace("\n", "<br>")
        st.markdown(
            (
                '<div class="section-card">'
                '<div class="section-label">Direct answer</div>'
                f'<div class="section-text">{direct_answer_html}</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    formula = sections.get("Formula")
    if formula:
        formula_html = html.escape(formula).replace("\n", "<br>")
        st.markdown('<div class="section-label">Formula</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="formula-card">{formula_html}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    business_meaning = sections.get("Business meaning")
    if business_meaning:
        with col1:
            business_meaning_html = html.escape(business_meaning).replace("\n", "<br>")
            st.markdown(
                (
                    '<div class="section-card">'
                    '<div class="section-label">Business meaning</div>'
                    f'<div class="section-text">{business_meaning_html}</div>'
                    '</div>'
                ),
                unsafe_allow_html=True,
            )

    hr_ai_meaning = sections.get("Why this matters for HR Data & AI work")
    if hr_ai_meaning:
        with col2:
            hr_ai_meaning_html = html.escape(hr_ai_meaning).replace("\n", "<br>")
            st.markdown(
                (
                    '<div class="section-card">'
                    '<div class="section-label">Why this matters for HR Data & AI work</div>'
                    f'<div class="section-text">{hr_ai_meaning_html}</div>'
                    '</div>'
                ),
                unsafe_allow_html=True,
            )

    sources_used = sections.get("Sources used")
    if sources_used:
        st.markdown('<div class="section-label">Sources used</div>', unsafe_allow_html=True)
        render_sources(parse_sources_text(sources_used))


def parse_sources_text(sources_text: str) -> list[str]:
    """Convert the sources section into a simple list of labels."""
    sources = []
    for line in sources_text.splitlines():
        cleaned_line = line.strip().removeprefix("- ").strip()
        if cleaned_line:
            sources.append(cleaned_line)
    return sources


def render_sources(sources: list[str]) -> None:
    """Render source labels as small pills instead of a raw bullet list."""
    if not sources:
        st.write("No sources were returned.")
        return

    pills_html = "".join(
        f'<span class="source-pill">{html.escape(source)}</span>' for source in sources
    )
    st.markdown(pills_html, unsafe_allow_html=True)


def render_answer_meta(retrieved_chunks: list[dict]) -> None:
    """Show a compact grounding summary above the answer."""
    source_count = len({chunk.get("source", "unknown") for chunk in retrieved_chunks})
    chunk_count = len(retrieved_chunks)
    scores = [chunk.get("relevance_score") for chunk in retrieved_chunks if chunk.get("relevance_score") is not None]

    confidence = "Grounded"
    if scores:
        average_score = sum(scores) / len(scores)
        if average_score >= 0.65:
            confidence = "High confidence"
        elif average_score >= 0.45:
            confidence = "Moderate confidence"
        else:
            confidence = "Use with care"

    chips = [
        confidence,
        f"{chunk_count} retrieved chunks",
        f"{source_count} source documents",
    ]
    chips_html = "".join(f'<span class="metric-chip">{html.escape(chip)}</span>' for chip in chips)
    st.markdown(chips_html, unsafe_allow_html=True)


def render_sample_insights() -> None:
    """Show a few sample insights the assistant is designed to surface."""
    cards_html = []
    for index, insight in enumerate(SAMPLE_INSIGHTS, start=1):
        cards_html.append(
            '<div class="insight-card">'
            f'<div class="insight-title">Sample insight {index}</div>'
            f'<div class="insight-text">{html.escape(insight)}</div>'
            '</div>'
        )

    st.markdown("### What this assistant can surface")
    st.markdown(
        f'<div class="insight-grid">{"".join(cards_html)}</div>',
        unsafe_allow_html=True,
    )


def main() -> None:
    """Render the Streamlit user interface."""
    initialize_session_state()
    inject_styles()
    render_sidebar()

    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">AI-Ready HR Knowledge Assistant</div>
            <div class="hero-subtitle">
                RAG chatbot for workforce planning, compensation governance, HR metrics, data quality, and AI readiness.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Project explanation")
    st.markdown(
        '<div class="section-card"><div class="section-text">'
        'This project demonstrates how fragmented HR definitions, policies, and analytics guidance can be organized into a governed knowledge base, retrieved through semantic search, and used to support more reliable AI-assisted responses.'
        '</div></div>',
        unsafe_allow_html=True,
    )

    render_sample_insights()

    st.markdown(
        (
            '<div class="chat-intro">'
            '<div class="chat-intro-badge">AI</div>'
            '<div class="chat-intro-text">Ask a question about HR metrics, compensation governance, workforce planning, data quality, or AI readiness. The assistant will retrieve relevant governed content first and then generate a grounded response.</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="mini-note">Ask a question below or use one of the sample prompts from the sidebar.</div>', unsafe_allow_html=True)

    render_chat_history()

    prompt = st.chat_input("Ask about HR metrics, compensation, workforce planning, or AI readiness")
    if prompt:
        submit_question(prompt)
        st.rerun()

    st.markdown(
        '<div class="footer-note"><strong>Built with</strong> Streamlit, ChromaDB, sentence-transformers, and optional OpenAI generation.</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
