import requests

url = "http://api.nbp.pl/api/exchangerates/rates/a/chf/?format=json"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    rate = data['rates'][0]['mid']
    print(f"Aktualny kurs CHF: {rate} PLN")
else:
    print(f"Błąd zapytania: kod {response.status_code}")
