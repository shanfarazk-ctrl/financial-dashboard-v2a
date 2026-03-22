from __future__ import annotations

from statistics import median


def compare_pe(company_pe: float | None, peers: list[dict]) -> dict:
    peer_pes = [p.get("pe") for p in peers if p.get("pe") is not None]
    if company_pe is None or not peer_pes:
        return {"company_pe": company_pe, "peer_median_pe": None, "pe_position": None}
    peer_median = median(peer_pes)
    if company_pe < peer_median:
        position = "discount"
    elif company_pe > peer_median:
        position = "premium"
    else:
        position = "in-line"
    return {"company_pe": company_pe, "peer_median_pe": peer_median, "pe_position": position}
