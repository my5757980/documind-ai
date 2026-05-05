from crewai import Agent, Task, LLM


def create_analyst_agent(llm: LLM) -> Agent:
    return Agent(
        role="Multi-Modal Intelligence Analyst",
        goal="Synthesize visual and textual findings to generate cross-modal insights and a comprehensive document summary",
        backstory=(
            "You are a senior intelligence analyst powered by AMD MI300X GPUs. "
            "You receive both visual analysis and text analysis of a document and "
            "synthesize them into coherent, actionable insights. You identify patterns "
            "that span both modalities, highlight risks and opportunities, and draft "
            "executive summaries that capture the document's essential intelligence."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def create_analyst_task(
    agent: Agent,
    vision_output: str,
    reader_output: str,
    document_name: str,
) -> Task:
    description = (
        f"Synthesize the following analyses of document '{document_name}' "
        "to generate cross-modal intelligence.\n\n"
        f"=== VISUAL ANALYSIS ===\n{vision_output}\n\n"
        f"=== TEXT ANALYSIS ===\n{reader_output}\n\n"
        "Generate your synthesis in EXACT format:\n"
        "INSIGHTS:\n"
        "- [FINDING|CONCLUSION|RISK|OPPORTUNITY] ([visual|text|combined]): [insight text]\n"
        "- [add 3-6 insights total]\n"
        "SUMMARY DRAFT: [Write a 3-5 sentence executive summary that integrates "
        "both visual and textual findings. Be specific and factual.]\n"
    )

    return Task(
        description=description,
        expected_output=(
            "Cross-modal synthesis with INSIGHTS (categorized bullets) "
            "and SUMMARY DRAFT (3-5 sentences)"
        ),
        agent=agent,
    )
