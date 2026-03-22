from __future__ import annotations

from backend.utils.config import settings
from backend.utils.http import get_json

BASE_URL = "https://financialmodelingprep.com/api/v3"


def _with_key(path: str) -> str:
    sep = "&" if "?" in path else "?"
    return f"{BASE_URL}{path}{sep}apikey={settings.fmp_api_key}"


def get_profile(symbol: str):
    return get_json(_with_key(f"/profile/{symbol}"))


def get_quote(symbol: str):
    return get_json(_with_key(f"/quote/{symbol}"))


def get_income_statement(symbol: str, limit: int = 5):
    return get_json(_with_key(f"/income-statement/{symbol}?limit={limit}"))


def get_balance_sheet(symbol: str, limit: int = 5):
    return get_json(_with_key(f"/balance-sheet-statement/{symbol}?limit={limit}"))


def get_cash_flow(symbol: str, limit: int = 5):
    return get_json(_with_key(f"/cash-flow-statement/{symbol}?limit={limit}"))


def get_key_metrics(symbol: str, limit: int = 5):
    return get_json(_with_key(f"/key-metrics/{symbol}?limit={limit}"))


def get_peers(symbol: str):
    # Some FMP plans support peers endpoints differently. This is a safe starter fallback.
    industry_peers = get_profile(symbol)
    if not industry_peers:
        return []
    return []
