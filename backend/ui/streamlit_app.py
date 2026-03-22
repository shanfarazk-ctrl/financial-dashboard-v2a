from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from backend.services.dashboard_service import DashboardService
from backend.utils.config import settings
from backend.utils.formatting import fmt_money, fmt_num, fmt_pct


def _render_header(result: dict):
    profile = result["profile"]
    quote = result["quote"]
    st.title(settings.app_name)
    st.caption(f"Mode: {result['source_mode'].upper()} | Exchange: {profile.get('exchangeShortName', 'N/A')} | Currency: {profile.get('currency', 'N/A')}")
    st.subheader(profile.get("companyName") or quote.get("name") or "Company")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Share Price", fmt_num(quote.get("price")))
    c2.metric("Market Cap", fmt_money(quote.get("marketCap")))
    c3.metric("Revenue", fmt_money(result["kpis"].get("revenue")))
    c4.metric("Score", f"{result['scoring']['score']} ({result['scoring']['band']})")


def _render_charts(result: dict):
    income = pd.DataFrame(result["income"])
    if not income.empty and {"calendarYear", "revenue", "netIncome"}.issubset(income.columns):
        fig = px.line(income.sort_values("calendarYear"), x="calendarYear", y=["revenue", "netIncome"], markers=True, title="Revenue and Net Income Trend")
        st.plotly_chart(fig, width="stretch")

    peers = pd.DataFrame(result["peers"])
    if not peers.empty and {"symbol", "pe", "revenueGrowth"}.issubset(peers.columns):
        fig = px.scatter(peers, x="pe", y="revenueGrowth", text="symbol", title="Peer P/E vs Revenue Growth")
        fig.update_traces(textposition="top center")
        st.plotly_chart(fig, width="stretch")


def _render_tabs(result: dict):
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["KPIs", "Valuation", "Risk", "Macro", "AI Memo"])

    with tab1:
        view = {**result["kpis"], **result["growth"], **result["scoring"]}
        st.dataframe(pd.DataFrame([{"metric": k, "value": v} for k, v in view.items()]), width="stretch")

    with tab2:
        st.json(result["valuation"])
        if result["peers"]:
            st.dataframe(pd.DataFrame(result["peers"]), width="stretch")

    with tab3:
        for flag in result["risks"]:
            if "No major quantitative" in flag:
                st.success(flag)
            else:
                st.warning(flag)

    with tab4:
        st.json(result["macro"])

    with tab5:
        st.text(result["memo"])


def run_app():
    st.set_page_config(page_title=settings.app_name, layout="wide")
    service = DashboardService()
    with st.sidebar:
        st.header("Controls")
        ticker = st.text_input("Ticker", value=settings.default_ticker).upper().strip()
        st.caption("Set USE_SAMPLE_DATA=false for live mode after secrets are configured.")
        run = st.button("Run Analysis", type="primary")

    if run or ticker:
        with st.spinner("Loading company data..."):
            result = service.analyze(ticker)
        _render_header(result)
        _render_charts(result)
        _render_tabs(result)
