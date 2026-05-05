# Internal Contracts: DocuMind AI Pipeline

**Branch**: `001-multimodal-doc-agents` | **Date**: 2026-05-04

DocuMind AI is a Streamlit app — there is no external REST API. These
contracts define the internal function signatures that each layer must
honour so components are independently testable and replaceable.

---

## Contract 1: Document Loader

**Module**: `tools/document_loader.py`

```python
def load_document(file_bytes: bytes, filename: str) -> UploadedDocument:
    """
    Parse a raw uploaded file into a structured UploadedDocument.

    Args:
        file_bytes: Raw bytes from Streamlit file_uploader
        filename:   Original filename including extension

    Returns:
        UploadedDocument with text_content and images populated

    Raises:
        ValueError: if format unsupported or file empty
        ValueError: if file exceeds 10 MB size limit
    """
```

**Guarantees**:
- Always returns `text_content` as a non-None string (empty string if no text)
- Always returns `images` as a non-None list (empty list if no images)
- Never raises on valid PDF/JPG/PNG/TXT within size limit
- Duration: ≤5 seconds for files ≤5 MB

---

## Contract 2: Vision Agent

**Module**: `agents/vision_agent.py`

```python
def create_vision_agent(llm: LLM) -> Agent:
    """
    Build the CrewAI Vision Agent.

    The agent MUST:
    - Accept image bytes (base64-encoded) in its task context
    - Return a structured string describing: visual elements, charts,
      diagrams, key visual data points, and layout observations
    - Complete each image analysis in ≤15 seconds via AMD Cloud API
    """

def create_vision_task(agent: Agent, images: List[bytes], document_name: str) -> Task:
    """
    Create the CrewAI Task for the Vision Agent.

    Task output format (returned as string):
        VISUAL ANALYSIS:
        - [observation 1]
        - [observation 2]
        CHARTS/FIGURES: [description or "none detected"]
        KEY VISUAL DATA: [extracted data points or "none"]
    """
```

---

## Contract 3: Reader Agent

**Module**: `agents/reader_agent.py`

```python
def create_reader_agent(llm: LLM) -> Agent:
    """
    Build the CrewAI Reader Agent.

    The agent MUST:
    - Accept plain text content in its task context
    - Return a structured string with: main topics, key facts,
      named entities (people/orgs/places/dates), and document type classification
    - Complete in ≤15 seconds via AMD Cloud API
    """

def create_reader_task(agent: Agent, text_content: str, document_name: str) -> Task:
    """
    Create the CrewAI Task for the Reader Agent.

    Task output format:
        DOCUMENT TYPE: [invoice | research paper | report | article | other]
        MAIN TOPICS: [comma-separated topics]
        KEY FACTS:
        - [fact 1]
        - [fact 2]
        NAMED ENTITIES:
        - [name] ([type: person/org/location/date/concept])
    """
```

---

## Contract 4: Analyst Agent

**Module**: `agents/analyst_agent.py`

```python
def create_analyst_agent(llm: LLM) -> Agent:
    """
    Build the CrewAI Analyst Agent.

    The agent MUST:
    - Receive both Vision Agent output and Reader Agent output as context
    - Synthesize cross-modal insights (text + visual combined)
    - Return structured insights with categories and sources
    - Complete in ≤15 seconds via AMD Cloud API
    """

def create_analyst_task(
    agent: Agent,
    vision_output: str,
    reader_output: str,
    document_name: str
) -> Task:
    """
    Task output format:
        INSIGHTS:
        - [FINDING|CONCLUSION|RISK|OPPORTUNITY] ([visual|text|combined]): [insight text]
        SUMMARY DRAFT: [3-5 sentence summary paragraph]
    """
```

---

## Contract 5: Reporter Agent

**Module**: `agents/reporter_agent.py`

```python
def create_reporter_agent(llm: LLM) -> Agent:
    """
    Build the CrewAI Reporter Agent.

    The agent MUST:
    - Receive all prior agent outputs as context
    - Produce a final structured report in the exact format below
    - Complete in ≤15 seconds via AMD Cloud API
    """

def create_reporter_task(
    agent: Agent,
    analyst_output: str,
    document_name: str
) -> Task:
    """
    Task output format (STRICT — parsed by models/report.py):
        EXECUTIVE SUMMARY:
        [3-5 sentences]

        KEY ENTITIES:
        - [name] | [type] | [context sentence]

        INSIGHTS:
        - [FINDING|CONCLUSION|RISK|OPPORTUNITY] | [visual|text|combined] | [insight text]

        ACTION ITEMS:
        - [action item 1]
        - [action item 2]
    """
```

---

## Contract 6: DocuMind Crew (Pipeline Orchestrator)

**Module**: `pipeline/crew.py`

```python
def run_pipeline(
    document: UploadedDocument,
    status_callback: Callable[[AgentStatus], None]
) -> IntelligenceReport:
    """
    Execute the full 4-agent pipeline sequentially.

    Args:
        document:        Loaded UploadedDocument (text + images populated)
        status_callback: Called after each agent completes with its AgentStatus.
                         Used by Streamlit UI to update live progress display.

    Returns:
        Complete IntelligenceReport with all sections populated

    Raises:
        PipelineError: if any agent fails and cannot recover
        TimeoutError:  if total pipeline exceeds 120 seconds

    Agent execution order (MUST be sequential, not parallel):
        1. Vision Agent   → processes document.images
        2. Reader Agent   → processes document.text_content
        3. Analyst Agent  → receives Vision + Reader outputs as context
        4. Reporter Agent → receives Analyst output as context → produces report
    """
```

---

## Contract 7: Report Parser

**Module**: `models/report.py`

```python
def parse_reporter_output(
    raw_output: str,
    document_name: str,
    agent_statuses: List[AgentStatus],
    total_duration: float
) -> IntelligenceReport:
    """
    Parse the Reporter Agent's structured text output into an IntelligenceReport.

    Parsing rules:
    - Split on section headers: EXECUTIVE SUMMARY:, KEY ENTITIES:, INSIGHTS:, ACTION ITEMS:
    - Parse entities as: name | type | context (pipe-delimited)
    - Parse insights as: category | source | content (pipe-delimited)
    - Action items: lines starting with "- "

    Raises:
        ValueError: if output missing required sections
    """
```

---

## Error Taxonomy

| Error | When | Recovery |
|-------|------|----------|
| `UnsupportedFormatError` | File type not in [pdf, jpg, png, txt] | Show message, allow re-upload |
| `FileSizeError` | File > 10 MB | Show message with size limit |
| `EmptyDocumentError` | No text and no images extracted | Show message, allow re-upload |
| `AgentTimeoutError` | Single agent exceeds 20s | Show partial results with warning |
| `PipelineError` | Agent API call fails | Show error state, allow retry |
| `ParseError` | Reporter output malformed | Show raw output with warning |
