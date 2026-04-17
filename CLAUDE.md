# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server (http://localhost:8000)
py main.py

# Run all tests
pytest

# Run a single test file
pytest tests/test_api.py

# Run a single test
pytest tests/test_api.py::test_get_reference_data
```

## Architecture

FastAPI backend serving a Jinja2 HTML frontend. No client-side framework — vanilla JS only.

```
main.py                  # FastAPI app, mounts static files, serves index.html
app/
  routes.py              # All /api/* endpoints (reference-data, persona-card, refine)
  models.py              # Pydantic models: PersonaCard, RefineRequest, RefinedPersonaCard
  data/
    reference_data.py    # Static lists: INDUSTRIES, MARKETS, PERSONAS
    personas.py          # Predefined persona cards for CEO/CFO/CIO/COO/CMO
  agents/
    crew_agent.py        # CrewAI integration — Researcher + Writer agents
templates/
  index.html             # Single-page UI with form, original card, refined card sections
static/
  css/styles.css         # Accenture design system (CSS variables, components)
  js/app.js              # Form validation, API calls, DOM rendering, state management
```

## Key flows

**Persona card display**: selecting a persona in the UI triggers `GET /api/persona-card/{id}` which returns a `PersonaCard` from `app/data/personas.py`.

**Refinement**: form submit calls `POST /api/refine` → `app/agents/crew_agent.py::refine_persona_card()`. CrewAI runs two sequential agents (Researcher then Writer) and returns structured JSON matching `RefinedPersonaCard`.

**Mock mode**: set `MOCK_AGENT=true` in `.env` (or leave all LLM keys unset) to skip CrewAI calls and return a prefixed mock response — useful for local development.

## Environment variables

Copy `.env.example` to `.env` and set one of:
- `ANTHROPIC_API_KEY` — uses `claude-sonnet-4-6` by default
- `OPENAI_API_KEY` — uses `gpt-4o` by default
- `LLM_MODEL` — override the model name
- `SERPER_API_KEY` — enables web search in the Researcher agent
- `MOCK_AGENT=true` — bypasses all LLM calls
