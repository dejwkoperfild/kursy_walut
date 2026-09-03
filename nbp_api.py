import requests
from requests.exceptions import RequestException

def get_exchange_rates(currency, start_date, end_date):
    payload = {'format':'json'}
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/{start_date}/{end_date}"
    try:
        response = requests.get(url, params = payload, timeout = 15)
        response.raise_for_status()
        data = response.json()
        return data

    except RequestException as e:
        print(f"Błąd podczas komunikacji z API: {e}")
        return None

