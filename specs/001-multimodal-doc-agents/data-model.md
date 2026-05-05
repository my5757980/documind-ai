# Data Model: DocuMind AI

**Branch**: `001-multimodal-doc-agents` | **Date**: 2026-05-04

All models are Python `dataclasses`. No database. All instances live in
memory for the duration of a single Streamlit session.

---

## Entity: UploadedDocument

Represents the raw user-uploaded file before any processing.

```python
@dataclass
class UploadedDocument:
    name: str               # original filename
    format: str             # "pdf" | "jpg" | "png" | "txt"
    raw_bytes: bytes        # file content
    size_bytes: int         # file size
    text_content: str       # extracted plain text (populated by document_loader)
    images: List[bytes]     # extracted image bytes (populated by document_loader)
    page_count: int         # number of pages (PDFs only; 1 for images/text)
```

**Validation rules**:
- `format` MUST be one of: `pdf`, `jpg`, `jpeg`, `png`, `txt`
- `size_bytes` MUST be ≤ 10,485,760 (10 MB hard limit; 5 MB soft target)
- `raw_bytes` MUST NOT be empty

**State transitions**: `raw` → `loaded` (after document_loader runs) →
`processed` (after pipeline completes)

---

## Entity: AgentStatus

Tracks real-time state of a single pipeline agent. Used by Streamlit UI
for live progress display.

```python
@dataclass
class AgentStatus:
    agent_name: str         # "Vision Agent" | "Reader Agent" | "Analyst Agent" | "Reporter Agent"
    status: str             # "pending" | "running" | "complete" | "error"
    message: str            # human-readable status message for UI display
    started_at: Optional[float]   # Unix timestamp
    completed_at: Optional[float] # Unix timestamp
    error: Optional[str]    # error message if status == "error"

    @property
    def duration_seconds(self) -> Optional[float]:
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return None
```

**Status flow**: `pending` → `running` → `complete` (success path)
                 `pending` → `running` → `error` (failure path)

---

## Entity: Entity (document entity)

A named concept, person, organization, or term extracted from the document.

```python
@dataclass
class Entity:
    name: str               # extracted name or term
    type: str               # "person" | "organization" | "location" | "concept" | "date" | "metric"
    context: str            # one-sentence context from the document
    mentions: int           # estimated occurrence count in document
```

---

## Entity: Insight

A key finding, conclusion, risk, or opportunity derived by the Analyst Agent.

```python
@dataclass
class Insight:
    content: str            # the insight text (1-3 sentences)
    category: str           # "finding" | "conclusion" | "risk" | "opportunity"
    source: str             # "visual" | "text" | "combined"
```

---

## Entity: IntelligenceReport

The complete output of the 4-agent pipeline. This is what the user sees and
can download.

```python
@dataclass
class IntelligenceReport:
    document_name: str          # from UploadedDocument.name
    summary: str                # 3-5 sentence executive summary
    entities: List[Entity]      # extracted named entities
    insights: List[Insight]     # key findings and conclusions
    action_items: List[str]     # recommended next steps (plain strings)
    agent_statuses: List[AgentStatus]  # one per agent, in pipeline order
    total_duration_seconds: float
    created_at: str             # ISO 8601 timestamp

    def to_dict(self) -> dict:
        """Serialize to JSON-safe dict for download."""
        ...

    def to_markdown(self) -> str:
        """Render as readable markdown string."""
        ...
```

**Completeness rule**: A report is only valid if:
- `summary` is non-empty
- `entities` has ≥ 1 item
- `insights` has ≥ 1 item
- All 4 `agent_statuses` have `status == "complete"`

---

## Entity Relationships

```text
UploadedDocument
    │
    ├── (input to) ──► DocuMindCrew (pipeline/crew.py)
    │                       │
    │           ┌───────────┼───────────────────┐
    │           ▼           ▼                   ▼
    │      VisionAgent  ReaderAgent  AnalystAgent  ReporterAgent
    │           │           │              │             │
    │           └───────────┴──────────────┘             │
    │                       │                           │
    │               (produces context)          (final output)
    │                                                   │
    └────────────────────────────────────────► IntelligenceReport
                                                    │
                                                    ├── List[Entity]
                                                    ├── List[Insight]
                                                    ├── List[str] (action_items)
                                                    └── List[AgentStatus]
```
