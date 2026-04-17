from pydantic import BaseModel, Field
from typing import List, Optional


class PersonaCard(BaseModel):
    core_responsibilities: List[str]
    external_signals: List[str]
    objections_concerns_risks: List[str]
    value_gaps: List[str]


class RefineRequest(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=200)
    industry: str
    market: str
    persona: str
    persona_card: PersonaCard


class RefinedPersonaCard(PersonaCard):
    refinement_summary: Optional[str] = None
