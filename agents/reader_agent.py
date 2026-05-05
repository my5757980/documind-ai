from crewai import Agent, Task, LLM


def create_reader_agent(llm: LLM) -> Agent:
    return Agent(
        role="Document Reader and Text Analyst",
        goal="Extract and understand all textual content from documents, identifying key facts, entities, and the document's purpose",
        backstory=(
            "You are an expert document reader running on AMD MI300X GPUs. "
            "You can read and comprehend any type of document — research papers, "
            "invoices, reports, articles, legal documents — and extract structured "
            "information including named entities, key facts, and main topics. "
            "You classify documents and identify their core purpose."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def create_reader_task(agent: Agent, text_content: str, document_name: str) -> Task:
    preview = text_content[:3000] if len(text_content) > 3000 else text_content

    if not text_content.strip():
        description = (
            f"Analyze document '{document_name}'. "
            "No text content was extractable from this document (it may be image-only). "
            "Report that the document appears to contain only visual content."
        )
    else:
        description = (
            f"Read and analyze the following text from document '{document_name}':\n\n"
            f"{preview}\n\n"
            "Extract and structure the following information in EXACT format:\n"
            "DOCUMENT TYPE: [invoice | research paper | report | article | legal | other]\n"
            "MAIN TOPICS: [comma-separated list of 3-7 main topics]\n"
            "KEY FACTS:\n"
            "- [important fact 1]\n"
            "- [important fact 2]\n"
            "- [important fact 3 (add more as needed)]\n"
            "NAMED ENTITIES:\n"
            "- [Name] ([type: person/organization/location/date/metric])\n"
        )

    return Task(
        description=description,
        expected_output=(
            "Structured text analysis with sections: "
            "DOCUMENT TYPE, MAIN TOPICS, KEY FACTS (bullets), NAMED ENTITIES (bullets with types)"
        ),
        agent=agent,
    )
