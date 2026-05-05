---
title: DocuMind AI
emoji: 🧠
colorFrom: purple
colorTo: blue
sdk: streamlit
sdk_version: 1.32.2
app_file: app.py
pinned: true
license: mit
---

# DocuMind AI — Multi-Modal Document Intelligence

**AMD Developer Hackathon 2026** | Track 1: AI Agents & Agentic Workflows | Track 3: Vision & Multimodal AI

Upload any document (PDF, image, TXT). Four specialized AI agents powered by **AMD Instinct MI300X GPUs** via Fireworks AI (AMD-powered inference) analyze it and deliver a structured intelligence report in under 60 seconds.

## Live Demo

🚀 **[Try it on Hugging Face Spaces](https://huggingface.co/spaces/YOUR_HF_ORG/documind-ai)**

## How It Works

```
Document Upload (PDF / JPG / PNG / TXT)
            │
    ┌───────▼────────┐
    │  🔍 Vision Agent │  ← Kimi K2.5 on AMD MI300X (Fireworks AI)
    │  Analyzes images,│    Charts, diagrams, figures
    │  charts, figures │
    └───────┬────────┘
            │
    ┌───────▼────────┐
    │  📖 Reader Agent │  ← DeepSeek V3.1 on AMD MI300X (Fireworks AI)
    │  Extracts text, │    Entities, facts, document type
    │  entities, facts │
    └───────┬────────┘
            │
    ┌───────▼────────┐
    │  🧠 Analyst Agent│  ← DeepSeek V3.1 on AMD MI300X (Fireworks AI)
    │  Cross-modal    │    Synthesizes vision + text findings
    │  intelligence   │
    └───────┬────────┘
            │
    ┌───────▼────────┐
    │  📋 Reporter    │  ← DeepSeek V3.1 on AMD MI300X (Fireworks AI)
    │  Agent          │    Structured final report
    └───────┬────────┘
            │
    Intelligence Report
    (Summary + Entities + Insights + Action Items + JSON Download)
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| GPU | AMD Instinct MI300X via Fireworks AI (AMD-powered) |
| Inference Provider | Fireworks AI — OpenAI-compatible API on AMD hardware |
| Vision Model | Kimi K2.5 (`accounts/fireworks/models/kimi-k2p5`) |
| Text Model | DeepSeek V3.1 (`accounts/fireworks/models/deepseek-v3p1`) |
| Agent Framework | CrewAI (sequential pipeline) |
| UI | Streamlit |
| Language | Python 3.11+ |
| Package Manager | uv |

## Features

- **4-Agent CrewAI Pipeline** — specialized agents work sequentially, each building on the last
- **Multimodal Understanding** — processes both text AND embedded images/charts in same document
- **AMD MI300X Powered** — all inference runs on AMD Instinct MI300X via Fireworks AI
- **Kimi K2.5** — state-of-the-art vision-language model for image/chart analysis
- **DeepSeek V3.1** — open-source frontier model for text reasoning and report writing
- **Live Agent Progress** — real-time display of which agent is running
- **JSON Export** — download full structured report
- **Multi-Format** — PDF, JPG, PNG, TXT (up to 10 MB)

## Local Setup

```bash
git clone https://github.com/YOUR_USERNAME/documind-ai.git
cd documind-ai
uv sync
cp .env.example .env
# Edit .env — add your Fireworks AI API key from app.fireworks.ai/settings/users/api-keys
uv run streamlit run app.py
```

## Environment Variables

```env
AMD_API_KEY=your_fireworks_api_key_here
AMD_BASE_URL=https://api.fireworks.ai/inference/v1
VISION_MODEL=accounts/fireworks/models/kimi-k2p5
TEXT_MODEL=accounts/fireworks/models/deepseek-v3p1
```

Get your free API key at [fireworks.ai](https://fireworks.ai) — $6 free credit, no payment needed.

## Supported Formats

| Format | Text Extraction | Image Extraction |
|--------|----------------|-----------------|
| PDF | ✅ PyMuPDF | ✅ Embedded images |
| JPG / JPEG | ❌ | ✅ Full image |
| PNG | ❌ | ✅ Full image |
| TXT | ✅ UTF-8 | ❌ |

## Build in Public — AMD Developer Experience Feedback

Building DocuMind AI on AMD-powered infrastructure revealed several key insights:

**What worked great:**
- Fireworks AI provides an **OpenAI-compatible API on AMD MI300X GPUs** — zero SDK changes needed, just swap `base_url` and `api_key`
- **Kimi K2.5** multimodal model handles base64 image encoding identically to OpenAI Vision API
- **CrewAI's LLM class** integrates cleanly with custom endpoints — `LLM(model="openai/accounts/fireworks/models/deepseek-v3p1", base_url=AMD_BASE_URL)` just works
- **DeepSeek V3.1** on AMD hardware delivers frontier-level reasoning for document analysis

**Developer experience notes:**
- The OpenAI-compatible interface dramatically lowers barrier to entry — existing Python AI code migrates in minutes
- AMD MI300X's large memory bandwidth is ideal for multimodal workloads processing both vision and text simultaneously
- Serverless inference via Fireworks AI means no GPU provisioning or infrastructure management

**Improvement suggestions:**
- A curated list of confirmed serverless model IDs available on AMD-powered infrastructure would help developers choose faster
- Example notebooks showing CrewAI + AMD inference integration would accelerate adoption

## Project Structure

```
documind-ai/
├── app.py                    # Streamlit UI
├── config.py                 # LLM factory (Fireworks AI / AMD-powered)
├── agents/
│   ├── vision_agent.py       # Kimi K2.5 vision analysis
│   ├── reader_agent.py       # DeepSeek V3.1 text extraction
│   ├── analyst_agent.py      # Cross-modal synthesis
│   └── reporter_agent.py     # Structured report generation
├── pipeline/
│   ├── crew.py               # CrewAI sequential pipeline
│   └── tasks.py              # Task definitions
├── tools/
│   ├── document_loader.py    # PDF/image/text loader
│   └── image_extractor.py    # PyMuPDF image extractor
├── models/
│   └── report.py             # Data models + parser
└── tests/
    └── test_document_loader.py  # 7/7 passing
```

## License

MIT — See [LICENSE](LICENSE)

---

*Built with ❤️ on AMD MI300X GPUs • Fireworks AI • DeepSeek V3.1 • Kimi K2.5 • CrewAI • Streamlit*
*AMD Developer Hackathon 2026 — Solo submission by Muhammad Yaseen*
"# documind-ai" 
