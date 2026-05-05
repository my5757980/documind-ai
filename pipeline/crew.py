import time
from typing import Callable
from crewai import Crew, Process

from config import get_amd_llm, get_vision_llm
from models.report import (
    UploadedDocument, IntelligenceReport, AgentStatus,
    PipelineError, parse_reporter_output
)
from agents.vision_agent import create_vision_agent, create_vision_task
from agents.reader_agent import create_reader_agent, create_reader_task
from agents.analyst_agent import create_analyst_agent
from agents.reporter_agent import create_reporter_agent
from pipeline.tasks import build_analyst_task, build_reporter_task

PIPELINE_TIMEOUT = 120


def run_pipeline(
    document: UploadedDocument,
    status_callback: Callable[[AgentStatus], None],
) -> IntelligenceReport:
    pipeline_start = time.time()
    llm = get_amd_llm()
    vision_llm = get_vision_llm()

    statuses: list[AgentStatus] = [
        AgentStatus(agent_name="Vision Agent"),
        AgentStatus(agent_name="Reader Agent"),
        AgentStatus(agent_name="Analyst Agent"),
        AgentStatus(agent_name="Reporter Agent"),
    ]

    try:
        # Build agents
        vision_agent = create_vision_agent(vision_llm)
        reader_agent = create_reader_agent(llm)
        analyst_agent = create_analyst_agent(llm)
        reporter_agent = create_reporter_agent(llm)

        # Build tasks
        vision_task = create_vision_task(vision_agent, document.images, document.name)
        reader_task = create_reader_task(reader_agent, document.text_content, document.name)
        analyst_task = build_analyst_task(analyst_agent, vision_task, reader_task, document.name)
        reporter_task = build_reporter_task(reporter_agent, analyst_task, document.name)

        # Update status: all running
        for i, name in enumerate(["Vision Agent", "Reader Agent", "Analyst Agent", "Reporter Agent"]):
            statuses[i].status = "pending"
            statuses[i].message = f"{name} queued"
            status_callback(statuses[i])

        # Run crew sequentially
        statuses[0].status = "running"
        statuses[0].started_at = time.time()
        statuses[0].message = "Analyzing visual content on AMD MI300X..."
        status_callback(statuses[0])

        statuses[1].status = "running"
        statuses[1].started_at = time.time()
        statuses[1].message = "Extracting text content on AMD MI300X..."
        status_callback(statuses[1])

        crew = Crew(
            agents=[vision_agent, reader_agent, analyst_agent, reporter_agent],
            tasks=[vision_task, reader_task, analyst_task, reporter_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()

        # Mark all complete
        now = time.time()
        for i, status in enumerate(statuses):
            status.status = "complete"
            status.completed_at = now
            if not status.started_at:
                status.started_at = now - 5
            status_callback(status)

        raw_output = str(result)
        total_duration = time.time() - pipeline_start

        return parse_reporter_output(raw_output, document.name, statuses, total_duration)

    except Exception as e:
        for status in statuses:
            if status.status in ("pending", "running"):
                status.status = "error"
                status.error = str(e)
                status_callback(status)
        raise PipelineError(f"Pipeline failed: {e}") from e
