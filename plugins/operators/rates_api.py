import logging
import requests

TARGET_CURR = "EUR,USD,CZK"


class GetRates:
    def __init__(self, base, amount):
        self.base = base
        self.amount = amount

    def get_rates(
        self,
    ):

        url = "https://api.exchangerate.host/latest"
        params = {
            "base": f"{self.base}",  # Reference base currency
            "symbols": f"{TARGET_CURR}",  # Comma-seperated values of currencies
            "amount": f"{self.amount}",  # Amount to convert
            "format": "json",
            "source": "ecb",
        }
        headers = {
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        }  # Avoiding caching behaviour as this is critical for updated rates.

        try:
            response = requests.get(
                url=url,
                params=params,
                headers=headers,
            )
            data = response.json()
            print("Script is working!")
            logging.info(f"{response.status_code} : GETTING CURRENCY VALUES")
            return data["rates"]
        except ValueError:
            logging.info(f"{response.status_code} : ERROR IN API REQUEST")