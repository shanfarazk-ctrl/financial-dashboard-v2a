from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from backend.services.dashboard_service import DashboardService
from backend.ui.components import hero_card, memo_box, metric_card, risk_box
from backend.ui.theme import apply_theme
from backend.utils.config import settings
from backend.utils.formatting import fmt_money, fmt_num, fmt_pct


PLOTLY_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(15,23,42,0.0)",
    "font": {"color": "#e5eefc", "family": "Arial"},
    "margin": {"l": 20, "r": 20, "t": 55, "b": 20},
    "legend": {"orientation": "h", "yanchor": "bottom", "y": 1.02, "x": 0},
    "xaxis": {"showgrid": False, "zeroline": False},
    "yaxis": {"gridcolor": "rgba(148,163,184,0.12)", "zeroline": False},
}


def _safe_delta(current, prior, pct: bool = False) -> str:
    if current is None or prior is None:
        return "No prior period"
    try:
        delta = float(current) - float(prior)
        if pct:
            return fmt_pct(delta)
        return fmt_money(delta)
    except Exception:
        return "No prior period"


def _hero(result: dict) -> None:
    profile = result["profile"]
    quote = result["quote"]
    score = result["scoring"]
    subtitle = (
        f"{profile.get('sector', 'N/A')} • {profile.get('industry', 'N/A')} • "
        f"{profile.get('country', 'N/A')} • {result['source_mode'].upper()} mode"
    )
    pills = [
        f"Exchange: {profile.get('exchangeShortName', 'N/A')}",
        f"Currency: {profile.get('currency', 'N/A')}",
        f"Score: {score.get('score')} / 100",
        f"Band: {score.get('band')}",
        f"Price: {fmt_num(quote.get('price'))}",
    ]
    hero_card(profile.get("companyName") or quote.get("name") or "Company", subtitle, pills)


def _metric_strip(result: dict) -> None:
    kpis = result["kpis"]
    growth = result["growth"]
    valuation = result["valuation"]
    score = result["scoring"]
    income = result["income"]
    prior_revenue = income[1].get("revenue") if len(income) > 1 else None

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        metric_card("Share Price", fmt_num(result["quote"].get("price")), "Latest market snapshot")
    with c2:
        metric_card("Revenue", fmt_money(kpis.get("revenue")), _safe_delta(kpis.get("revenue"), prior_revenue))
    with c3:
        metric_card("Revenue Growth", fmt_pct(growth.get("revenue_growth")), "Year over year")
    with c4:
        metric_card(
            "P/E vs Peers",
            fmt_num(valuation.get("company_pe")),
            f"Position: {valuation.get('pe_position') or 'N/A'}",
        )
    with c5:
        metric_card("Composite Score", str(score.get("score")), score.get("band", ""))


def _financial_chart(result: dict, key_prefix: str) -> None:
    income = pd.DataFrame(result["income"])
    if income.empty or not {"calendarYear", "revenue", "netIncome"}.issubset(income.columns):
        return

    income = income.sort_values("calendarYear")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=income["calendarYear"],
            y=income["revenue"],
            mode="lines+markers",
            name="Revenue",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=income["calendarYear"],
            y=income["netIncome"],
            mode="lines+markers",
            name="Net Income",
        )
    )
    fig.update_layout(title="Financial Trend", **PLOTLY_LAYOUT)
    st.plotly_chart(fig, width="stretch", key=f"{key_prefix}_financial_chart")


def _margin_chart(result: dict, key_prefix: str) -> None:
    income = pd.DataFrame(result["income"])
    if income.empty:
        return

    df = income.sort_values("calendarYear").copy()
    needed = {"revenue", "grossProfit", "operatingIncome", "netIncome"}
    if not needed.issubset(df.columns):
        return

    df["Gross Margin"] = df["grossProfit"] / df["revenue"]
    df["Operating Margin"] = df["operatingIncome"] / df["revenue"]
    df["Net Margin"] = df["netIncome"] / df["revenue"]

    fig = px.line(
        df,
        x="calendarYear",
        y=["Gross Margin", "Operating Margin", "Net Margin"],
        markers=True,
        title="Margin Quality",
    )
    fig.update_layout(**PLOTLY_LAYOUT)
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, width="stretch", key=f"{key_prefix}_margin_chart")


