from crewai import Task, Agent
from typing import List


def build_vision_task(agent: Agent, images: List[bytes], document_name: str) -> Task:
    from agents.vision_agent import create_vision_task
    return create_vision_task(agent, images, document_name)


def build_reader_task(agent: Agent, text_content: str, document_name: str) -> Task:
    from agents.reader_agent import create_reader_task
    return create_reader_task(agent, text_content, document_name)


def build_analyst_task(
    agent: Agent,
    vision_task: Task,
    reader_task: Task,
    document_name: str,
) -> Task:
    from agents.analyst_agent import create_analyst_task
    return Task(
        description=(
            f"Synthesize visual and text analyses of '{document_name}' "
            "from prior agent outputs to generate cross-modal insights.\n\n"
            "Generate your synthesis in EXACT format:\n"
            "INSIGHTS:\n"
            "- [FINDING|CONCLUSION|RISK|OPPORTUNITY] ([visual|text|combined]): [insight text]\n"
            "SUMMARY DRAFT: [3-5 sentence executive summary]\n"
        ),
        expected_output=(
            "Cross-modal synthesis with INSIGHTS (categorized bullets) "
            "and SUMMARY DRAFT (3-5 sentences)"
        ),
        agent=agent,
        context=[vision_task, reader_task],
    )


def build_reporter_task(
    agent: Agent,
    analyst_task: Task,
    document_name: str,
) -> Task:
    return Task(
        description=(
            f"Create the final intelligence report for document '{document_name}' "
            "based on all prior agent analyses.\n\n"
            "Use STRICT format with these EXACT section headers:\n\n"
            "EXECUTIVE SUMMARY:\n"
            "[3-5 clear sentences]\n\n"
            "KEY ENTITIES:\n"
            "- [Name] | [type] | [context sentence]\n\n"
            "INSIGHTS:\n"
            "- [FINDING|CONCLUSION|RISK|OPPORTUNITY] | [visual|text|combined] | [text]\n\n"
            "ACTION ITEMS:\n"
            "- [actionable recommendation]\n"
        ),
        expected_output=(
            "Complete structured report: EXECUTIVE SUMMARY, KEY ENTITIES, INSIGHTS, ACTION ITEMS"
        ),
        agent=agent,
        context=[analyst_task],
    )
