from unittest.mock import Mock, patch
import requests

from src.file_handler import prepare_data_for_graph, save_to_csv
from src.nbp_api import get_exchange_rates, get_today_exchange_rate
from src.user_interface import DateSelectorDialog


class FakeEntry:
    def __init__(self, value="0.00"):
        self.value = str(value)

    def get(self):
        return self.value

    def delete(self, start, end):
        self.value = ""

    def insert(self, index, text):
        self.value = text


class FakeCombo:
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value


class FakeLabel:
    def __init__(self, text="0.00"):
        self.text = text

    def config(self, text=None):
        if text is not None:
            self.text = text


class FakeVar:
    def __init__(self, value):
        self.value = value

    def set(self, value):
        self.value = value

    def get(self):
        return self.value


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
        "https://api.nbp.pl/api/exchangerates/rates/c/USD/2023-01-01/2023-01-10",
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


def test_get_today_exchange_rate_success():
    response = Mock()
    response.json.return_value = {"rates": [{"bid": 4.12, "ask": 4.20}]}
    session = Mock()
    session.get.return_value = response

    with patch("src.nbp_api.build_session", return_value=session):
        result = get_today_exchange_rate("USD")

    assert result["rates"][0]["bid"] == 4.12
    session.get.assert_called_once_with(
        "https://api.nbp.pl/api/exchangerates/rates/c/USD/today",
        params={"format": "json"},
        timeout=15,
    )
    response.raise_for_status.assert_called_once_with()


def test_save_to_csv_writes_expected_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    output_dir = tmp_path / "output_files"
    output_dir.mkdir()

    data = {
        "rates": [
            {"effectiveDate": "2024-01-01", "bid": 3.80, "ask": 4.00},
            {"effectiveDate": "2024-01-02", "bid": 3.90, "ask": 4.10},
        ]
    }

    save_to_csv(data, "USD", "2024-01-01", "2024-01-02")

    file_path = output_dir / "kursy_USD_2024-01-01-2024-01-02.csv"
    assert file_path.exists()

    content = file_path.read_text(encoding="utf-8")
    assert "Data,kurs_sprzedazy,kurs_kupna,spread" in content
    assert "2024-01-01" in content
    assert "0.2000" in content


def test_prepare_data_for_graph_returns_expected_axes():
    data = {
        "rates": [
            {"effectiveDate": "2024-01-01", "bid": 3.80, "ask": 4.00},
            {"effectiveDate": "2024-01-02", "bid": 3.90, "ask": 4.10},
        ]
    }

    x_axis, y_axis, z_axis = prepare_data_for_graph(data)

    assert [day.strftime("%Y-%m-%d") for day in x_axis] == ["2024-01-01", "2024-01-02"]
    assert y_axis == [3.80, 3.90]
    assert z_axis == [4.00, 4.10]


def test_reverse_conversion_and_clear_conversion_update_values():
    dialog = object.__new__(DateSelectorDialog)
    dialog.is_reversed = False
    dialog.source_currency_label = FakeVar("Kwota w PLN:")
    dialog.target_currency_label = FakeVar("Kwota w walucie docelowej:")
    dialog.amount_entry = FakeEntry("100")
    dialog.converted_amount_label = FakeLabel("0.00")
    dialog.converter_currency_combo = FakeCombo("Dolar amerykański")

    with patch("src.user_interface.get_today_exchange_rate", return_value={"rates": [{"bid": 4.0}]}) :
        dialog.reverse_conversion()

    assert dialog.is_reversed is True
    assert dialog.source_currency_label.get() == "Kwota w walucie obcej:"
    assert dialog.target_currency_label.get() == "Kwota w PLN:"
    assert dialog.converted_amount_label.text == "400.00"

    dialog.clear_conversion()

    assert dialog.amount_entry.get() == "0.00"
    assert dialog.converted_amount_label.text == "0.00"