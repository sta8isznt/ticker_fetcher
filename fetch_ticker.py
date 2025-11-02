import yfinance as yf
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import datetime as dt

def fetch_data():
    ticker = item_ticker_entry.get().strip().upper()
    date = item_date_entry.get().strip()

    if not ticker or not date:
        messagebox.showerror("Input Error", "Please provide valid ticker and date")

    yfinance_ticker = yf.Ticker(ticker)

    next_day = dt.datetime.strptime(date, "%Y-%m-%d")
    next_day += dt.timedelta(days=1)
    data = yfinance_ticker.history(start=date, end=next_day)

    open_price = data["Open"].iloc[0]
    high = data["High"].iloc[0]
    low = data["Low"].iloc[0]
    close_price = data["Close"].iloc[0]

    result_label.config(text=f"O: {open_price:.2f}\tH: {high:.2f}\tL: {low:.2f}\tC: {close_price:.2f}")

root = tk.Tk()
root.title("Ticker Data Fetcher (NTUA FINCLUB)")

# Input fields
item_ticker_label = tk.Label(root, text="Stock Ticker: ")
item_ticker_label.grid(row=0, column=0, padx=5, pady=5)
item_ticker_entry = tk.Entry(root)
item_ticker_entry.grid(row=0, column=1, padx=5, pady=5)

item_date_label = tk.Label(root, text="Date (yyyy-mm-dd): ")
item_date_label.grid(row=1, column=0, padx=5, pady=5)
item_date_entry = tk.Entry(root)
item_date_entry.grid(row=1, column=1, padx=5, pady=5)

# Buttons
fetch_button = tk.Button(root, text="Fetch Data", command=fetch_data)
fetch_button.grid(row=2, column=0, padx=5, pady=5)

# Result Display
result_label = tk.Label(root, text="Result will appear here", wraplength=300)
result_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)


root.mainloop()