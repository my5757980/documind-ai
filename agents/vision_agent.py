from crewai import Agent, Task, LLM
from typing import List
from tools.image_extractor import image_to_base64


def create_vision_agent(llm: LLM) -> Agent:
    return Agent(
        role="Visual Content Analyst",
        goal="Analyze all visual elements in documents including charts, diagrams, images, and figures to extract meaningful information",
        backstory=(
            "You are an expert visual analyst powered by AMD MI300X GPUs. "
            "You specialize in understanding charts, graphs, diagrams, tables, "
            "and any visual content within documents. You extract data points, "
            "trends, and insights from visual elements that text alone cannot convey."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def create_vision_task(agent: Agent, images: List[bytes], document_name: str) -> Task:
    if not images:
        description = (
            f"Analyze the document '{document_name}'. "
            "No embedded images were found in this document. "
            "Report that no visual content is present and note this in your analysis."
        )
    else:
        img_descriptions = []
        for i, img_bytes in enumerate(images[:5], 1):
            b64 = image_to_base64(img_bytes)
            img_descriptions.append(f"Image {i}: data:image/jpeg;base64,{b64[:100]}... [base64 encoded]")

        description = (
            f"Analyze the visual content of document '{document_name}'. "
            f"This document contains {len(images)} image(s). "
            "For each image, identify: visual element type (chart/diagram/photo/table), "
            "key data points or values shown, trends or patterns visible, "
            "and what insight the visual communicates. "
            "\n\nProvide your analysis in this EXACT format:\n"
            "VISUAL ANALYSIS:\n"
            "- [observation about each visual element]\n"
            "CHARTS/FIGURES: [description of any charts/graphs found, or 'none detected']\n"
            "KEY VISUAL DATA: [any specific numbers, percentages, or data extracted from visuals]\n"
            f"\nImages to analyze: {len(images)} image(s) found in document."
        )

    return Task(
        description=description,
        expected_output=(
            "A structured visual analysis report with sections: "
            "VISUAL ANALYSIS (bullet points), CHARTS/FIGURES, KEY VISUAL DATA"
        ),
        agent=agent,
    )
