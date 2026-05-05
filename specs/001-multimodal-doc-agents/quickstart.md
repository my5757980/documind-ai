# Quickstart: DocuMind AI Local Development

**Branch**: `001-multimodal-doc-agents` | **Date**: 2026-05-04

## Prerequisites

- Python 3.11+
- `uv` installed: `pip install uv` (one-time only)
- AMD Developer Cloud API key (from AMD AI Developer Program)

## 1. Clone and Setup

```bash
git clone https://github.com/YOUR_USERNAME/documind-ai.git
cd documind-ai
uv sync
```

## 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your AMD_API_KEY
```

`.env` contents:
```
AMD_API_KEY=your_amd_developer_cloud_api_key
AMD_BASE_URL=https://api.amd.com/v1
VISION_MODEL=Qwen/Qwen2-VL-7B-Instruct
TEXT_MODEL=Qwen/Qwen2.5-72B-Instruct
```

## 3. Run the App

```bash
uv run streamlit run app.py
```

App opens at `http://localhost:8501`

## 4. Test the Pipeline

Upload any of:
- A PDF file (research paper, invoice, report)
- A JPG or PNG image
- A TXT file

Expected: Report generated in ≤60 seconds with summary, entities, insights,
and action items visible.

## 5. Run Tests

```bash
uv run pytest tests/ -v
```

## Validation Checklist

- [ ] App loads at localhost:8501 without errors
- [ ] PDF upload produces a complete report
- [ ] Image upload produces a complete report
- [ ] All 4 agent status steps visible in UI during processing
- [ ] Download button produces a valid JSON file
- [ ] `.env` is in `.gitignore` (never committed)
