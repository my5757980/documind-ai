---
id: 003
title: DocuMind Plan Pipeline Architecture
stage: plan
date: 2026-05-04
surface: agent
model: claude-sonnet-4-6
feature: 001-multimodal-doc-agents
branch: 001-multimodal-doc-agents
user: Muhammad Yaseen
command: /sp.plan
labels: ["plan","amd-hackathon","documind-ai","crewai","qwen","streamlit","architecture"]
links:
  spec: specs/001-multimodal-doc-agents/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-multimodal-doc-agents/plan.md
  - specs/001-multimodal-doc-agents/research.md
  - specs/001-multimodal-doc-agents/data-model.md
  - specs/001-multimodal-doc-agents/quickstart.md
  - specs/001-multimodal-doc-agents/contracts/pipeline.md
tests:
  - none
---

## Prompt

001-multimodal-doc-agents

## Response snapshot

Full implementation plan generated for DocuMind AI:

**Technical Context locked**:
- Python 3.11+, CrewAI, openai SDK (AMD endpoint), Streamlit, PyMuPDF, Pillow, uv
- In-memory only, no database
- AMD Instinct MI300X via AMD Developer Cloud (OpenAI-compatible API)
- HF Spaces (Streamlit sdk) for deployment

**Constitution Check**: All 6 principles PASS.

**Project Structure**: Single Python app — app.py + agents/ + pipeline/ + tools/ + models/

**Phase 0 Research** (7 decisions):
1. AMD Dev Cloud = OpenAI-compatible API → use openai SDK with base_url override
2. Qwen2-VL-7B-Instruct for vision (base64 image encoding)
3. Qwen2.5-72B-Instruct for text (AMD cloud)
4. CrewAI sequential process + custom LLM via LLM() class
5. PyMuPDF for PDF parsing + image extraction
6. Streamlit st.status() for real-time agent progress
7. HF Space (sdk: streamlit) for deployment

**Phase 1 Design**:
- data-model.md: 5 entities (UploadedDocument, AgentStatus, Entity, Insight, IntelligenceReport)
- contracts/pipeline.md: 7 internal contracts (loader, 4 agents, crew, parser) + error taxonomy
- quickstart.md: uv-based local setup guide

## Outcome

- ✅ Impact: Complete architecture plan — all decisions made, no NEEDS CLARIFICATION remaining
- 🧪 Tests: tests/ directory defined in project structure
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/pipeline.md
- 🔁 Next prompts: /sp.tasks — generate actionable task list
- 🧠 Reflection: AMD OpenAI-compatible API simplifies integration greatly. CrewAI LLM() class handles custom endpoints cleanly. Streamlit st.status() is perfect for live agent display without websockets.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): all constitution gates PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): /sp.tasks immediately
