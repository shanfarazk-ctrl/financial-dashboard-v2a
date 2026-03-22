from backend.engine.risk_engine import generate_risk_flags
from backend.engine.scoring_engine import score_company


def test_risks_and_score():
    risks = generate_risk_flags({"current_ratio": 0.8, "debt_to_equity": 2.5, "free_cf": -5, "net_margin": -0.02})
    score = score_company(
        {"operating_margin": 0.12, "roe": 0.14, "current_ratio": 0.8},
        {"revenue_growth": 0.05},
        risks,
    )
    assert len(risks) >= 3
    assert score["score"] <= 50