def _peer_chart(result: dict, key_prefix: str) -> None:
    peers = pd.DataFrame(result["peers"])
    if peers.empty or not {"symbol", "pe", "revenueGrowth"}.issubset(peers.columns):
        return

    fig = px.scatter(
        peers,
        x="pe",
        y="revenueGrowth",
        text="symbol",
        size_max=16,
        title="Peer Positioning: P/E vs Growth",
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(**PLOTLY_LAYOUT)
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, width="stretch", key=f"{key_prefix}_peer_chart")


def _overview(result: dict, key_prefix: str) -> None:
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown("### Overview")
        _financial_chart(result, key_prefix=key_prefix)
    with right:
        st.markdown("### Margins & Quality")
        _margin_chart(result, key_prefix=key_prefix)


def _financial_tables(result: dict) -> None:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### KPI Snapshot")
        kpi_rows = [
            ("Revenue", fmt_money(result["kpis"].get("revenue"))),
            ("Gross Margin", fmt_pct(result["kpis"].get("gross_margin"))),
            ("Operating Margin", fmt_pct(result["kpis"].get("operating_margin"))),
            ("Net Margin", fmt_pct(result["kpis"].get("net_margin"))),
            ("ROA", fmt_pct(result["kpis"].get("roa"))),
            ("ROE", fmt_pct(result["kpis"].get("roe"))),
            ("Current Ratio", fmt_num(result["kpis"].get("current_ratio"))),
            ("Debt / Equity", fmt_num(result["kpis"].get("debt_to_equity"))),
            ("Free Cash Flow", fmt_money(result["kpis"].get("free_cf"))),
        ]
        st.dataframe(pd.DataFrame(kpi_rows, columns=["Metric", "Value"]), width="stretch", hide_index=True)

    with c2:
        st.markdown("### Growth Snapshot")
        growth_rows = [
            ("Revenue Growth", fmt_pct(result["growth"].get("revenue_growth"))),
            ("Net Income Growth", fmt_pct(result["growth"].get("net_income_growth"))),
            ("Operating Cash Flow", fmt_money(result["kpis"].get("operating_cf"))),
            ("Cash / Debt", fmt_num(result["kpis"].get("cash_to_debt"))),
            ("P/B", fmt_num(result["kpis"].get("pb_ratio"))),
            ("EV / EBITDA", fmt_num(result["kpis"].get("ev_ebitda"))),
        ]
        st.dataframe(pd.DataFrame(growth_rows, columns=["Metric", "Value"]), width="stretch", hide_index=True)


def _valuation_risk(result: dict, key_prefix: str) -> None:
    c1, c2 = st.columns([1.05, 0.95])

    with c1:
        st.markdown("### Relative Valuation")
        valuation = result["valuation"]
        summary = pd.DataFrame(
            [
                ["Company P/E", fmt_num(valuation.get("company_pe"))],
                ["Peer Median P/E", fmt_num(valuation.get("peer_median_pe"))],
                ["Relative Position", valuation.get("pe_position") or "N/A"],
            ],
            columns=["Item", "Value"],
        )
        st.dataframe(summary, width="stretch", hide_index=True)
        _peer_chart(result, key_prefix=key_prefix)

        if result["peers"]:
            st.markdown("### Peer Table")
            peers = pd.DataFrame(result["peers"])
            if "revenueGrowth" in peers.columns:
                peers["revenueGrowth"] = peers["revenueGrowth"].map(fmt_pct)
            st.dataframe(peers, width="stretch", hide_index=True)

    with c2:
        st.markdown("### Risk Monitor")
        risk_messages = result["risks"] or ["No risks returned"]
        for msg in risk_messages:
            if "No major quantitative" in msg:
                risk_box(msg, "good")
            elif any(word in msg.lower() for word in ["negative", "high", "loss"]):
                risk_box(msg, "bad")
            else:
                risk_box(msg, "warn")

        st.markdown("### Quality Score")
        score = result["scoring"].get("score", 0)
        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                number={"suffix": "/100", "font": {"color": "#e5eefc"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#94a3b8"},
                    "bar": {"color": "#38bdf8"},
                    "steps": [
                        {"range": [0, 55], "color": "rgba(239,68,68,0.28)"},
                        {"range": [55, 75], "color": "rgba(245,158,11,0.25)"},
                        {"range": [75, 100], "color": "rgba(34,197,94,0.22)"},
                    ],
                    "threshold": {"line": {"color": "#e5eefc", "width": 3}, "value": score},
                },
                title={"text": result["scoring"].get("band", "Score")},
            )
        )
        gauge.update_layout(**PLOTLY_LAYOUT, height=340)
        st.plotly_chart(gauge, width="stretch", key=f"{key_prefix}_quality_gauge")


