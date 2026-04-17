import json
import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()

_MOCK_MODE = os.getenv("MOCK_AGENT", "false").lower() == "true"
_ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")
_OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
_USE_MOCK = _MOCK_MODE or (not _ANTHROPIC_KEY and not _OPENAI_KEY)


def _mock_refine(company_name: str, industry: str, market: str, persona: str, card: dict) -> dict:
    """Return a lightly contextualized card without calling an LLM."""
    context_prefix = f"[{company_name} | {industry} | {market}]"

    def contextualize(items: list[str]) -> list[str]:
        return [f"{context_prefix} {item}" for item in items]

    return {
        "core_responsibilities": contextualize(card["core_responsibilities"]),
        "external_signals": contextualize(card["external_signals"]),
        "objections_concerns_risks": contextualize(card["objections_concerns_risks"]),
        "value_gaps": contextualize(card["value_gaps"]),
        "refinement_summary": (
            f"This persona card has been contextualized for the {persona} at {company_name}, "
            f"operating in the {industry} industry across the {market} market. "
            f"(Running in mock mode — set ANTHROPIC_API_KEY or OPENAI_API_KEY to enable LLM refinement.)"
        ),
    }


def _build_crew(company_name: str, industry: str, market: str, persona: str, card: dict) -> Any:
    from crewai import Agent, Crew, Process, Task

    llm_model = os.getenv("LLM_MODEL")
    llm = None

    if _ANTHROPIC_KEY:
        from crewai import LLM
        llm = LLM(model=llm_model or "claude-sonnet-4-6", api_key=_ANTHROPIC_KEY)
    elif _OPENAI_KEY:
        from crewai import LLM
        llm = LLM(model=llm_model or "gpt-4o", api_key=_OPENAI_KEY)

    agent_kwargs = {"llm": llm} if llm else {}

    researcher = Agent(
        role="Business Research Analyst",
        goal=(
            f"Research {company_name} in the {industry} industry within the {market} market. "
            "Identify the company's strategic priorities, recent initiatives, competitive landscape, "
            "regulatory environment, and key challenges relevant to the executive persona."
        ),
        backstory=(
            "You are a senior business analyst specialising in executive-level intelligence gathering. "
            "You distil publicly available information into concise, actionable insights for C-suite engagement."
        ),
        verbose=False,
        allow_delegation=False,
        **agent_kwargs,
    )

    writer = Agent(
        role="Persona Card Specialist",
        goal=(
            f"Refine the {persona} persona card to reflect the specific context of {company_name}, "
            f"operating in {industry} / {market}."
        ),
        backstory=(
            "You are an expert in building executive persona cards for enterprise sales and strategy teams. "
            "You translate business research into targeted, credible, and actionable persona narratives."
        ),
        verbose=False,
        allow_delegation=False,
        **agent_kwargs,
    )

    card_json = json.dumps(card, indent=2)

    research_task = Task(
        description=(
            f"Research {company_name}. Focus on:\n"
            f"- Strategic priorities and announced transformation programs\n"
            f"- Competitive pressures specific to {industry} in {market}\n"
            f"- Relevant regulatory or market dynamics\n"
            f"- Recent news, earnings calls, or executive statements\n"
            "Summarise your findings in 300 words or fewer."
        ),
        agent=researcher,
        expected_output="A concise business intelligence summary about the company.",
    )

    refine_task = Task(
        description=(
            f"Using the research findings above, refine the following {persona} persona card "
            f"for {company_name} ({industry}, {market}).\n\n"
            f"Original persona card:\n{card_json}\n\n"
            "Instructions:\n"
            "- Update each section to reflect company-specific context\n"
            "- Each list should contain 4–6 concise bullet points\n"
            "- Add a 'refinement_summary' field (2–3 sentences) explaining key changes made\n"
            "- Return ONLY valid JSON matching this schema:\n"
            "{\n"
            '  "core_responsibilities": [...],\n'
            '  "external_signals": [...],\n'
            '  "objections_concerns_risks": [...],\n'
            '  "value_gaps": [...],\n'
            '  "refinement_summary": "..."\n'
            "}"
        ),
        agent=writer,
        expected_output="A valid JSON object representing the refined persona card.",
    )

    return Crew(
        agents=[researcher, writer],
        tasks=[research_task, refine_task],
        process=Process.sequential,
        verbose=False,
    )


def _parse_crew_output(raw: str) -> dict:
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError("No JSON object found in crew output")
    return json.loads(raw[start:end])


async def refine_persona_card(
    company_name: str,
    industry: str,
    market: str,
    persona: str,
    card: dict,
) -> dict:
    if _USE_MOCK:
        return _mock_refine(company_name, industry, market, persona, card)

    import asyncio

    loop = asyncio.get_event_loop()
    crew = _build_crew(company_name, industry, market, persona, card)

    raw_result = await loop.run_in_executor(None, crew.kickoff)
    return _parse_crew_output(str(raw_result))
