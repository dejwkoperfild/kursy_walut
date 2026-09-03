import tkinter as tk
from tkcalendar import DateEntry
from datetime import date, timedelta
from tkinter import ttk

def get_dates():
    results = {"start": None, "end": None, "currency": None}


    def save_close():
        results["start"] = calendar_from.get_date()
        results["end"] = calendar_to.get_date()
        results["currency"] = combo.get()
        root.destroy()
    

    root = tk.Tk()
    root.title("Wybor daty")
    root.geometry("350x200")

    start_end_date = date.today()
    start_pick_date = start_end_date - timedelta(days=183)

    calendar_from = DateEntry(
            root,
            width=15,
            mindate=start_pick_date,
            maxdate=start_end_date,
            date_pattern='yyyy-mm-dd'
            )

    calendar_to = DateEntry(
            root,
            width=15,
            mindate=start_pick_date,
            maxdate=start_end_date,
            date_pattern='yyyy-mm-dd'
            )

    tk.Label(root, text="Data początkowa (od):").grid(row=0, column=0, padx=10,pady=20, sticky="e")
    calendar_from.grid(row=0, column=1, padx=10, pady=20)

    tk.Label(root, text="Data końcowa (do):").grid(row=1,column=0,padx=10,pady=5,sticky="e")
    calendar_to.grid(row=1, column=1, padx=10,pady=5)

    tk.Button(root, text="Zapisz i zamknij", command=save_close).grid(row=2, column=1, columnspan=2, pady=15)

    opcje = ["chf", "eur", "usd", "sek", "gpb", "uah"]

    combo = ttk.Combobox(root, values=opcje, state="readonly")
    combo.current(0)
    combo.grid(row=2, column=0, columnspan=1, pady=15)
    
    def aktualizuj_pole(event):
        currency = combo.get()

    combo.bind("<<ComboboxSelected>>", aktualizuj_pole)

    root.mainloop()

    return results["start"], results["end"], results["currency"]
