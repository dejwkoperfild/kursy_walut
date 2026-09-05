from src.view_data import get_data_from_user
from src.nbp_api import get_exchange_rates
from src.file_handler import save_to_csv, save_to_png

currencies = {"chf": "Frank szwajcarski", "eur": "Euro", "usd": "Dolar amerykański", "sek": "Korona szwedzka", "gpb": "Funt szterling"}
days = 183
startDate, endDate, selected_label = get_data_from_user(days, currencies)
currency = [k for k, v in currencies.items() if v == selected_label][0] if selected_label else None

if startDate and endDate and currency:
    data = get_exchange_rates(currency, startDate, endDate)
    if data:
        save_to_csv(data, currency, startDate, endDate)
        save_to_png(data, currency, startDate, endDate)

    else:
        print("Nie udało się pobrać danych")

else:
    print("Nie udało się pobrać danych od użytkownika")



