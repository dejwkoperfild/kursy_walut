import csv
import datetime
from src.view_data import get_data_from_user
from src.nbp_api import get_exchange_rates
from src.file_handler import save_to_csv, save_to_png

currencies = ["chf", "eur", "usd", "sek", "gpb"]
days = 183
startDate, endDate, currency = get_data_from_user(days, currencies)

if startDate and endDate and currency:
    data = get_exchange_rates(currency, startDate, endDate)
    if data:
        save_to_csv(data, currency, startDate, endDate)
        save_to_png(data, currency, startDate, endDate)

    else:
        print("Nie udało się pobrać danych")

else:
    print("Nie udało się pobrać danych od użytkownika")



