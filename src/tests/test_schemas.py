import pytest
from pydantic import ValidationError

from src.ingestion.schemas import EnergyRateRecord, Sector


def test_from_eia_record_valid():
    raw = {
        "period": "2026-06",
        "stateid": "co",  # lowercase on purpose — tests the uppercase validator
        "sectorid": "RES",
        "price": 14.23,
        "sales": 1234.5,
    }

    record = EnergyRateRecord.from_eia_record(raw)

    assert record.state == "CO"
    assert record.sector == Sector.RESIDENTIAL
    assert record.period == "2026-06"
    assert record.price_cents_per_kwh == 14.23
    assert record.sales_million_kwh == 1234.5


def test_from_eia_record_skips_all_sector():
    raw = {
        "period": "2026-06",
        "stateid": "CO",
        "sectorid": "ALL",
        "price": 13.0,
        "sales": 5000.0,
    }

    with pytest.raises(ValueError):
        EnergyRateRecord.from_eia_record(raw)


def test_from_eia_record_invalid_sector_raises():
    raw = {
        "period": "2026-06",
        "stateid": "CO",
        "sectorid": "XYZ",  # not a real sector
        "price": 14.23,
        "sales": 1234.5,
    }

    with pytest.raises(ValidationError):
        EnergyRateRecord.from_eia_record(raw)


def test_state_must_be_two_letters():
    with pytest.raises(ValidationError):
        EnergyRateRecord(
            state="Colorado",  # not a 2-letter code
            sector=Sector.RESIDENTIAL,
            period="2026-06",
            price_cents_per_kwh=14.23,
            sales_million_kwh=1234.5,
        )


def test_from_eia_record_missing_field_raises():
    raw = {
        "period": "2026-06",
        "stateid": "CO",
        "sectorid": "RES",
        # missing "price"
        "sales": 1234.5,
    }

    with pytest.raises(KeyError):
        EnergyRateRecord.from_eia_record(raw)
        