from src.user_interface import Currency
from src.view_data import get_data_from_user
from src.nbp_api import get_exchange_rates



currencies = {currency.name.lower(): currency.value for currency in Currency}
days = 93
startDate, endDate, selected_label = get_data_from_user(days, currencies)
currency = [k for k, v in currencies.items() if v == selected_label][0] if selected_label else None

if startDate and endDate and currency:
    data = get_exchange_rates(currency, startDate, endDate)
    if data:
        print("Pobrano dane z NBP API")

    else:
        print("Nie udało się pobrać danych")




