from __future__ import annotations

from backend.utils.config import settings
from backend.utils.http import get_json

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


def get_series(series_id: str):
    params = {
        "series_id": series_id,
        "api_key": settings.fred_api_key,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 24,
    }
    return get_json(BASE_URL, params=params)


def get_macro_bundle():
    return {
        "gdp": get_series("GDP"),
        "cpi": get_series("CPIAUCSL"),
        "fed_funds": get_series("FEDFUNDS"),
        "unemployment": get_series("UNRATE"),
    }
