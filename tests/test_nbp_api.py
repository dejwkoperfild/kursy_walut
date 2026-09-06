from unittest.mock import Mock, patch
import requests
from src.nbp_api import get_exchange_rates

def test_get_exchange_rates_success():
    response = Mock()
    response.json.return_value = {
        "currency": "dolar amerykański",
        "code": "USD",
        "rates": [],
    }
    session = Mock()
    session.get.return_value = response

    with patch("src.nbp_api.build_session", return_value=session):
        result = get_exchange_rates("USD", "2023-01-01", "2023-01-10")

    assert result["currency"] == "dolar amerykański"
    assert result["code"] == "USD"
    session.get.assert_called_once_with(
        "https://api.nbp.pl/api/exchangerates/rates/a/USD/2023-01-01/2023-01-10",
        params={"format": "json"},
        timeout=15,
    )
    response.raise_for_status.assert_called_once_with()


def test_get_exchange_rates_returns_none_for_request_errors():
    exceptions = [
        requests.exceptions.ConnectionError("connection failed"),
        requests.exceptions.Timeout("request timed out"),
        requests.exceptions.RequestException("request failed"),
    ]

    for exception in exceptions:
        session = Mock()
        session.get.side_effect = exception

        with patch("src.nbp_api.build_session", return_value=session):
            result = get_exchange_rates("EUR", "2023-01-01", "2023-01-10")

        assert result is None


def test_get_exchange_rates_returns_none_for_http_error():
    response = Mock()
    response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "not found", response=response
    )
    response.status_code = 404
    session = Mock()
    session.get.return_value = response

    with patch("src.nbp_api.build_session", return_value=session):
        result = get_exchange_rates("GBP", "2023-01-01", "2023-01-10")

    assert result is None
    response.json.assert_not_called()