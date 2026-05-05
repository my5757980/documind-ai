---
description: "Task list for DocuMind AI — Multi-Modal Document Intelligence"
---

# Tasks: DocuMind AI — Multi-Modal Document Intelligence

**Input**: Design documents from `/specs/001-multimodal-doc-agents/`
**Prerequisites**: plan.md ✅ | spec.md ✅ | research.md ✅ | data-model.md ✅ | contracts/pipeline.md ✅

**Organization**: Tasks grouped by user story. Each story is independently
implementable and testable. No TDD requested — no test tasks generated unless
noted.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, environment configuration.

- [x] T001 Initialize uv project: `uv init` in `E:\New folder\documind-ai\`, create `pyproject.toml`
- [x] T002 Add dependencies via uv: `uv add crewai openai streamlit pymupdf pillow python-dotenv`
- [x] T003 [P] Create `.env.example` with AMD_API_KEY, AMD_BASE_URL, VISION_MODEL, TEXT_MODEL placeholders
- [x] T004 [P] Create `.gitignore` — exclude `.env`, `__pycache__/`, `*.pyc`, `.venv/`, `uploaded_*`
- [x] T005 [P] Create `LICENSE` file (MIT, owner: Muhammad Yaseen, year: 2026)
- [x] T006 Create `README.md` with project description, setup instructions, AMD tech stack, HF Space link placeholder
- [x] T007 [P] Create directory structure: `agents/`, `pipeline/`, `tools/`, `models/`, `tests/` with `__init__.py` in each

**Checkpoint**: `uv run python -c "import crewai, streamlit, fitz, openai; print('deps OK')"` succeeds.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure all user stories depend on. MUST complete before any story work.

- [x] T008 Create `config.py` — load AMD_API_KEY, AMD_BASE_URL, VISION_MODEL, TEXT_MODEL from env via python-dotenv; expose `get_amd_llm()` returning CrewAI `LLM` instance pointing to AMD endpoint
- [x] T009 Create `models/report.py` — implement `Entity`, `Insight`, `AgentStatus`, `IntelligenceReport`, `UploadedDocument` dataclasses exactly per `data-model.md`; add `IntelligenceReport.to_dict()` and `to_markdown()` methods
- [x] T010 Create `tools/document_loader.py` — implement `load_document(file_bytes, filename) -> UploadedDocument` per `contracts/pipeline.md Contract 1`; handle PDF (PyMuPDF text + image extraction), JPG/PNG (Pillow → bytes), TXT (decode utf-8); raise `ValueError` on unsupported format or empty file
- [x] T011 Create `tools/image_extractor.py` — implement `extract_images_from_pdf(pdf_bytes) -> List[bytes]` using PyMuPDF `get_images()` + `extract_image()`; convert all extracted images to JPEG bytes at quality=85
- [x] T012 [P] Create `models/report.py` function `parse_reporter_output(raw_output, document_name, agent_statuses, total_duration) -> IntelligenceReport` per `contracts/pipeline.md Contract 7`; parse EXECUTIVE SUMMARY, KEY ENTITIES, INSIGHTS, ACTION ITEMS sections

**Checkpoint**: `uv run python -c "from tools.document_loader import load_document; from models.report import IntelligenceReport; print('foundation OK')"` succeeds.

---

## Phase 3: User Story 1 — Document Upload & Intelligence Extraction (Priority: P1) 🎯 MVP

**Goal**: User uploads a document, all 4 agents run, structured report is returned.

**Independent Test**: Upload `tests/fixtures/sample.pdf` via Streamlit UI →
verify report appears with non-empty summary, ≥1 entity, ≥1 insight, ≥1 action item.

### Implementation for User Story 1

- [x] T013 [US1] Create `agents/vision_agent.py` — implement `create_vision_agent(llm) -> Agent` and `create_vision_task(agent, images, document_name) -> Task` per `contracts/pipeline.md Contract 2`; system prompt instructs agent to analyze visual elements, charts, figures; encode images as base64 for Qwen-VL multimodal input
- [x] T014 [US1] Create `agents/reader_agent.py` — implement `create_reader_agent(llm) -> Agent` and `create_reader_task(agent, text_content, document_name) -> Task` per `contracts/pipeline.md Contract 3`; system prompt instructs agent to extract document type, main topics, key facts, and named entities from plain text
- [x] T015 [US1] Create `agents/analyst_agent.py` — implement `create_analyst_agent(llm) -> Agent` and `create_analyst_task(agent, vision_output, reader_output, document_name) -> Task` per `contracts/pipeline.md Contract 4`; system prompt instructs agent to synthesize cross-modal insights and draft a summary
- [x] T016 [US1] Create `agents/reporter_agent.py` — implement `create_reporter_agent(llm) -> Agent` and `create_reporter_task(agent, analyst_output, document_name) -> Task` per `contracts/pipeline.md Contract 5`; system prompt enforces STRICT output format: EXECUTIVE SUMMARY, KEY ENTITIES, INSIGHTS, ACTION ITEMS sections
- [x] T017 [US1] Create `pipeline/tasks.py` — define all 4 CrewAI Task objects; wire context: analyst task receives vision + reader outputs; reporter task receives analyst output; use `context=[]` parameter for inter-task context passing
- [x] T018 [US1] Create `pipeline/crew.py` — implement `run_pipeline(document, status_callback) -> IntelligenceReport` per `contracts/pipeline.md Contract 6`; assemble `Crew(agents=[...], tasks=[...], process=Process.sequential, verbose=True)`; call `status_callback` after each agent with `AgentStatus`; call `parse_reporter_output()` on final crew output; handle `PipelineError` and `TimeoutError`
- [x] T019 [US1] Create `app.py` — Streamlit UI entry point: page title "DocuMind AI", file uploader accepting pdf/jpg/jpeg/png/txt, call `load_document()` on upload, call `run_pipeline()` on submit button, display pipeline results using `st.status()` context with 4 steps, render final `IntelligenceReport` as formatted sections (summary, entities table, insights list, action items list)

**Checkpoint**: `uv run streamlit run app.py` → upload a PDF → report appears in ≤60 seconds with all 4 sections populated. All 4 agent status steps visible during processing.

---

## Phase 4: User Story 2 — Live Agent Pipeline Visibility (Priority: P2)

**Goal**: Real-time per-agent status shown in UI during processing.

**Independent Test**: Upload any document → observe UI shows each agent name
activating in sequence → all 4 steps show green checkmark on completion.

### Implementation for User Story 2

- [x] T020 [P] [US2] Update `app.py` — replace any simple spinner with `st.status(label="Processing document...", expanded=True)` context manager; inside context add `st.write()` calls before and after each agent stage showing agent name + emoji (🔍 Vision, 📖 Reader, 🧠 Analyst, 📋 Reporter); call `status.update(label="Report ready!", state="complete")` at end
- [x] T021 [US2] Update `pipeline/crew.py` — ensure `status_callback` is invoked with correct `AgentStatus` (agent_name, status="running") BEFORE each agent starts and (status="complete") AFTER it finishes; pass timing data (started_at, completed_at) in `AgentStatus`
- [x] T022 [P] [US2] Add per-agent duration display in `app.py` — after each agent completes, show elapsed time in seconds next to the agent step (e.g., "✅ Vision Agent — 8.3s")

**Checkpoint**: During document processing, all 4 agent names appear on screen in sequence without page refresh. Each shows a running indicator then a completion checkmark.

---

## Phase 5: User Story 3 — Report Download & Export (Priority: P3)

**Goal**: User can download the intelligence report as a JSON file.

**Independent Test**: Generate any report → click "Download Report" button →
verify downloaded JSON file contains all sections: summary, entities, insights,
action_items.

### Implementation for User Story 3

- [x] T023 [P] [US3] Update `models/report.py` — verify `IntelligenceReport.to_dict()` returns JSON-serializable dict with keys: `document_name`, `summary`, `entities` (list of dicts), `insights` (list of dicts), `action_items` (list of strings), `processing_time_seconds`, `created_at`
- [x] T024 [US3] Update `app.py` — after report is displayed, add `st.download_button(label="Download Report (JSON)", data=json.dumps(report.to_dict(), indent=2), file_name=f"{report.document_name}_report.json", mime="application/json")`

**Checkpoint**: Download button appears after report renders. Clicking it downloads a valid JSON file with all report sections. File can be opened in any text editor.

---

## Phase 6: User Story 4 — Multi-Format Document Support (Priority: P4)

**Goal**: PDF, JPG, PNG, and TXT all produce valid reports.

**Independent Test**: Submit one file of each format — PDF, JPG, PNG, TXT —
and verify all four produce complete reports with no errors.

### Implementation for User Story 4

- [x] T025 [US4] Update `tools/document_loader.py` — ensure TXT files are decoded as utf-8 with `errors='replace'`; ensure JPEG files (extension .jpeg) are handled identically to .jpg; add `FileSizeError` raised when `size_bytes > 10_485_760`; add `EmptyDocumentError` raised when both `text_content` is empty and `images` list is empty after loading
- [x] T026 [P] [US4] Update `app.py` — wrap `load_document()` and `run_pipeline()` calls in try/except for `ValueError`, `FileSizeError`, `EmptyDocumentError`, `PipelineError`; display `st.error("...")` with user-friendly message for each error type; ensure UI does not freeze on error — always return to upload state
- [x] T027 [P] [US4] Add `tests/fixtures/` directory — place one sample file of each type: `sample.pdf`, `sample.jpg`, `sample.png`, `sample.txt` for manual validation testing
- [x] T028 [US4] Create `tests/test_document_loader.py` — unit tests for `load_document()`: test PDF loading returns non-empty text, test JPG loading returns non-empty images list, test unsupported format raises ValueError, test oversized file raises FileSizeError, test empty file raises EmptyDocumentError

**Checkpoint**: Upload each of the 4 sample formats. All 4 produce complete reports. Upload an oversized file — see clear error message. UI returns to upload state after error.

---

## Phase 7: Polish & Deployment

**Purpose**: HF Space deployment, social posts, submission preparation.

- [x] T029 Add `README.md` final content — project title, one-line description, AMD tech stack badges, screenshot placeholder, HF Space URL, GitHub repo URL, setup instructions, MIT license badge
- [x] T030 [P] Generate `requirements.txt` via `uv export --no-hashes > requirements.txt` for HF Space compatibility
- [ ] T031 Create HF Space — go to Hugging Face, create new Space in AMD Developer Hackathon organization, SDK=Streamlit, copy repo contents, add AMD_API_KEY as Space secret
- [ ] T032 [P] Verify HF Space is live — open public Space URL, upload a test document, confirm full pipeline runs on HF infrastructure
- [ ] T033 [P] Write social media post 1 (technical) — share architecture diagram or screenshot of 4-agent pipeline running; tag @lablab + @AIatAMD on X; post on LinkedIn tagging AMD Developer
- [ ] T034 [P] Write social media post 2 (demo) — share HF Space URL + demo GIF or screenshot of report output; tag @lablab + @AIatAMD; include open-source GitHub link
- [ ] T035 Submit project on lablab.ai — fill: title, short description, long description, cover image, video presentation URL, slide presentation, GitHub repo URL, HF Space URL, technology tags (AMD, ROCm, CrewAI, Qwen, Multi-Agent, Vision AI, Python)
- [ ] T036 [P] Record 3-5 minute demo video — show: file upload → live agent progress → full report → download JSON; narrate AMD MI300X GPU usage and 4-agent architecture

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately ✅
- **Foundational (Phase 2)**: Depends on Phase 1 completion — BLOCKS all user stories
- **US1 — P1 (Phase 3)**: Depends on Phase 2 — this is MVP 🎯
- **US2 — P2 (Phase 4)**: Depends on Phase 3 (builds on app.py + crew.py)
- **US3 — P3 (Phase 5)**: Depends on Phase 3 (builds on report model)
- **US4 — P4 (Phase 6)**: Depends on Phase 3 (builds on document_loader)
- **Polish (Phase 7)**: Depends on all user stories

### User Story Dependencies

- **US1 (P1)**: Independent after Phase 2 — no other story dependency ✅
- **US2 (P2)**: Depends on US1 (modifies app.py and crew.py created in US1)
- **US3 (P3)**: Depends on US1 (uses IntelligenceReport from US1 pipeline)
- **US4 (P4)**: Depends on US1 (extends document_loader used by US1)

### Parallel Opportunities Within Each Phase

**Phase 1 (Setup)**:
```
T001, T002 → sequential (T002 depends on T001)
T003, T004, T005, T006, T007 → all parallel once T001 done
```

**Phase 2 (Foundational)**:
```
T008 → must complete first (config needed by T009, T010)
T009, T010, T011 → parallel after T008
T012 → parallel with T009/T010/T011
```

**Phase 3 (US1 — MVP)**:
```
T013, T014, T015, T016 → parallel (each in different file, no deps)
T017 → after T013-T016 (wires tasks together)
T018 → after T017 (assembles crew)
T019 → after T018 (UI calls crew)
```

---

## Implementation Strategy

### Day-by-Day Sprint Plan

| Day | Phases | Goal |
|-----|--------|------|
| Day 1 (May 4) | Phase 1 + Phase 2 | Project setup + foundational models |
| Day 2 (May 5) | Phase 3 (T013-T018) | All 4 agents + pipeline |
| Day 3 (May 6) | Phase 3 (T019) + Phase 4 | Streamlit UI + live status |
| Day 4 (May 7) | Phase 5 + Phase 6 | Download + multi-format support |
| Day 5 (May 8) | Phase 7 (T029-T032) | Deploy to HF Space + test live |
| Day 6 (May 9) | Phase 7 (T033-T036) | Social posts + video + submit |

### MVP Definition (US1 Only)

Complete Phase 1 → Phase 2 → Phase 3 (T001-T019) → working demo.

This alone qualifies for Track 1 (AI Agents), Track 3 (Vision/Multimodal),
Grand Prize, and HF Prize eligibility. Everything after is bonus.

---

## Notes

- [P] = parallelizable (different files, no incomplete task dependency)
- [USN] = maps task to user story for traceability
- `uv run` prefix REQUIRED for all Python/Streamlit commands (never use `python` or `pip` directly)
- Commit after each phase checkpoint passes
- Total tasks: 36 | Setup: 7 | Foundational: 5 | US1: 7 | US2: 3 | US3: 2 | US4: 4 | Polish: 7 | Tests: 1
