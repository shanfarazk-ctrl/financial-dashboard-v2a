from __future__ import annotations

from backend.adapters import fmp_adapter, fred_adapter
from backend.ai.memo_generator import generate_memo
from backend.data.sample_data import get_sample_bundle
from backend.engine.kpi_engine import compute_growth, compute_kpis
from backend.engine.risk_engine import generate_risk_flags
from backend.engine.scoring_engine import score_company
from backend.engine.valuation_engine import compare_pe
from backend.utils.config import has_live_financial_keys, has_live_macro_keys, settings


class DashboardService:
    def load_bundle(self, symbol: str) -> dict:
        symbol = symbol.upper().strip()
        if settings.use_sample_data or not has_live_financial_keys():
            return get_sample_bundle(symbol)

        try:
            profile = fmp_adapter.get_profile(symbol)
            quote = fmp_adapter.get_quote(symbol)
            income = fmp_adapter.get_income_statement(symbol, limit=5)
            balance = fmp_adapter.get_balance_sheet(symbol, limit=5)
            cashflow = fmp_adapter.get_cash_flow(symbol, limit=5)
            metrics = fmp_adapter.get_key_metrics(symbol, limit=5)
            macro = fred_adapter.get_macro_bundle() if has_live_macro_keys() else get_sample_bundle(symbol)["macro"]
            peers = get_sample_bundle(symbol)["peers"]
            return {
                "profile": profile,
                "quote": quote,
                "income": income,
                "balance": balance,
                "cashflow": cashflow,
                "metrics": metrics,
                "peers": peers,
                "macro": macro,
                "source_mode": "live",
            }
        except Exception:
            return get_sample_bundle(symbol)

    def analyze(self, symbol: str) -> dict:
        bundle = self.load_bundle(symbol)
        profile = (bundle.get("profile") or [{}])[0]
        quote = (bundle.get("quote") or [{}])[0]
        income = bundle.get("income") or []
        balance = bundle.get("balance") or []
        cashflow = bundle.get("cashflow") or []
        metrics = bundle.get("metrics") or []
        peers = bundle.get("peers") or []
        macro = bundle.get("macro") or {}

        latest_is = income[0] if income else {}
        prior_is = income[1] if len(income) > 1 else {}
        latest_bs = balance[0] if balance else {}
        latest_cf = cashflow[0] if cashflow else {}
        latest_metrics = metrics[0] if metrics else {}

        kpis = compute_kpis(latest_is, latest_bs, latest_cf, latest_metrics)
        growth = compute_growth(latest_is, prior_is)
        risks = generate_risk_flags({**kpis, **growth})
        valuation = compare_pe(kpis.get("pe_ratio"), peers)
        scoring = score_company(kpis, growth, risks)

        summary = (
            f"Company: {profile.get('companyName') or profile.get('name') or symbol}\n"
            f"Sector: {profile.get('sector')}\n"
            f"Industry: {profile.get('industry')}\n"
            f"Price: {quote.get('price')}\n"
            f"Revenue: {kpis.get('revenue')}\n"
            f"Revenue Growth: {growth.get('revenue_growth')}\n"
            f"Operating Margin: {kpis.get('operating_margin')}\n"
            f"Net Margin: {kpis.get('net_margin')}\n"
            f"ROE: {kpis.get('roe')}\n"
            f"Current Ratio: {kpis.get('current_ratio')}\n"
            f"Debt/Equity: {kpis.get('debt_to_equity')}\n"
            f"Free Cash Flow: {kpis.get('free_cf')}\n"
            f"Valuation: {valuation}\n"
            f"Risk Flags: {risks}\n"
            f"Macro snapshot keys: {list(macro.keys())}\n"
        )
        memo = generate_memo(summary)
        return {
            "source_mode": bundle.get("source_mode", "sample"),
            "profile": profile,
            "quote": quote,
            "income": income,
            "balance": balance,
            "cashflow": cashflow,
            "metrics": metrics,
            "macro": macro,
            "peers": peers,
            "kpis": kpis,
            "growth": growth,
            "risks": risks,
            "valuation": valuation,
            "scoring": scoring,
            "memo": memo,
        }
