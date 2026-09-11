import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import Menu
from src.file_handler import save_to_csv, save_to_png, show_graph
from src.nbp_api import get_exchange_rates, get_today_exchange_rate
from enum import Enum

class Currency(Enum):
    CHF = "Frank szwajcarski"
    EUR = "Euro"
    USD = "Dolar amerykański"
    SEK = "Korona szwedzka"
    GBP = "Funt szterling"

class DateSelectorDialog:
    def __init__(self, min_date, max_date, currencies):
        self.root = tk.Tk()
        self.root.title("Kursy walut NBP")
        self.root.geometry("420x280")

        # create frames for the main view and the new tab
        self.main_frame = tk.Frame(self.root)
        self.new_frame = tk.Frame(self.root)

        # place the frames in the same location, but only one will be visible at a time
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.new_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.main_frame.tkraise()

        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
        def about():
            print("About this application")


        def show_new_tab():
            self.new_frame.tkraise()

        def show_main_tab():
            self.main_frame.tkraise()

        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_command(label="Główny widok", command=show_main_tab)
        menu_bar.add_command(label="Przelicznik walut", command=show_new_tab)
        menu_bar.add_cascade(label="Pomoc", menu=help_menu)
        help_menu.add_command(label="O aplikacji", command=about)

    
        
        self.results = {"start": None, "end": None, "currency": None}

        # create the date selection widgets for the main view
        self.calendar_from = DateEntry(
            self.main_frame, width=15, mindate=min_date, maxdate=max_date, date_pattern='yyyy-mm-dd'
        )
        self.calendar_to = DateEntry(
            self.main_frame, width=15, mindate=min_date, maxdate=max_date, date_pattern='yyyy-mm-dd'
        )

        tk.Label(self.main_frame, text="Data początkowa (od):").grid(row=0, column=0, padx=10, pady=20, sticky="w")
        self.calendar_from.grid(row=0, column=1, padx=10, pady=20)

        tk.Label(self.main_frame, text="Data końcowa (do):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.calendar_to.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.main_frame, text="Waluta:").grid(row=2, column=0, padx=10, pady=15, sticky="w")
        self.main_currency_combo = ttk.Combobox(self.main_frame, values=currencies, state="readonly")
        self.main_currency_combo.current(0)
        self.main_currency_combo.grid(row=2, column=1, padx=10, pady=15)

        button_frame = tk.Frame(self.main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        tk.Button(button_frame, text="Zapisz i zamknij", command=self.save_and_close).grid(
            row=0, column=0, padx=5, pady=5
        )
        tk.Button(button_frame, text="Eksportuj wykres do PNG", command=self.export_to_graph).grid(
            row=0, column=1, padx=5, pady=5
        )
        tk.Button(button_frame, text="Eksportuj do CSV", command=self.export_to_csv).grid(
            row=1, column=0, padx=5, pady=5
        )
        tk.Button(button_frame, text="Pokaż wykres", command=self.show_graph).grid(
                    row=1, column=1, padx=5, pady=5
                )


        # create the widgets for the new tab
        tk.Label(self.new_frame, text="Kwota w PLN:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.amount_entry = tk.Spinbox(self.new_frame, from_=0, to=100000, increment=0.01, width=15)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=(25, 10))
        tk.Label(self.new_frame, text="Kwota w walucie docelowej:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        tk.Label(self.new_frame, text="Waluta docelowa:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.converted_amount_label = tk.Label(self.new_frame, text="0.00")
        self.converted_amount_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        tk.Button(self.new_frame, text="Przelicz", command=self.convert_amount).grid(row=3, column=0, padx=10, pady=15)
        tk.Button(self.new_frame, text="Wyczyść", command=self.clear_conversion).grid(row=3, column=1, padx=10, pady=15, sticky="w")

        self.converter_currency_combo = ttk.Combobox(self.new_frame, values=currencies, state="readonly")
        self.converter_currency_combo.current(0)
        self.converter_currency_combo.grid(row=2, column=1, padx=10, pady=10)


    def convert_amount(self):
        amount = float(self.amount_entry.get())
        currency = self.converter_currency_combo.get()
        currencies = {currency.name.lower(): currency.value for currency in Currency}
        currency_code = [k for k, v in currencies.items() if v == currency][0] if currency else None
        data = get_today_exchange_rate(currency_code)
        if data:
            rate = data['rates'][0]['bid']
            converted_amount = amount / rate
            self.converted_amount_label.config(text=f"{converted_amount:.2f}")
        else:
            print("Nie udało się pobrać danych")

    def clear_conversion(self):
            pass

    def choose_currency(self, event):
        self.results["currency"] = self.main_currency_combo.get()
        currencies = {currency.name.lower(): currency.value for currency in Currency}
        currency = [k for k, v in currencies.items() if v == self.results["currency"]][0] if self.results["currency"] else None
        return currency

    def export_to_graph(self):
        self.results["start"] = self.calendar_from.get_date()
        self.results["end"] = self.calendar_to.get_date()
        currency = self.choose_currency(None)
        data = get_exchange_rates(currency, self.results["start"], self.results["end"])
        if data:
            save_to_png(data, currency, self.results["start"], self.results["end"])
            print("Dane zapisane do pliku PNG")
        else:
            print("Nie udało się pobrać danych")

    def export_to_csv(self):
        self.results["start"] = self.calendar_from.get_date()
        self.results["end"] = self.calendar_to.get_date()
        currency = self.choose_currency(None)
        data = get_exchange_rates(currency, self.results["start"], self.results["end"])
        if data:
            save_to_csv(data, currency, self.results["start"], self.results["end"])
            print("Dane zapisane do pliku CSV")
        else:
            print("Nie udało się pobrać danych")

    def show_graph(self):
        self.results["start"] = self.calendar_from.get_date()
        self.results["end"] = self.calendar_to.get_date()
        currency = self.choose_currency(None)
        data = get_exchange_rates(currency, self.results["start"], self.results["end"])
        if data:
            show_graph(data, currency, self.results["start"], self.results["end"])
            print("Wykres został wyświetlony")
        else:
            print("Nie udało się pobrać danych")

    def save_and_close(self):
        self.results["start"] = self.calendar_from.get_date()
        self.results["end"] = self.calendar_to.get_date()
        self.results["currency"] = self.main_currency_combo.get()
        self.root.destroy()

    def show(self):
        self.root.mainloop()
        return self.results["start"], self.results["end"], self.results["currency"]