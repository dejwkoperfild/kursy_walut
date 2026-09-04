import requests
import logging
from requests.exceptions import RequestException

logging.basicConfig(level=logging.ERROR)

def get_exchange_rates(currency, start_date, end_date):
    payload = {'format':'json'}
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/{start_date}/{end_date}"
    try:
        response = requests.get(url, params = payload, timeout = 15)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.HTTPError as e:
        logging.error(f"Błąd HTTP: {e.response.status_code} - {e}")
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Błąd połączenia z API NBP: {e}")
    except requests.exceptions.Timeout as e:
        logging.error(f"Przekroczono czas oczekiwania: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Nieoczekiwany błąd żądania: {e}")

    return None

