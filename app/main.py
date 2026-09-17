from src.user_interface import Currency
from src.view_data import get_data_from_user
from src.nbp_api import get_exchange_rates


def main():
    currencies = {currency.name.lower(): currency.value for currency in Currency}
    days = 93
    start_date, end_date, selected_label = get_data_from_user(days, currencies)
    currency = [
        code for code, label in currencies.items() if label == selected_label
    ][0] if selected_label else None

    if start_date and end_date and currency:
        data = get_exchange_rates(currency, start_date, end_date)
        if data:
            print("Pobrano dane z NBP API")

        else:
            print("Nie udało się pobrać danych")


if __name__ == "__main__":
    main()




