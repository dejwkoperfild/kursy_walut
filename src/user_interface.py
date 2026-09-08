import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import Menu


class DateSelectorDialog:
    def __init__(self, min_date, max_date, currencies):
        self.root = tk.Tk()
        self.root.title("Kursy walut NBP")
        self.root.geometry("350x200")

        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
                
        def about():
            print("About this application")

        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)

       
        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=about)
        
        self.results = {"start": None, "end": None, "currency": None}

        self.calendar_from = DateEntry(
            self.root, width=15, mindate=min_date, maxdate=max_date, date_pattern='yyyy-mm-dd'
        )
        self.calendar_to = DateEntry(
            self.root, width=15, mindate=min_date, maxdate=max_date, date_pattern='yyyy-mm-dd'
        )

        tk.Label(self.root, text="Data początkowa (od):").grid(row=0, column=0, padx=10, pady=20, sticky="w")
        self.calendar_from.grid(row=0, column=1, padx=10, pady=20)

        tk.Label(self.root, text="Data końcowa (do):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.calendar_to.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Waluta:").grid(row=2, column=0, padx=10, pady=15, sticky="w")
        self.combo = ttk.Combobox(self.root, values=currencies, state="readonly")
        self.combo.current(0)
        self.combo.grid(row=2, column=1, padx=10, pady=15)

    def save_and_close(self):
        self.results["start"] = self.calendar_from.get_date()
        self.results["end"] = self.calendar_to.get_date()
        self.results["currency"] = self.combo.get()
        self.root.destroy()

    def show(self):
        self.root.mainloop()
        return self.results["start"], self.results["end"], self.results["currency"]