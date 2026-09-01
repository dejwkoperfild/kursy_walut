import requests
from requests.exceptions import RequestException
import csv

startDate = '2026-08-01'
endDate = '2026-08-31'
# TO DO 
# Dorobienie okienka z wyborem dat
payload = {'format':'json'}
currency = 'chf'
url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/{startDate}/{endDate}"
try:
    response = requests.get(url, params = payload, timeout = 15)
    response.raise_for_status()
    data = response.json()
    with open('kursy.csv','w',newline='') as csvfile:
        fieldnames = ['Date','rate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for kurs in data['rates']:
            data_publikacji = kurs['effectiveDate']
            wartosc_srednia = kurs['mid']
            writer.writerow({'Date': data_publikacji, 'rate': wartosc_srednia})


except RequestException as e:
    print(f"Blad podczas komunikacji z API {e}")

