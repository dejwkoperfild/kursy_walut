import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import Menu



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
        self.combo = ttk.Combobox(self.main_frame, values=currencies, state="readonly")
        self.combo.current(0)
        self.combo.grid(row=2, column=1, padx=10, pady=15)

        tk.Button(self.main_frame, text="Zapisz i zamknij", command=self.save_and_close).grid(row=3, column=0, columnspan=2, pady=15, sticky="w")


        # create the widgets for the new tab
        tk.Label(self.new_frame, text="Kwota w PLN:").grid(row=0, column=0, padx=10, pady=(25, 10), sticky="w")
        
        tk.Label(self.new_frame, text="Waluta docelowa:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        tk.Button(self.new_frame, text="Przelicz", command=self.convert_amount).grid(row=2, column=0, padx=10, pady=15)
        tk.Button(self.new_frame, text="Wyczyść", command=self.clear_conversion).grid(row=2, column=1, padx=10, pady=15, sticky="w")

        self.combo = ttk.Combobox(self.new_frame, values=currencies, state="readonly")
        self.combo.current(0)
        self.combo.grid(row=1, column=1, padx=10, pady=10)


    def convert_amount(self):
            pass

    def clear_conversion(self):
            pass
    

    def save_and_close(self):
        self.results["start"] = self.calendar_from.get_date()
        self.results["end"] = self.calendar_to.get_date()
        self.results["currency"] = self.combo.get()
        self.root.destroy()

    def show(self):
        self.root.mainloop()
        return self.results["start"], self.results["end"], self.results["currency"]