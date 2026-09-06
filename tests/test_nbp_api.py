from src.nbp_api import get_exchange_rates

def test_get_exchange_rates_success():
    url = "https://api.nbp.pl/api/exchangerates/rates/a/USD/2023-01-01/2023-01-10?format=json"
    result = get_exchange_rates("USD", "2023-01-01", "2023-01-10")
    assert result["currency"] == "dolar amerykański"
    assert result["code"] == "USD"