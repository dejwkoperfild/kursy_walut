import csv
from date_picker import get_dates
from nbp_api import get_exchange_rates



startDate, endDate = get_dates()

if startDate and endDate:
    data = get_exchange_rates('chf', startDate, endDate)
    if data:
        with open('kursy.csv','w',newline='') as csvfile:
            fieldnames = ['Date','rate']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for kurs in data['rates']:
                data_publikacji = kurs['effectiveDate']
                wartosc_srednia = kurs['mid']
                writer.writerow({'Date': data_publikacji, 'rate': wartosc_srednia})
            print("Pomyślnie zapisano plik")

    else:
        print("Nie udało się pobrać danych")

else:
    print("Nie udało się wybrać zakresu dat")



