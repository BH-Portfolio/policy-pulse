import argparse
import json
from pathlib import Path

from src.ingestion.eia_client import EIAClient, EIAClientError
from src.ingestion.schemas import EnergyRateRecord
from pydantic import ValidationError


def parse_args():
    parser = argparse.ArgumentParser(description="Ingest EIA retail electricity rate data.")
    parser.add_argument("--state", required=True, help="Two-letter state code, e.g. CO")
    parser.add_argument("--start", required=True, help="Start period, e.g. 2025-01")
    parser.add_argument("--end", required=True, help="End period, e.g. 2026-06")
    parser.add_argument("--sector", default="RES", choices=["RES", "COM", "IND"])
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    client = EIAClient()

    try:
        raw_records = client.get_electricity_rates(
            state=args.state, start=args.start, end=args.end, sector=args.sector
        )
    except EIAClientError as e:
        print(f"Failed to fetch data: {e}")
        return

    validated = []
    skipped = 0

    for raw in raw_records:
        try:
            record = EnergyRateRecord.from_eia_record(raw)
            validated.append(record)
        except (ValueError, ValidationError):
            skipped += 1

    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"eia_{args.state}_{args.sector}_{args.start}_{args.end}.json"

    with open(out_path, "w") as f:
        json.dump([r.model_dump() for r in validated], f, indent=2, default=str)

    print(f"Fetched: {len(raw_records)} | Validated: {len(validated)} | Skipped: {skipped}")
    print(f"Wrote to: {out_path}")

