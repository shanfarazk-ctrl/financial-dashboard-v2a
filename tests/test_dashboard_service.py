from backend.services.dashboard_service import DashboardService


def test_dashboard_service_returns_expected_keys():
    service = DashboardService()
    result = service.analyze("AAPL")
    for key in ["profile", "quote", "kpis", "growth", "risks", "valuation", "scoring", "memo"]:
        assert key in result
