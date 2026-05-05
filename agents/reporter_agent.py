from crewai import Agent, Task, LLM


def create_reporter_agent(llm: LLM) -> Agent:
    return Agent(
        role="Intelligence Report Writer",
        goal="Produce a final structured intelligence report that is clear, actionable, and immediately useful to the user",
        backstory=(
            "You are a professional report writer running on AMD MI300X GPUs. "
            "You take raw analytical findings and transform them into polished, "
            "structured reports that executives and professionals can act on immediately. "
            "You write with precision and clarity, ensuring every section is complete "
            "and every recommendation is actionable."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def create_reporter_task(agent: Agent, analyst_output: str, document_name: str) -> Task:
    description = (
        f"Create the final intelligence report for document '{document_name}' "
        "based on the following analyst synthesis:\n\n"
        f"{analyst_output}\n\n"
        "Produce the report in STRICT format (use these EXACT section headers):\n\n"
        "EXECUTIVE SUMMARY:\n"
        "[Write 3-5 clear, specific sentences summarizing the document's key content and significance]\n\n"
        "KEY ENTITIES:\n"
        "- [Entity Name] | [type: person/organization/location/concept/metric/date] | [one sentence context]\n"
        "- [add 3-8 entities]\n\n"
        "INSIGHTS:\n"
        "- [FINDING|CONCLUSION|RISK|OPPORTUNITY] | [visual|text|combined] | [insight text]\n"
        "- [add 3-6 insights]\n\n"
        "ACTION ITEMS:\n"
        "- [Specific, actionable recommendation 1]\n"
        "- [Specific, actionable recommendation 2]\n"
        "- [add 2-5 action items]\n"
    )

    return Task(
        description=description,
        expected_output=(
            "A complete structured report with four sections: "
            "EXECUTIVE SUMMARY, KEY ENTITIES (pipe-delimited), "
            "INSIGHTS (pipe-delimited with category and source), ACTION ITEMS"
        ),
        agent=agent,
    )