def _macro_tab(result: dict) -> None:
    st.markdown("### Macro Snapshot")
    macro = result.get("macro", {})
    cards = []
    for key, payload in macro.items():
        obs = (payload or {}).get("observations", [])
        latest = obs[-1] if obs else {}
        cards.append((key.upper(), latest.get("value", "N/A"), latest.get("date", "N/A")))

    cols = st.columns(max(1, min(4, len(cards)))) if cards else [st]
    for idx, (name, value, date) in enumerate(cards):
        with cols[idx % len(cols)]:
            metric_card(name, value, f"As of {date}")

    if cards:
        st.dataframe(pd.DataFrame(cards, columns=["Series", "Latest", "Date"]), width="stretch", hide_index=True)


def _memo_tab(result: dict) -> None:
    st.markdown("### AI Investment Memo")
    memo_text = (result.get("memo") or "").replace("\n", "<br>")
    memo_box(memo_text)
    st.caption("Premium UI pack V3 foundation: structured presentation layer ready for peer AI, scenario AI, and PDF export.")


def run_app() -> None:
    st.set_page_config(page_title=settings.app_name, layout="wide", page_icon="📈")
    apply_theme()
    service = DashboardService()

    with st.sidebar:
        st.markdown("## Global Equity Intelligence")
        ticker = st.text_input("Ticker / Symbol", value=settings.default_ticker).upper().strip()
        market_scope = st.multiselect(
            "Priority Exchanges",
            ["NASDAQ", "NYSE", "LSE", "Tadawul", "PSX"],
            default=["NASDAQ", "NYSE", "Tadawul"],
            help="UI placeholder for V3 global resolver. Data engine can be extended in the next sprint.",
        )
        st.toggle("Premium visual mode", value=True, disabled=True)
        st.toggle("Peer AI commentary", value=False, disabled=True)
        st.toggle("Scenario engine", value=False, disabled=True)
        st.caption("This pack upgrades presentation, layout, and premium information hierarchy before adding resolver + peer engines.")
        run = st.button("Run Analysis", type="primary", width="stretch")

    if run or ticker:
        with st.spinner("Building premium view..."):
            result = service.analyze(ticker)

        _hero(result)
        _metric_strip(result)

        top_left, top_right = st.columns([1.05, 0.95])
        with top_left:
            _overview(result, key_prefix="top_overview")
        with top_right:
            st.markdown("### Company Profile")
            profile = result["profile"]
            quote = result["quote"]
            profile_rows = [
                ["Company", profile.get("companyName") or quote.get("name")],
                ["Exchange", profile.get("exchangeShortName")],
                ["Country", profile.get("country")],
                ["Currency", profile.get("currency")],
                ["Sector", profile.get("sector")],
                ["Industry", profile.get("industry")],
                ["Website", profile.get("website")],
                ["Exchange Universe", ", ".join(market_scope)],
            ]
            st.dataframe(pd.DataFrame(profile_rows, columns=["Field", "Value"]), width="stretch", hide_index=True)

        tab_overview, tab_financials, tab_valuation, tab_macro, tab_memo = st.tabs(
            ["Overview", "Financials", "Valuation & Risk", "Macro", "AI Insights"]
        )
        with tab_overview:
            _overview(result, key_prefix="tab_overview")
        with tab_financials:
            _financial_tables(result)
        with tab_valuation:
            _valuation_risk(result, key_prefix="tab_valuation")
        with tab_macro:
            _macro_tab(result)
        with tab_memo:
            _memo_tab(result)