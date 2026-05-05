from dataclasses import dataclass, field
from typing import List, Optional
import time
import json


@dataclass
class Entity:
    name: str
    type: str
    context: str
    mentions: int = 1


@dataclass
class Insight:
    content: str
    category: str  # finding | conclusion | risk | opportunity
    source: str    # visual | text | combined


@dataclass
class AgentStatus:
    agent_name: str
    status: str = "pending"  # pending | running | complete | error
    message: str = ""
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    error: Optional[str] = None

    @property
    def duration_seconds(self) -> Optional[float]:
        if self.started_at and self.completed_at:
            return round(self.completed_at - self.started_at, 1)
        return None


@dataclass
class UploadedDocument:
    name: str
    format: str
    raw_bytes: bytes
    size_bytes: int
    text_content: str = ""
    images: List[bytes] = field(default_factory=list)
    page_count: int = 1


@dataclass
class IntelligenceReport:
    document_name: str
    summary: str
    entities: List[Entity]
    insights: List[Insight]
    action_items: List[str]
    agent_statuses: List[AgentStatus]
    total_duration_seconds: float
    created_at: str

    def to_dict(self) -> dict:
        return {
            "document_name": self.document_name,
            "summary": self.summary,
            "entities": [
                {"name": e.name, "type": e.type, "context": e.context, "mentions": e.mentions}
                for e in self.entities
            ],
            "insights": [
                {"content": i.content, "category": i.category, "source": i.source}
                for i in self.insights
            ],
            "action_items": self.action_items,
            "processing_time_seconds": self.total_duration_seconds,
            "created_at": self.created_at,
        }

    def to_markdown(self) -> str:
        lines = [f"# DocuMind AI Report: {self.document_name}\n"]
        lines.append(f"## Executive Summary\n{self.summary}\n")
        lines.append("## Key Entities")
        for e in self.entities:
            lines.append(f"- **{e.name}** ({e.type}): {e.context}")
        lines.append("\n## Insights")
        for i in self.insights:
            lines.append(f"- [{i.category.upper()}] ({i.source}): {i.content}")
        lines.append("\n## Action Items")
        for a in self.action_items:
            lines.append(f"- {a}")
        return "\n".join(lines)


class FileSizeError(ValueError):
    pass


class EmptyDocumentError(ValueError):
    pass


class PipelineError(RuntimeError):
    pass


def parse_reporter_output(
    raw_output: str,
    document_name: str,
    agent_statuses: List[AgentStatus],
    total_duration: float,
) -> IntelligenceReport:
    import datetime

    sections = {
        "EXECUTIVE SUMMARY": "",
        "KEY ENTITIES": "",
        "INSIGHTS": "",
        "ACTION ITEMS": "",
    }

    current = None
    for line in raw_output.splitlines():
        stripped = line.strip()
        matched = False
        for key in sections:
            if stripped.upper().startswith(key + ":") or stripped.upper() == key:
                current = key
                rest = stripped[len(key):].lstrip(":").strip()
                if rest:
                    sections[key] += rest + "\n"
                matched = True
                break
        if not matched and current:
            sections[current] += line + "\n"

    summary = sections["EXECUTIVE SUMMARY"].strip()

    entities: List[Entity] = []
    for line in sections["KEY ENTITIES"].splitlines():
        line = line.strip().lstrip("- ").strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3:
            entities.append(Entity(name=parts[0], type=parts[1], context=parts[2]))
        elif len(parts) == 2:
            entities.append(Entity(name=parts[0], type=parts[1], context=""))
        elif parts[0]:
            entities.append(Entity(name=parts[0], type="concept", context=""))

    insights: List[Insight] = []
    for line in sections["INSIGHTS"].splitlines():
        line = line.strip().lstrip("- ").strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3:
            insights.append(Insight(content=parts[2], category=parts[0].lower(), source=parts[1].lower()))
        elif parts[0]:
            insights.append(Insight(content=parts[0], category="finding", source="combined"))

    action_items: List[str] = []
    for line in sections["ACTION ITEMS"].splitlines():
        line = line.strip().lstrip("- ").strip()
        if line:
            action_items.append(line)

    if not summary:
        summary = raw_output[:500].strip()
    if not entities:
        entities = [Entity(name="Document Content", type="concept", context="See summary for details")]
    if not insights:
        insights = [Insight(content="Analysis complete. Review summary for key findings.", category="finding", source="combined")]
    if not action_items:
        action_items = ["Review the executive summary for key takeaways"]

    return IntelligenceReport(
        document_name=document_name,
        summary=summary,
        entities=entities,
        insights=insights,
        action_items=action_items,
        agent_statuses=agent_statuses,
        total_duration_seconds=round(total_duration, 1),
        created_at=datetime.datetime.utcnow().isoformat() + "Z",
    )
