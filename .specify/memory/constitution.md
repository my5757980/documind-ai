<!--
SYNC IMPACT REPORT
==================
Version change: [TEMPLATE] → 1.0.0 (new project — first ratification)
Modified principles: none (new)
Added sections: Core Principles (6), Tech Stack & Hackathon Requirements, Submission Checklist, Governance
Removed sections: none
Templates updated:
  ✅ .specify/templates/plan-template.md — Constitution Check gates align with 6 principles
  ✅ .specify/templates/spec-template.md — functional requirements align with AMD-first + agent pipeline
  ✅ .specify/templates/tasks-template.md — task phases align with 6-day sprint constraint
Deferred TODOs: none
-->

# DocuMind AI Constitution

## Core Principles

### I. AMD-First Computing

All inference, fine-tuning, and heavy compute MUST run on AMD Developer Cloud
(AMD Instinct MI300X GPUs) via ROCm. No NVIDIA CUDA fallback is permitted in
the production path. Local CPU-only execution is allowed solely for unit tests
and CI checks that do not require GPU.

**Rationale**: The hackathon judging criterion "Application of Technology"
rewards deep AMD integration. Every compute call must be traceable to AMD
infrastructure to maximize score on this criterion.

### II. 4-Agent Pipeline (NON-NEGOTIABLE)

The system MUST implement exactly four specialized AI agents orchestrated via
CrewAI:

- **Vision Agent** — processes images, charts, and visual content using Qwen-VL
  running on AMD MI300X
- **Reader Agent** — extracts and understands text from PDFs and documents using
  Qwen2.5 running on AMD MI300X
- **Analyst Agent** — synthesizes findings from Vision + Reader agents and
  generates structured insights
- **Reporter Agent** — produces the final structured output report for the user

Agents MUST be independently testable. No agent may directly call another
agent's internal methods — all communication goes through CrewAI task
delegation.

**Rationale**: Multi-agent architecture is the core of Track 1 (AI Agents &
Agentic Workflows). The 4-agent design demonstrates sophistication beyond
simple RAG pipelines, which is explicitly rewarded by the hackathon spec.

### III. End-to-End Working Demo (NON-NEGOTIABLE)

Every milestone MUST leave the system in a runnable, demonstrable state. A
feature that works in isolation but breaks the demo pipeline MUST NOT be merged.
The live demo MUST:

1. Accept a real document or image as input
2. Run all 4 agents visibly (progress shown in UI)
3. Produce a structured output report
4. Complete within 60 seconds on AMD Developer Cloud

**Rationale**: Judges evaluate live demos. A broken or staged demo eliminates
prize eligibility regardless of code quality.

### IV. Open Source & Deploy-First

The project MUST be:
- Licensed under MIT (LICENSE file at root, no exceptions)
- Published to a public GitHub repository before submission deadline
- Deployed as a Hugging Face Space within the AMD Developer Hackathon HF
  organization
- The HF Space MUST be live and accessible for judges at submission time

All AMD Developer Cloud credentials MUST live in `.env` (gitignored). Never
hardcode API keys, tokens, or secrets in source code.

**Rationale**: Open source + HF Space deployment unlocks three additional
prize pools: HF Special Prize (likes), Build in Public prize (AMD GPU), and
demonstrates the project's real-world usability to judges.

### V. Speed Over Perfection (6-Day Sprint)

Deadline is **May 11 2026 00:00 AM Pakistan Standard Time**. Given this
constraint:

- YAGNI strictly enforced — build only what judges will see and evaluate
- No refactoring passes unless a bug blocks the demo
- Streamlit UI is the mandatory frontend (no Next.js, no React for this sprint)
- FastAPI backend is optional if Streamlit can call AMD Cloud APIs directly
- Every day MUST end with a committable, runnable state

**Rationale**: A working 80% solution submitted beats a perfect 100% solution
missed. Six days solo from Pakistan — ruthless scope discipline is survival.

### VI. Multi-Prize Targeting Strategy

The implementation MUST simultaneously satisfy requirements for all target
prizes without feature bloat:

| Prize Target | Implementation Requirement |
|---|---|
| Grand Prize ($5,000) | Overall strongest project — AMD integration depth |
| Track 1 — AI Agents | 4-agent CrewAI pipeline (Principle II) |
| Track 3 — Vision/Multimodal | Qwen-VL vision processing (Principle II) |
| HF Special Prize | HF Space deployed + community likes campaign |
| Build in Public (AMD GPU) | 2 social posts + open source (Principle IV) |
| Qwen Bonus | Qwen-VL + Qwen2.5 used as primary models |

Any feature that does not serve at least one prize target MUST be cut.

## Tech Stack & Hackathon Requirements

### Locked Tech Stack

```
Models:     Qwen-VL (vision)  +  Qwen2.5-72B (text)
Agents:     CrewAI
Compute:    AMD Instinct MI300X via AMD Developer Cloud (ROCm)
UI:         Streamlit
Deploy:     Hugging Face Space (primary) + local Docker (optional)
Repo:       GitHub (public, MIT)
Language:   Python 3.11+
Deps:       uv (NEVER pip)
```

### AMD Developer Cloud Access

- **Credits**: $100 in AMD Developer Cloud credits (already activated)
- **GPU**: AMD Instinct MI300X
- **Platform**: AMD AI Developer Program membership required (already registered)
- All GPU calls MUST use ROCm-compatible libraries (torch with ROCm backend)

### Social Media Requirements (Build in Public)

Share at minimum 2 technical posts before May 11 2026:
- Tag **@lablab** on X and **lablab.ai** on LinkedIn
- Tag **@AIatAMD** on X and **AMD Developer** on LinkedIn
- Content MUST be technical (architecture, progress, insights) — not just
  promotional

## Submission Checklist

These items MUST be complete before May 11 2026 00:00 AM PST:

- [ ] Project Title: "DocuMind AI — Multi-Modal Document Intelligence"
- [ ] Short Description (≤ 280 chars)
- [ ] Long Description (detailed, includes AMD tech depth)
- [ ] Cover Image (1280×640 px minimum)
- [ ] Video Presentation (3-5 min demo video)
- [ ] Slide Presentation (PDF, ≤ 15 slides)
- [ ] Public GitHub Repository (MIT licensed, README with setup instructions)
- [ ] Live Demo URL (HF Space)
- [ ] Hugging Face Space published in AMD Developer Hackathon HF Organization
- [ ] 2 social media posts published (tags verified)
- [ ] Technology tags: AMD, ROCm, CrewAI, Qwen, Multi-Agent, Vision AI

## Governance

This constitution supersedes all other development guidelines for DocuMind AI.
Amendments require:

1. Written justification citing which prize target or deadline constraint forces
   the change
2. Update to this file with version bump
3. No amendment may reduce scope in a way that eliminates a prize target without
   explicit acknowledgment

**Versioning policy**: MAJOR for principle removal/redefinition,
MINOR for new principle or section, PATCH for clarifications.

**Compliance**: Every task in `tasks.md` MUST map to at least one principle.
Tasks that cannot be justified against a principle are out of scope.

**Version**: 1.0.0 | **Ratified**: 2026-05-04 | **Last Amended**: 2026-05-04
