import requests
from requests.exceptions import RequestException
import csv
import tkinter as tk
from tkcalendar import DateEntry
from datetime import date, timedelta

root = tk.Tk()
root.title("Wybor daty")
root.geometry("350x200")

start_end_date = date.today()
start_pick_date = start_end_date - timedelta(days=183)

calendar = DateEntry(
        root,
        width=15,
        mindate=start_pick_date,
        maxdate=start_end_date,
        date_pattern='yyyy-mm-dd'
        )
calendar.pack(padx=20, pady=20)

root.mainloop()


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
        print("Pomyślnie zapisano plik")


except RequestException as e:
    print(f"Blad podczas komunikacji z API {e}")

