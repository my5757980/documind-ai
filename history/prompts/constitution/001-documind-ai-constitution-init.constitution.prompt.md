---
id: 001
title: DocuMind AI Constitution Init
stage: constitution
date: 2026-05-04
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: Muhammad Yaseen
command: /sp.constitution
labels: ["constitution","amd-hackathon","documind-ai","multi-agent","vision-ai"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/001-documind-ai-constitution-init.constitution.prompt.md
tests:
  - none
---

## Prompt

DocuMind AI — AMD Developer Hackathon project. Multi-Modal Multi-Agent Document Intelligence Platform. Runs on AMD Developer Cloud (MI300X GPUs) using ROCm. Uses Qwen-VL (vision) + Qwen2.5 (text) models via CrewAI agents. Python + FastAPI backend. Streamlit UI. Deployed on Hugging Face Space + GitHub open-source. Goal: WIN AMD Developer Hackathon — Track 1 (AI Agents), Track 3 (Vision/Multimodal), Grand Prize $5000, Hugging Face Prize, Build in Public Prize. Solo project by Muhammad Yaseen from Pakistan. Deadline: May 11 2026 12:00 AM Pakistan time. Core principles: (1) AMD-first — everything runs on AMD MI300X via ROCm (2) 4-agent pipeline — Vision Agent, Reader Agent, Analyst Agent, Reporter Agent (3) End-to-end working demo required (4) Hugging Face Space deployment mandatory (5) Open source MIT license (6) Speed over perfection — ship in 6 days

## Response snapshot

Constitution v1.0.0 created for DocuMind AI with 6 core principles:
I. AMD-First Computing — all compute on MI300X via ROCm
II. 4-Agent Pipeline (NON-NEGOTIABLE) — Vision/Reader/Analyst/Reporter agents via CrewAI
III. End-to-End Working Demo — must run in <60s, always demonstrable
IV. Open Source & Deploy-First — MIT + HF Space mandatory
V. Speed Over Perfection — 6-day sprint, Streamlit UI, YAGNI enforced
VI. Multi-Prize Targeting Strategy — Grand Prize + Track 1 + Track 3 + HF + Build in Public + Qwen bonus

Tech stack locked: Qwen-VL + Qwen2.5 + CrewAI + AMD MI300X + Streamlit + uv.
Submission checklist embedded. Governance rules defined.

## Outcome

- ✅ Impact: Project constitution established — all 6 principles locked, tech stack confirmed, prize targets mapped, submission checklist defined
- 🧪 Tests: none at this stage
- 📁 Files: .specify/memory/constitution.md (created v1.0.0)
- 🔁 Next prompts: /sp.specify — create feature spec for DocuMind AI core pipeline
- 🧠 Reflection: Constitution deliberately prioritizes speed and prize-target alignment over engineering elegance, appropriate for 6-day hackathon sprint

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): run /sp.specify immediately
