from backend.engine.kpi_engine import compute_growth, compute_kpis


def test_compute_kpis_and_growth():
    latest_is = {"revenue": 110, "grossProfit": 44, "operatingIncome": 22, "netIncome": 11}
    prior_is = {"revenue": 100, "netIncome": 10}
    latest_bs = {
        "totalAssets": 200,
        "totalDebt": 50,
        "cashAndCashEquivalents": 25,
        "totalStockholdersEquity": 100,
        "totalCurrentAssets": 80,
        "totalCurrentLiabilities": 40,
    }
    latest_cf = {"operatingCashFlow": 18, "freeCashFlow": 9}
    latest_metrics = {"peRatio": 18, "pbRatio": 2, "evToEbitda": 10}

    kpis = compute_kpis(latest_is, latest_bs, latest_cf, latest_metrics)
    growth = compute_growth(latest_is, prior_is)

    assert round(kpis["gross_margin"], 4) == 0.4
    assert round(kpis["operating_margin"], 4) == 0.2
    assert round(kpis["roe"], 4) == 0.11
    assert round(growth["revenue_growth"], 4) == 0.1
