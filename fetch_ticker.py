import yfinance as yf
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import datetime as dt

def fetch_data():
    """Get user input and fetch data from yfinance"""

    # Get user data
    ticker = item_ticker_entry.get().strip().upper()
    date1 = item_date1_entry.get().strip()
    date2 = item_date2_entry.get().strip()

    # Check for empty entryboxes
    if not ticker or not date1:
        messagebox.showerror("Input Error", "Please provide ticker and first date")
        return

    # Check for invalid date format
    try:
        d1 = dt.datetime.strptime(date1, "%Y-%m-%d")
    except Exception:
        messagebox.showerror("Date Error", "Date 1 must be yyyy-mm-dd")
        return

    # Check for invalid ticker
    yfinance_ticker = yf.Ticker(ticker)
    try:
        current_price = yfinance_ticker.fast_info["last_price"]
    except (KeyError, TypeError):
        messagebox.showerror("Ticker Error", f"Invalid ticker: {ticker}")
        return

    # Single Date mode
    if mode_var.get() == "single":
        start = d1
        end = (d1 + dt.timedelta(days=1)).strftime("%Y-%m-%d")
        data = yfinance_ticker.history(start=start, end=end)
        if data.empty:
            messagebox.showerror("No Data", f"No data for {ticker} on {date1}. It might be a weekend or holiday")
            return
        open_price = data["Open"].iloc[0]
        high = data["High"].iloc[0]
        low = data["Low"].iloc[0]
        close_price = data["Close"].iloc[0]
        # Show 4 decimals for prices under 1$ or 2 decimals for the other prices
        if open_price < 1:
            result_label.config(text=f"O: {open_price:.4f}   H: {high:.4f}   L: {low:.4f}   C: {close_price:.4f}")
        else:
            result_label.config(text=f"O: {open_price:.2f}   H: {high:.2f}   L: {low:.2f}   C: {close_price:.2f}")
        return

    # Compare mode
    if not date2:
        messagebox.showerror("Input Error", "Please provide second date for comparison")
        return
    try:
        d2 = dt.datetime.strptime(date2, "%Y-%m-%d")
    except Exception:
        messagebox.showerror("Date Error", "Date 2 must be yyyy-mm-dd")
        return

    # Ensure ordering
    if d2 < d1:
        messagebox.showerror("Input Error", "Date 2 must be the same or after Date 1")
        return
    
    start = d1
    end = d2 + dt.timedelta(days=1)
    df = yfinance_ticker.history(start=start, end=end)
    if df.empty:
        messagebox.showerror("No Data", f"No historical data in range {start} to {end}")
        return
    d1_open = df["Open"].iloc[0]
    d2_close = df["Close"].iloc[-1]

    pct = (d2_close - d1_open) / d1_open * 100
    if d1_open < 1:
        result_label.config(text=f"Open {date1}: {d1_open:.4f}\nClose {date2}: {d2_close:.4f}\n% change: {pct:.2f}%")
        return
    result_label.config(text=f"Open {date1}: {d1_open:.2f}\nClose {date2}: {d2_close:.2f}\n% change: {pct:.2f}%")
    
    

# UI
root = tk.Tk()
root.title("Ticker Data Fetcher (NTUA FINCLUB)")

# Mode selection (single vs compare)
mode_var = tk.StringVar(value="single")
mode_frame = tk.Frame(root)
tk.Label(mode_frame, text="Mode:").pack(side="left")
tk.Radiobutton(mode_frame, text="Single date", variable=mode_var, value="single", command=lambda: toggle_mode()).pack(side="left")
tk.Radiobutton(mode_frame, text="Compare 2 dates", variable=mode_var, value="compare", command=lambda: toggle_mode()).pack(side="left")
mode_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

def toggle_mode():
    """Update UI based on RadioButton selection"""
    if mode_var.get() == "single":
        # Delete text inside Date2 box
        item_date2_entry.delete(0, tk.END)

        # Disable Date2 box and update its label
        item_date2_entry.config(state="disabled")
        item_date1_label.config(text= "Date (yyyy-mm-dd): ")
        item_date2_label.config(text="Date 2 (leave empty)")
    else:
        item_date2_entry.config(state="normal")
        item_date1_label.config(text= "Opening Date (yyyy-mm-dd): ")
        item_date2_label.config(text="Closing Date (yyyy-mm-dd):")

# Input fields (shifted rows by +1 due to mode_frame)
item_ticker_label = tk.Label(root, text="Stock Ticker: ")
item_ticker_label.grid(row=1, column=0, padx=5, pady=5)
item_ticker_entry = tk.Entry(root)
item_ticker_entry.grid(row=1, column=1, padx=5, pady=5)

item_date1_label = tk.Label(root, text="Date 1 (yyyy-mm-dd): ")
item_date1_label.grid(row=2, column=0, padx=5, pady=5)
item_date1_entry = tk.Entry(root)
item_date1_entry.grid(row=2, column=1, padx=5, pady=5)

item_date2_label = tk.Label(root, text="Date 2 (leave empty)")
item_date2_label.grid(row=3, column=0, padx=5, pady=5)
item_date2_entry = tk.Entry(root)
item_date2_entry.grid(row=3, column=1, padx=5, pady=5)

# Buttons
fetch_button = tk.Button(root, text="Fetch Data", command=fetch_data)
fetch_button.grid(row=4, column=0, padx=5, pady=5)

# Result Display
result_label = tk.Label(root, text="Result will appear here", wraplength=400, justify="left")
result_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# initialize mode UI
toggle_mode()

root.mainloop()
