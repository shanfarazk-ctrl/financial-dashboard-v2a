from __future__ import annotations

from backend.utils.config import settings
from backend.utils.http import get_json

BASE_URL = "https://www.alphavantage.co/query"


def get_daily_adjusted(symbol: str):
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "apikey": settings.alpha_vantage_api_key,
        "outputsize": "compact",
    }
    return get_json(BASE_URL, params=params)
