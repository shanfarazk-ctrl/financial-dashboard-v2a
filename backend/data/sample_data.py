from __future__ import annotations


def get_sample_bundle(ticker: str = "AAPL") -> dict:
    ticker = ticker.upper().strip() or "AAPL"
    income = [
        {"calendarYear": "2024", "revenue": 1260.0, "grossProfit": 540.0, "operatingIncome": 233.0, "netIncome": 172.0},
        {"calendarYear": "2023", "revenue": 1125.0, "grossProfit": 487.0, "operatingIncome": 205.0, "netIncome": 150.0},
        {"calendarYear": "2022", "revenue": 1000.0, "grossProfit": 430.0, "operatingIncome": 180.0, "netIncome": 130.0},
    ]
    balance = [
        {"calendarYear": "2024", "totalAssets": 1610.0, "totalDebt": 355.0, "cashAndCashEquivalents": 210.0, "totalStockholdersEquity": 760.0, "totalCurrentAssets": 480.0, "totalCurrentLiabilities": 290.0},
        {"calendarYear": "2023", "totalAssets": 1490.0, "totalDebt": 340.0, "cashAndCashEquivalents": 194.0, "totalStockholdersEquity": 680.0, "totalCurrentAssets": 455.0, "totalCurrentLiabilities": 278.0},
    ]
    cashflow = [
        {"calendarYear": "2024", "operatingCashFlow": 207.0, "freeCashFlow": 152.0, "capitalExpenditure": -55.0},
        {"calendarYear": "2023", "operatingCashFlow": 181.0, "freeCashFlow": 133.0, "capitalExpenditure": -48.0},
    ]
    metrics = [
        {"calendarYear": "2024", "peRatio": 18.9, "pbRatio": 4.1, "evToEbitda": 14.8, "roe": 0.2263},
    ]
    quote = [{"symbol": ticker, "price": 182.4, "marketCap": 3250.0, "name": f"{ticker} Demo Holdings"}]
    profile = [{"symbol": ticker, "companyName": f"{ticker} Demo Holdings", "sector": "Technology", "industry": "Software", "exchangeShortName": "NASDAQ", "currency": "USD", "country": "US", "website": "https://example.com"}]
    peers = [
        {"symbol": f"{ticker}1", "companyName": "Peer One", "pe": 16.5, "revenueGrowth": 0.08},
        {"symbol": f"{ticker}2", "companyName": "Peer Two", "pe": 20.4, "revenueGrowth": 0.11},
        {"symbol": f"{ticker}3", "companyName": "Peer Three", "pe": 24.1, "revenueGrowth": 0.06},
    ]
    macro = {
        "gdp": {"observations": [{"date": "2024-10-01", "value": "29184.6"}]},
        "cpi": {"observations": [{"date": "2024-12-01", "value": "315.605"}]},
        "fed_funds": {"observations": [{"date": "2024-12-01", "value": "4.33"}]},
        "unemployment": {"observations": [{"date": "2024-12-01", "value": "4.1"}]},
    }
    return {
        "profile": profile,
        "quote": quote,
        "income": income,
        "balance": balance,
        "cashflow": cashflow,
        "metrics": metrics,
        "peers": peers,
        "macro": macro,
        "source_mode": "sample",
    }
