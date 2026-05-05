import streamlit as st
import json
import time

from tools.document_loader import load_document
from models.report import AgentStatus, IntelligenceReport, FileSizeError, EmptyDocumentError, PipelineError
from pipeline.crew import run_pipeline

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="🧠",
    layout="wide",
)

AGENT_ICONS = {
    "Vision Agent":   "🔍",
    "Reader Agent":   "📖",
    "Analyst Agent":  "🧠",
    "Reporter Agent": "📋",
}

AGENT_DESCRIPTIONS = {
    "Vision Agent":   "Analyzing visual content, charts & diagrams on AMD MI300X...",
    "Reader Agent":   "Extracting & understanding text content on AMD MI300X...",
    "Analyst Agent":  "Synthesizing cross-modal intelligence on AMD MI300X...",
    "Reporter Agent": "Generating structured intelligence report on AMD MI300X...",
}


def render_header():
    st.title("🧠 DocuMind AI")
    st.markdown(
        "**Multi-Modal Document Intelligence** — Powered by AMD Instinct MI300X GPUs via Fireworks AI"
    )
    st.markdown(
        "Upload any document. Four specialized AI agents analyze it on AMD hardware "
        "and deliver a structured intelligence report in seconds."
    )
    st.divider()


def render_agent_pipeline_status(statuses: list[AgentStatus]):
    cols = st.columns(4)
    for col, status in zip(cols, statuses):
        icon = AGENT_ICONS.get(status.agent_name, "⚙️")
        with col:
            if status.status == "complete":
                dur = f" — {status.duration_seconds}s" if status.duration_seconds else ""
                st.success(f"{icon} {status.agent_name}{dur}")
            elif status.status == "running":
                st.info(f"{icon} {status.agent_name}\n\n*Running...*")
            elif status.status == "error":
                st.error(f"{icon} {status.agent_name}\n\n*Error*")
            else:
                st.caption(f"{icon} {status.agent_name}\n\n*Queued*")


def render_report(report: IntelligenceReport):
    st.success(f"Report ready in {report.total_duration_seconds}s")
    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Executive Summary")
        st.write(report.summary)

        st.subheader("Insights")
        for insight in report.insights:
            badge = insight.category.upper()
            source = insight.source
            st.markdown(f"- **[{badge}]** *({source})*: {insight.content}")

        st.subheader("Action Items")
        for item in report.action_items:
            st.markdown(f"- {item}")

    with col2:
        st.subheader("Key Entities")
        for entity in report.entities:
            st.markdown(f"**{entity.name}**")
            st.caption(f"*{entity.type}* — {entity.context}")
            st.divider()

    st.divider()
    st.download_button(
        label="Download Report (JSON)",
        data=json.dumps(report.to_dict(), indent=2),
        file_name=f"{report.document_name}_report.json",
        mime="application/json",
    )


def main():
    render_header()

    uploaded_file = st.file_uploader(
        "Upload your document",
        type=["pdf", "jpg", "jpeg", "png", "txt"],
        help="Supported: PDF, JPG, PNG, TXT — max 10 MB",
    )

    if uploaded_file is None:
        st.info("Upload a document above to get started. DocuMind AI will analyze it with 4 specialized AMD-powered agents.")
        st.markdown(
            "**Powered by:** AMD Instinct MI300X • Fireworks AI • Kimi K2.5 Vision • DeepSeek V3.1 • CrewAI"
        )
        return

    st.markdown(f"**File:** `{uploaded_file.name}` ({uploaded_file.size // 1024} KB)")

    if st.button("Analyze Document", type="primary", use_container_width=True):
        _run_analysis(uploaded_file)


def _run_analysis(uploaded_file):
    # Load document
    try:
        with st.spinner("Loading document..."):
            doc = load_document(uploaded_file.read(), uploaded_file.name)
        st.success(f"Loaded: {doc.page_count} page(s), {len(doc.images)} image(s), {len(doc.text_content)} chars of text")
    except FileSizeError as e:
        st.error(f"File too large: {e}")
        return
    except EmptyDocumentError as e:
        st.error(f"Empty document: {e}")
        return
    except ValueError as e:
        st.error(f"Cannot read file: {e}")
        return

    # Run pipeline with live status
    agent_status_placeholders = {}
    status_container = st.container()

    with status_container:
        st.subheader("Agent Pipeline — AMD MI300X")
        status_ph = st.empty()

    live_statuses: list[AgentStatus] = []

    def status_callback(updated: AgentStatus):
        found = False
        for i, s in enumerate(live_statuses):
            if s.agent_name == updated.agent_name:
                live_statuses[i] = updated
                found = True
                break
        if not found:
            live_statuses.append(updated)
        with status_ph.container():
            render_agent_pipeline_status(live_statuses)

    try:
        with st.status("Running 4-agent AMD pipeline...", expanded=True) as pipeline_status:
            for name in AGENT_ICONS:
                icon = AGENT_ICONS[name]
                st.write(f"{icon} {name}: queued")

            report = run_pipeline(doc, status_callback)
            pipeline_status.update(label="All agents complete!", state="complete", expanded=False)

        st.divider()
        render_report(report)

    except PipelineError as e:
        st.error(f"Pipeline error: {e}")
        st.info("Please try again or upload a different document.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        st.info("Please try again.")


if __name__ == "__main__":
    main()
