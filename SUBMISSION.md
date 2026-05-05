# DocuMind AI — Lablab.ai Submission Content

## Project Title
DocuMind AI — Multi-Modal Document Intelligence

## Short Description (≤280 chars)
Upload any document. 4 AI agents powered by AMD Instinct MI300X GPUs (via Fireworks AI) analyze it — Vision Agent (Kimi K2.5), Reader Agent, Analyst Agent, Reporter Agent — and deliver a structured intelligence report in under 60 seconds.

## Long Description
DocuMind AI is a multi-modal, multi-agent document intelligence platform built on AMD MI300X GPU infrastructure via Fireworks AI's OpenAI-compatible inference API. It demonstrates what AMD's MI300X GPUs can unlock for real-world AI applications.

**The Problem:** Professionals — researchers, analysts, doctors, lawyers — spend hours manually extracting insights from complex documents containing both text and visual content (charts, diagrams, figures). Existing tools handle text OR images, not both together.

**The Solution:** DocuMind AI runs a sequential 4-agent CrewAI pipeline on AMD Instinct MI300X GPUs:

1. **🔍 Vision Agent** — uses Kimi K2.5 to analyze every image, chart, and diagram embedded in the document
2. **📖 Reader Agent** — uses DeepSeek V3.1 to extract text, identify entities, classify document type, and extract key facts
3. **🧠 Analyst Agent** — synthesizes visual AND textual findings into cross-modal insights, identifying patterns neither modality reveals alone
4. **📋 Reporter Agent** — produces a structured intelligence report: Executive Summary, Key Entities, Categorized Insights, and Actionable Recommendations

Users see real-time agent progress — each agent's activation is shown live in the Streamlit UI. Processing completes in under 60 seconds. The full report downloads as JSON.

**AMD Technology Used:**
- AMD Instinct MI300X GPUs via Fireworks AI (AMD-powered inference provider)
- OpenAI-compatible API — zero-friction integration with CrewAI and Python AI ecosystem
- Kimi K2.5 (vision-language model) + DeepSeek V3.1 (open-source frontier text model)

**Why This Wins:**
- Covers Track 1 (AI Agents) AND Track 3 (Vision/Multimodal) in one project
- Real business value — immediate use case for researchers, analysts, professionals
- Multimodal + multi-agent: both vision and text deeply integrated
- Live demo deployable on Hugging Face Spaces with zero setup for judges
- MIT open-source with detailed Build in Public documentation

## Technology & Category Tags
AMD, AMD-MI300X, Fireworks-AI, CrewAI, DeepSeek, Kimi-K2, Multi-Agent, Vision-AI, Multimodal, Document-Intelligence, Streamlit, Python, AI-Agents, Agentic-Workflows, OpenAI-Compatible

## Social Media Posts (Copy-Paste Ready)

### Post 1 — Technical (for X/Twitter):
```
Built DocuMind AI on AMD MI300X GPUs (via @fireworks_ai) — a 4-agent CrewAI pipeline that analyzes documents with both vision + text understanding.

Architecture:
🔍 Vision Agent (Kimi K2.5) → charts + images
📖 Reader Agent (DeepSeek V3.1) → text + entities
🧠 Analyst Agent → cross-modal synthesis
📋 Reporter Agent → structured report

All running on AMD MI300X hardware.

@lablab @AIatAMD #AMDDeveloperHackathon

GitHub: [YOUR_GITHUB_URL]
```

### Post 2 — Demo (for X/Twitter):
```
DocuMind AI is LIVE on Hugging Face Spaces!

Upload any PDF or image → 4 AMD-powered agents analyze it → get a full intelligence report in <60 seconds.

Built with:
⚡ AMD Instinct MI300X
🤖 CrewAI agents
👁️ Kimi K2.5 vision
📝 DeepSeek V3.1 text

Try it: [HF_SPACE_URL]
Code: [GITHUB_URL]

@lablab @AIatAMD #BuildInPublic
```

### LinkedIn Post 1:
```
Excited to share DocuMind AI — my solo submission for the AMD Developer Hackathon!

DocuMind AI is a multi-modal document intelligence platform powered by AMD Instinct MI300X GPUs via Fireworks AI. It uses a 4-agent CrewAI pipeline with Kimi K2.5 (vision) and DeepSeek V3.1 (text) to analyze any document — PDF, image, or text file — and produce a structured intelligence report in under 60 seconds.

The AMD-powered OpenAI-compatible API made integration seamless. What would normally require complex GPU setup took just an API key swap.

Check it out: [HF_SPACE_URL]
Open source: [GITHUB_URL]

#AIAgents #AMD #MachineLearning @lablab.ai @AMD Developer
```

## Judging Criteria — How DocuMind AI Scores

### 1. Application of Technology
- AMD MI300X: all inference runs on AMD Instinct MI300X via Fireworks AI
- Kimi K2.5: multimodal vision-language model for image/chart understanding
- DeepSeek V3.1: open-source frontier model for document analysis and report writing
- CrewAI: sequential multi-agent orchestration with 4 specialized agents

### 2. Presentation
- Live Streamlit demo with real-time agent progress
- Clean UI showing 4 agent stages
- Downloadable JSON report
- 3-5 minute demo video showing full pipeline

### 3. Business Value
- Reduces document analysis time from hours to seconds
- Works for any professional: researcher, analyst, lawyer, doctor, student
- No setup required — open HF Space URL and upload

### 4. Originality
- Multi-modal + multi-agent combination (most submissions will be one or the other)
- Covers TWO tracks (AI Agents + Vision/Multimodal) in one project
- Cross-modal synthesis — agents that understand BOTH visual and textual content together
