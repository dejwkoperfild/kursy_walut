import csv
from src.view_data import get_dates
from src.nbp_api import get_exchange_rates
import matplotlib.pyplot as plt

currencies = ["chf", "eur", "usd", "sek", "gpb"]
days = 183
startDate, endDate, currency = get_dates(days, currencies)

if startDate and endDate and currency:
    data = get_exchange_rates(currency, startDate, endDate)
    if data:
        with open(f'output_files/kursy_{currency}.csv','w',newline='') as csvfile:
            fieldnames = ['Date','rate']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for kurs in data['rates']:
                data_publikacji = kurs['effectiveDate']
                wartosc_srednia = kurs['mid']
                writer.writerow({'Date': data_publikacji, 'rate': wartosc_srednia})
            print("Pomyślnie zapisano plik")

        x_axis = [kurs['effectiveDate'] for kurs in data['rates']]
        y_axis = [kurs['mid'] for kurs in data['rates']]
        plt.plot(x_axis, y_axis)
        plt.title(f"Wykres kursu {currency} od {startDate} do {endDate}")
        plt.xlabel("Data")
        plt.ylabel("Kurs")
        plt.xticks(rotation=45)
        path = f'output_files/{currency}_{startDate}-{endDate}.png'
        plt.savefig(path, dpi=300, bbox_inches='tight')

    else:
        print("Nie udało się pobrać danych")

else:
    print("Nie udało się wybrać zakresu dat")



