import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(level=logging.ERROR)

def build_session() -> requests.Session:
    retry = Retry(
        total=4,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=frozenset(["GET"])
    )

    adapter = HTTPAdapter(max_retries=retry)

    session = requests.Session()
    session.mount("https://", adapter)

    return session

def get_exchange_rates(currency, start_date, end_date):
    session = build_session()
    payload = {'format':'json'}
    url = f"https://api.nbp.pl/api/exchangerates/rates/c/{currency}/{start_date}/{end_date}"
    try:
        response = session.get(url, params = payload, timeout = 15)
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

