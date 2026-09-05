import tkinter as tk
from tkcalendar import DateEntry
from datetime import date, timedelta
from tkinter import ttk
from src.user_interface import DateSelectorDialog

def get_data_from_user(days : int, currencies : dict):
    start_end_date = date.today()
    start_pick_date = start_end_date - timedelta(days=days)
    etykiety = list(currencies.values())

    window = DateSelectorDialog(
        min_date=start_pick_date,
        max_date=start_end_date,
        currencies=etykiety
    )

    start_date, end_date, currency = window.show()
    
    return start_date, end_date, currency