from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from backend.utils.config import settings


class ApiError(RuntimeError):
    pass


def get_json(url: str, params: Optional[Dict[str, Any]] = None) -> Any:
    response = requests.get(url, params=params, timeout=settings.request_timeout_seconds)
    if response.status_code >= 400:
        raise ApiError(f"HTTP {response.status_code}: {response.text[:300]}")
    return response.json()
