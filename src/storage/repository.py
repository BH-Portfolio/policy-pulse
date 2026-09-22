from src.ingestion.schemas import EnergyRateRecord
from src.storage.db import get_session
from src.storage.models import RateRecord


def upsert_records(records: list[EnergyRateRecord]) -> int:
    session = get_session()

    return 0


def get_rates(state: str, sector: str, start: str, end: str) -> list[RateRecord]:
    
    return []