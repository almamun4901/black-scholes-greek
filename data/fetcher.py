import datetime
import numpy as np
import pandas as pd
import yfinance as yf


def get_spot_price(ticker):
    tk = yf.Ticker(ticker)
    hist = tk.history(period="1d")
    # if not data or fetching error
    if hist.empty:
        raise ValueError(f"No price data for {ticker}")
    return float(hist["Close"].iloc[-1])


def get_risk_free_rate():
    try:
        irx = yf.Ticker("^IRX")
        # default 5 days
        hist = irx.history(period="5d")
        if not hist.empty:
            return float(hist["Close"].iloc[-1]) / 100.0
    except Exception:
        pass
    return 0.05


def get_options_chain(ticker, expiry_index=0):
    tk = yf.Ticker(ticker)
    expirations = tk.options
    if not expirations:
        raise ValueError(f"No options data for {ticker}")
    expiry_index = min(expiry_index, len(expirations) - 1)
    expiry_str = expirations[expiry_index]
    chain = tk.option_chain(expiry_str)
    spot = get_spot_price(ticker)
    r = get_risk_free_rate()
    expiry_date = datetime.datetime.strptime(expiry_str, "%Y-%m-%d")
    T = max((expiry_date - datetime.datetime.now()).days, 1) / 365.0
    calls, puts = chain.calls.copy(), chain.puts.copy()
    for df in [calls, puts]:
        df["timeToExpiry"] = T
        df["mid"] = (df["bid"] + df["ask"]) / 2.0
    
    return{
        "calls" : calls,
        "puts" : puts,
        "expiry" : expiry_str,
        "T" : T,
        "spot" : spot,
        "r" : r,
        "all_expiries" : list(expirations)
    }
