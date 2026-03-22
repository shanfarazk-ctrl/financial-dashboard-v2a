from __future__ import annotations


def compute_kpis(latest_is: dict, latest_bs: dict, latest_cf: dict, latest_metrics: dict) -> dict:
    revenue = latest_is.get("revenue") or 0
    gross_profit = latest_is.get("grossProfit") or 0
    operating_income = latest_is.get("operatingIncome") or latest_is.get("ebit") or 0
    net_income = latest_is.get("netIncome") or 0

    total_assets = latest_bs.get("totalAssets") or 0
    total_debt = latest_bs.get("totalDebt") or 0
    cash = latest_bs.get("cashAndCashEquivalents") or 0
    equity = latest_bs.get("totalStockholdersEquity") or latest_bs.get("equity") or 0
    current_assets = latest_bs.get("totalCurrentAssets") or 0
    current_liabilities = latest_bs.get("totalCurrentLiabilities") or 0

    operating_cf = latest_cf.get("operatingCashFlow") or latest_cf.get("cashFromOperations") or 0
    free_cf = latest_cf.get("freeCashFlow") or 0

    return {
        "revenue": revenue,
        "gross_margin": (gross_profit / revenue) if revenue else None,
        "operating_margin": (operating_income / revenue) if revenue else None,
        "net_margin": (net_income / revenue) if revenue else None,
        "roa": (net_income / total_assets) if total_assets else None,
        "roe": (net_income / equity) if equity else None,
        "debt_to_equity": (total_debt / equity) if equity else None,
        "current_ratio": (current_assets / current_liabilities) if current_liabilities else None,
        "operating_cf": operating_cf,
        "free_cf": free_cf,
        "cash_to_debt": (cash / total_debt) if total_debt else None,
        "pe_ratio": latest_metrics.get("peRatio"),
        "pb_ratio": latest_metrics.get("pbRatio"),
        "ev_ebitda": latest_metrics.get("evToEbitda"),
    }


def compute_growth(current: dict, prior: dict) -> dict:
    current_rev = current.get("revenue") or 0
    prior_rev = prior.get("revenue") or 0
    current_ni = current.get("netIncome") or 0
    prior_ni = prior.get("netIncome") or 0
    return {
        "revenue_growth": ((current_rev - prior_rev) / prior_rev) if prior_rev else None,
        "net_income_growth": ((current_ni - prior_ni) / prior_ni) if prior_ni else None,
    }
