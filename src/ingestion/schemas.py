from enum import Enum
from pydantic import BaseModel, field_validator

class Sector(str, Enum):
    RESIDENTIAL = "RES"
    COMMERCIAL = "COM"
    INDUSTRIAL = "IND"

class EnergyRateRecord(BaseModel):

    state: str
    sector: str
    period: str
    price_cents_per_kwh: float
    sales_million_kwh: float

    @field_validator("state")
    @classmethod
    def state_must_be_two_letters(cls, v: str) -> str:
        if len(v) != 2:
            raise ValueError(f"state must be a 2-letter code, got '{v}'")
        return v.upper()

    @classmethod
    def from_eia_record(cls, raw: dict) -> "EnergyRateRecord":
        """
        Build a validated EnergyRateRecord from one raw EIA dict
        """
        sector_raw = raw.get("sectorid")
        if sector_raw == "ALL":
            raise ValueError("Skipping 'ALL' sector aggregate row")

        return cls(
            state=raw["stateid"],
            sector=sector_raw,
            period=raw["period"],
            price_cents_per_kwh=raw["price"],
            sales_million_kwh=raw["sales"],
        )
    