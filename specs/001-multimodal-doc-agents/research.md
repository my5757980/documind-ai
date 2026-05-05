# Research: DocuMind AI — Multi-Modal Document Intelligence

**Branch**: `001-multimodal-doc-agents` | **Date**: 2026-05-04

## Decision 1: AMD Developer Cloud API Format

**Decision**: Use AMD Developer Cloud's OpenAI-compatible REST API via the
standard `openai` Python SDK, pointing `base_url` to the AMD endpoint.

**Rationale**: AMD Developer Cloud exposes an OpenAI-compatible inference
endpoint. This means the existing `openai` Python SDK works out of the box
by changing only `base_url` and `api_key`. No custom AMD SDK required.

**Alternatives considered**:
- Direct ROCm/HIP native calls — too low-level for inference; unnecessary for API-based access
- vLLM self-hosted on AMD — requires GPU instance management; AMD Developer Cloud API is simpler for hackathon

**Config**:
```python
from openai import OpenAI
client = OpenAI(
    base_url="https://api.amd.com/v1",   # AMD Developer Cloud endpoint
    api_key=os.environ["AMD_API_KEY"]
)
```

---

## Decision 2: Qwen-VL for Vision (AMD Cloud)

**Decision**: Use `Qwen/Qwen2-VL-7B-Instruct` (or `Qwen2-VL-72B-Instruct`
if credits allow) via AMD Developer Cloud for image/chart understanding.

**Rationale**: Qwen-VL is a top-tier open-source vision-language model
explicitly listed in the hackathon tech stack. It accepts image + text
prompts and returns structured analysis. Available on AMD Developer Cloud.

**Image encoding**: Convert images to base64 and pass in the
`content[{type: "image_url", image_url: {url: "data:image/...;base64,..."}}]`
format — same as OpenAI Vision API format.

**Alternatives considered**:
- Llama 3.2 Vision — also supported but Qwen-VL mentioned explicitly in hackathon bonus criteria
- Local CLIP embeddings — no text generation capability

---

## Decision 3: Qwen2.5 for Text Understanding (AMD Cloud)

**Decision**: Use `Qwen/Qwen2.5-72B-Instruct` via AMD Developer Cloud for
all text extraction, reading, analysis, and report generation tasks.

**Rationale**: Qwen2.5-72B is the most capable text model in the Qwen family
available on AMD cloud. Strong reasoning and instruction-following needed for
analyst and reporter agents.

**Alternatives considered**:
- Llama 3.3-70B — also valid but Qwen bonus prize targets Qwen family
- DeepSeek-R1 — good at reasoning but Qwen2.5 better at instruction-following

---

## Decision 4: CrewAI for Agent Orchestration

**Decision**: Use CrewAI with `process=Process.sequential` to orchestrate
the 4-agent pipeline. Each agent is defined with a `role`, `goal`,
`backstory`, and assigned one `Task`. The Crew runs tasks in order.

**Rationale**: CrewAI is explicitly listed in hackathon Track 1 tech stack.
Sequential process enforces Vision → Reader → Analyst → Reporter order.
Context passing is built in — each task's output is available to the next.

**CrewAI + custom LLM**: Use `LLM` class from CrewAI pointing to AMD endpoint:
```python
from crewai import LLM
amd_llm = LLM(
    model="openai/Qwen2.5-72B-Instruct",
    base_url="https://api.amd.com/v1",
    api_key=os.environ["AMD_API_KEY"]
)
```

**Alternatives considered**:
- LangChain agent executor — more verbose, less hackathon-friendly
- AutoGen — multi-turn conversation style; overkill for linear pipeline

---

## Decision 5: PDF Parsing and Image Extraction

**Decision**: Use PyMuPDF (`fitz`) for PDF parsing.
- Text extraction: `page.get_text()` → plain text per page
- Image extraction: `page.get_images()` + `doc.extract_image()` → PNG bytes

**Rationale**: PyMuPDF is the fastest Python PDF library. Handles scanned
PDFs, embedded images, and complex layouts reliably.

**Image format normalization**: All extracted images converted to JPEG
(quality=85) and base64-encoded before passing to Vision Agent.

**Alternatives considered**:
- PDFPlumber — text only, no image extraction
- pdfminer — slow, no image support
- Unstructured.io — too heavy, external dependency

---

## Decision 6: Streamlit for UI and Real-Time Status

**Decision**: Use Streamlit with `st.status()` context manager and
`st.empty()` placeholders for real-time agent progress display.

**Rationale**: Streamlit runs synchronously in Python — no websocket
setup needed. `st.status()` provides built-in expandable step tracking.
HF Spaces natively hosts Streamlit apps.

**Real-time pattern**:
```python
with st.status("Processing document...", expanded=True) as status:
    st.write("🔍 Vision Agent analyzing visual content...")
    vision_result = run_vision_agent(doc)
    st.write("✅ Vision Agent complete")
    st.write("📖 Reader Agent extracting text...")
    reader_result = run_reader_agent(doc)
    # etc.
    status.update(label="Report ready!", state="complete")
```

**Alternatives considered**:
- FastAPI + React — too much setup for 6-day sprint (Constitution Principle V)
- Gradio — less control over layout; HF Space Streamlit is cleaner

---

## Decision 7: Hugging Face Space Deployment

**Decision**: Deploy as HF Space with `sdk: streamlit`. App entry point is
`app.py` at repo root. Secrets (AMD_API_KEY) stored in HF Space settings,
not in code.

**Space organization**: Join AMD Developer Hackathon HF organization and
create Space there for community likes (HF prize eligibility).

**requirements.txt**: Generated via `uv export --no-hashes > requirements.txt`
before deployment. HF Spaces reads this file automatically.

**Alternatives considered**:
- Docker Space on HF — more control but slower cold starts
- Railway/Render backend — adds complexity without benefit for Streamlit
