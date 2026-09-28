import requests

def get_current_exchange_rate(currency_code: str) -> float:
    """Returns the currently applicable average NBP exchange rate."""

    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    return data["rates"][0]["mid"]