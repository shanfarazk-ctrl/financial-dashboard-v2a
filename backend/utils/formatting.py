from __future__ import annotations


def fmt_pct(value):
    if value is None:
        return "—"
    return f"{float(value) * 100:,.1f}%"


def fmt_money(value):
    if value is None:
        return "—"
    value = float(value)
    if abs(value) >= 1_000_000_000:
        return f"{value/1_000_000_000:,.2f}B"
    if abs(value) >= 1_000_000:
        return f"{value/1_000_000:,.2f}M"
    if abs(value) >= 1_000:
        return f"{value:,.0f}"
    return f"{value:,.2f}"


def fmt_num(value):
    if value is None:
        return "—"
    return f"{float(value):,.2f}"
