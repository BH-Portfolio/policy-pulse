import pytest
import responses

from src.ingestion.eia_client import EIAClient, EIAClientError


FAKE_API_KEY = "test-key-123"


def make_response(records, total=None):
    """Helper to build a fake EIA API response payload."""
    return {
        "response": {
            "total": total if total is not None else len(records),
            "data": records,
        }
    }


@responses.activate
def test_get_electricity_rates_returns_records():
    fake_records = [
        {
            "period": "2026-06",
            "stateid": "CO",
            "sectorid": "RES",
            "price": 14.23,
            "sales": 1234.5,
        },
        {
            "period": "2026-05",
            "stateid": "CO",
            "sectorid": "RES",
            "price": 14.01,
            "sales": 1200.0,
        },
    ]

    responses.add(
        responses.GET,
        "https://api.eia.gov/v2/electricity/retail-sales/data/",
        json=make_response(fake_records),
        status=200,
    )

    client = EIAClient(api_key=FAKE_API_KEY, delay=0)
    result = client.get_electricity_rates("CO", "2026-05", "2026-06")

    assert len(result) == 2
    assert result[0]["stateid"] == "CO"
    assert result[0]["price"] == 14.23


@responses.activate
def test_get_electricity_rates_paginates():
    page_1 = [{"period": f"2026-{i:02d}", "stateid": "CO", "sectorid": "RES", "price": 14.0, "sales": 100.0} for i in range(1, 6)]
    page_2 = [{"period": f"2025-{i:02d}", "stateid": "CO", "sectorid": "RES", "price": 13.5, "sales": 95.0} for i in range(1, 4)]

    responses.add(
        responses.GET,
        "https://api.eia.gov/v2/electricity/retail-sales/data/",
        json=make_response(page_1, total=8),
        status=200,
    )
    responses.add(
        responses.GET,
        "https://api.eia.gov/v2/electricity/retail-sales/data/",
        json=make_response(page_2, total=8),
        status=200,
    )

    client = EIAClient(api_key=FAKE_API_KEY, delay=0)
    result = client.get_electricity_rates("CO", "2025-01", "2026-06")

    assert len(result) == 8
    assert len(responses.calls) == 2


@responses.activate
def test_get_electricity_rates_raises_on_error_status():
    responses.add(
        responses.GET,
        "https://api.eia.gov/v2/electricity/retail-sales/data/",
        json={"error": "invalid api key"},
        status=403,
    )

    client = EIAClient(api_key=FAKE_API_KEY, delay=0)

    with pytest.raises(EIAClientError):
        client.get_electricity_rates("CO", "2026-01", "2026-06")


def test_client_requires_api_key(monkeypatch):
    monkeypatch.delenv("EIA_API_KEY", raising=False)
    with pytest.raises(EIAClientError):
        EIAClient(api_key=None)
        