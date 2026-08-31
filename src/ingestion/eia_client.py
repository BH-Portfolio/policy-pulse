import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

class EIAClientErr(Exception):
    pass

class EIAClient:
    """Class wrapping EIA API requests"""

    def __init__(self, api_key: str):
        self.base_url = "https://api.eia.gov/v2"
        self.api_key = api_key or os.environ.get("EIA_API_KEY")
        if not self.api_key:
            raise EIAClientErr(
                "No EIA API key found. Set EIA_API_KEY in your .env file"
            )
        self.delay = 0.5

    def get_electricity_rates(self, state: str, start: str, end: str, sector: str = "RES", frequency: str = "monthly") -> list[dict]:
        """ Fetch retail electricity rates
            Args:
                state: two-letter state code
                start: period start
                end: period end
                sector: "RES", "COM", "IND"
                frequency: monthly or annual
        """
        url = f"{self.base_url}/electricity/retail-sales/data/"
        parameters = {
            "api_key": self.api_key,
            "frequency": frequency,
            "data[]": ["price", "sales"],
            "facets[stateid][]": state,
            "facets[sectorid][]": sector,
            "start": start,
            "end": end,
            "sort[0][column]": "period",
            "sort[0][column]": "desc",
            "length": 5000,
        }

        records: list[dict] = []
        offset = 0

        while True:
            parameters["offset"] = offset
            response = requests.get(url, params=parameters, timeout=30)

            if response.status_code != 200:
                raise EIAClientErr(
                    f"EIA API returned {response.status_code}: {response.text[:300]}"
                )

            payload = response.json().get("response", [])
            batch = payload.get("data", [])
            records.extend(batch)

            total = payload.get("total", len(records))
            offset += len(batch)

            if not batch or offset >= int(total):
                break

            time.sleep(self.delay)

        return records
