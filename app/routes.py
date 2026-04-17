from fastapi import APIRouter, HTTPException

from app.agents.crew_agent import refine_persona_card
from app.data.personas import get_persona_card
from app.data.reference_data import INDUSTRIES, MARKETS, PERSONAS
from app.models import RefineRequest

router = APIRouter(prefix="/api")


@router.get("/reference-data")
async def get_reference_data():
    return {"industries": INDUSTRIES, "markets": MARKETS, "personas": PERSONAS}


@router.get("/persona-card/{persona_id}")
async def get_persona(persona_id: str):
    card = get_persona_card(persona_id)
    if not card:
        raise HTTPException(status_code=404, detail=f"Persona '{persona_id}' not found.")
    return card


@router.post("/refine")
async def refine(request: RefineRequest):
    try:
        refined = await refine_persona_card(
            company_name=request.company_name,
            industry=request.industry,
            market=request.market,
            persona=request.persona,
            card=request.persona_card.model_dump(),
        )
        return refined
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Agent refinement failed: {str(exc)}",
        ) from exc
