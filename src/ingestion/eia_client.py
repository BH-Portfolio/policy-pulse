import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

class EIAClient:
    """Class wrapping EIA API requests"""

    def __init__(self, api_key: str):
        self.base_url = "https://api.eia.gov/v2"
        if not self.api_key:
            print("No EIA API Key Found")
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

    

