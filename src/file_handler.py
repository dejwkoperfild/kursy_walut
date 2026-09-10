import csv
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.pyplot as plt

def save_to_csv(data, currency, startDate, endDate):
    with open(f'output_files/kursy_{currency}_{startDate}-{endDate}.csv','w',newline='') as csvfile:
                fieldnames = ['Data','kurs_sprzedazy','kurs_kupna']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for kurs in data['rates']:
                    data_publikacji = kurs['effectiveDate']
                    kurs_sprzedzy = kurs['bid']
                    kurs_kupna = kurs['ask']
                    writer.writerow({'Data': data_publikacji, 'kurs_sprzedazy': kurs_sprzedzy, 'kurs_kupna': kurs_kupna})
                print("Pomyślnie zapisano plik")

def save_to_png(data, currency, startDate, endDate):
    x_axis = [datetime.strptime(kurs['effectiveDate'], '%Y-%m-%d') for kurs in data['rates']]
    y_axis = [kurs['bid'] for kurs in data['rates']]
    z_axis = [kurs['ask'] for kurs in data['rates']]
    plt.plot(x_axis, y_axis, label='Kurs sprzedaży')
    plt.plot(x_axis, z_axis, label='Kurs kupna')
    plt.title(f"Wykres kursu {currency} od {startDate} do {endDate}")
    plt.xlabel("Data")
    plt.ylabel("Kurs")
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()
    plt.grid()
    path = f'output_files/{currency}_{startDate}-{endDate}.png'
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.show()