import requests
from requests.exceptions import RequestException

payload = {'format':'json'}
url = "https://api.nbp.pl/api/exchangerates/rates/a/chf/"
try:
    response = requests.get(url, params = payload, timeout = 15)
    response.raise_for_status()
    data = response.json()
    rate = data['rates'][0]['mid']
    print(f"Aktualny kurs CHF: {rate} PLN")

except RequestException as e:
    print(f"Blad podczas komunikacji z API {e}")

