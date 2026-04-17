import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_reference_data():
    r = client.get("/api/reference-data")
    assert r.status_code == 200
    data = r.json()
    assert "industries" in data
    assert "markets" in data
    assert "personas" in data
    assert len(data["industries"]) > 0


def test_get_persona_card_valid():
    for persona_id in ["CEO", "CFO", "CIO", "COO", "CMO"]:
        r = client.get(f"/api/persona-card/{persona_id}")
        assert r.status_code == 200
        card = r.json()
        assert "core_responsibilities" in card
        assert "external_signals" in card
        assert "objections_concerns_risks" in card
        assert "value_gaps" in card


def test_get_persona_card_invalid():
    r = client.get("/api/persona-card/UNKNOWN")
    assert r.status_code == 404


def test_refine_endpoint_mock(monkeypatch):
    monkeypatch.setenv("MOCK_AGENT", "true")
    import importlib
    import app.agents.crew_agent as agent_module
    importlib.reload(agent_module)

    payload = {
        "company_name": "Acme Corp",
        "industry": "Technology",
        "market": "North America",
        "persona": "CEO",
        "persona_card": {
            "core_responsibilities": ["Lead strategy"],
            "external_signals": ["Market disruption"],
            "objections_concerns_risks": ["ROI uncertainty"],
            "value_gaps": ["No benchmarks"],
        },
    }
    r = client.post("/api/refine", json=payload)
    assert r.status_code == 200
    result = r.json()
    assert "core_responsibilities" in result
    assert "refinement_summary" in result


def test_refine_endpoint_validation():
    r = client.post("/api/refine", json={"company_name": "", "industry": "Tech"})
    assert r.status_code == 422
