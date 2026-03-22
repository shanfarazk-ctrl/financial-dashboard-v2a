from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

try:
    import streamlit as st
except Exception:  # pragma: no cover
    st = None
from dotenv import load_dotenv

load_dotenv()


def _coalesce(name: str, default: str = "") -> str:
    try:
        if st is not None and hasattr(st, "secrets") and name in st.secrets:
            value = st.secrets[name]
            return str(value)
    except Exception:
        pass
    return os.getenv(name, default)


def _as_bool(value: str | bool | None, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = _coalesce("APP_NAME", "Institutional Financial Dashboard V2A")
    app_env: str = _coalesce("APP_ENV", "local")
    default_ticker: str = _coalesce("DEFAULT_TICKER", "AAPL")
    use_sample_data: bool = _as_bool(_coalesce("USE_SAMPLE_DATA", "true"), True)
    enable_ai_memo: bool = _as_bool(_coalesce("ENABLE_AI_MEMO", "false"), False)
    request_timeout_seconds: int = int(_coalesce("REQUEST_TIMEOUT_SECONDS", "30"))
    cache_ttl_seconds: int = int(_coalesce("CACHE_TTL_SECONDS", "1800"))
    fmp_api_key: str = _coalesce("FMP_API_KEY", "")
    fred_api_key: str = _coalesce("FRED_API_KEY", "")
    alpha_vantage_api_key: str = _coalesce("ALPHA_VANTAGE_API_KEY", "")
    anthropic_api_key: str = _coalesce("ANTHROPIC_API_KEY", "")


settings = Settings()


def has_live_financial_keys() -> bool:
    return bool(settings.fmp_api_key)


def has_live_macro_keys() -> bool:
    return bool(settings.fred_api_key)


def has_ai_keys() -> bool:
    return bool(settings.anthropic_api_key)
