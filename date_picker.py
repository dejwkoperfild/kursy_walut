import tkinter as tk
from tkcalendar import DateEntry
from datetime import date, timedelta


def get_dates():
    selected_dates = {"start": None, "end": None}


    def save_close():
        selected_dates["start"] = calendar_from.get_date()
        selected_dates["end"] = calendar_to.get_date()
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

    tk.Button(root, text="Zapisz i zamknij", command=save_close).grid(row=2, column=0, columnspan=2, pady=15)

    root.mainloop()

    return selected_dates["start"], selected_dates["end"]
