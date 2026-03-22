from __future__ import annotations


def score_company(kpis: dict, growth: dict, risks: list[str]) -> dict:
    score = 50
    if (growth.get("revenue_growth") or 0) > 0.08:
        score += 10
    if (kpis.get("operating_margin") or 0) > 0.15:
        score += 10
    if (kpis.get("roe") or 0) > 0.15:
        score += 10
    if (kpis.get("current_ratio") or 0) > 1.2:
        score += 5
    if len(risks) and "No major quantitative" not in risks[0]:
        score -= min(20, len(risks) * 5)
    score = max(0, min(100, score))
    if score >= 75:
        band = "Strong"
    elif score >= 55:
        band = "Balanced"
    else:
        band = "Weak"
    return {"score": score, "band": band}
