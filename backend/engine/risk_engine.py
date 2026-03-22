from __future__ import annotations


def generate_risk_flags(kpis: dict) -> list[str]:
    flags = []
    if kpis.get("current_ratio") is not None and kpis["current_ratio"] < 1:
        flags.append("Liquidity pressure: current ratio below 1.0")
    if kpis.get("debt_to_equity") is not None and kpis["debt_to_equity"] > 2:
        flags.append("High leverage: debt-to-equity above 2.0")
    if kpis.get("free_cf") is not None and kpis["free_cf"] < 0:
        flags.append("Negative free cash flow")
    if kpis.get("net_margin") is not None and kpis["net_margin"] < 0:
        flags.append("Net losses reported")
    if not flags:
        flags.append("No major quantitative red flags detected in current snapshot")
    return flags
