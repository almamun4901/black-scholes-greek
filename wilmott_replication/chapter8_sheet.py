"""
Wilmott Chapter 8 spreadsheet replication.

Reproduces the exact content of all sheets:
  Sheet 1: Contents (info only)
  Sheet 2: Spreadsheet functions / VB functions reference
  Sheet 3: Greeks — vanilla + binary call/put with all 8 Greeks
  Sheet 4: Implied Volatility — Newton-Raphson IV for 5 options
"""

import numpy as np
import pandas as pd
from core.greeks import all_vanilla_greeks, all_binary_greeks
from core.implied_vol import implied_vol


def replicate_greeks_sheet(S=100, sigma=0.20, q=0.0, r=0.05, K=100, T=1.0):
    """
    Reproduce the 'Greeks' sheet exactly.
    Returns dict with vanilla_call, vanilla_put, binary_call, binary_put.
    """
    vc = all_vanilla_greeks(S, K, T, r, sigma, q, "call")
    vp = all_vanilla_greeks(S, K, T, r, sigma, q, "put")
    bc = all_binary_greeks(S, K, T, r, sigma, q, "call")
    bp = all_binary_greeks(S, K, T, r, sigma, q, "put")

    params = {"Asset": S, "Volatility": sigma, "Div. Yield": q,
              "Int. rate": r, "Strike": K, "Expiry": T}
    return {"params": params, "vanilla_call": vc, "vanilla_put": vp,
            "binary_call": bc, "binary_put": bp}


def replicate_iv_sheet(S=100, r=0.08, tol=0.001,
                       market_prices=None, strikes=None, expiries=None):
    """
    Reproduce the 'Implied Volatility' sheet exactly.
    Default values match Wilmott's sheet.
    """
    if market_prices is None:
        market_prices = [18.6, 14.8, 11.5, 8.9, 7.0]
    if strikes is None:
        strikes = [90.0, 95.0, 100.0, 105.0, 110.0]
    if expiries is None:
        expiries = [1.0, 1.0, 1.0, 1.0, 1.0]

    ivs = []
    for mkt, K, T in zip(market_prices, strikes, expiries):
        iv = implied_vol(mkt, S, K, T, r, q=0.0, option_type="call", tol=tol)
        ivs.append(iv)

    return {
        "params": {"Asset": S, "Interest rate": r, "Error": tol},
        "data": pd.DataFrame({
            "Mkt Price": market_prices,
            "Strike": strikes,
            "Expiry": expiries,
            "Implied volatility": ivs,
        })
    }


def run_full_replication():
    """Execute full replication and print results matching Wilmott layout."""
    greeks = replicate_greeks_sheet()
    iv = replicate_iv_sheet()

    print("=" * 65)
    print("WILMOTT CHAPTER 8 — FULL SPREADSHEET REPLICATION")
    print("=" * 65)

    print("\n── Sheet: Greeks ──")
    p = greeks["params"]
    print(f"  Asset={p['Asset']}  Volatility={p['Volatility']}  "
          f"Div.Yield={p['Div. Yield']}  Int.rate={p['Int. rate']}  "
          f"Strike={p['Strike']}  Expiry={p['Expiry']}")

    for label, data in [("CALL", greeks["vanilla_call"]), ("PUT", greeks["vanilla_put"])]:
        print(f"\n  {label}:")
        for name, val in data.items():
            print(f"    {name:>6s}: {val:>16.10f}")

    for label, data in [("BINARY CALL", greeks["binary_call"]), ("BINARY PUT", greeks["binary_put"])]:
        print(f"\n  {label}:")
        for name, val in data.items():
            print(f"    {name:>6s}: {val:>16.10f}")

    print("\n── Sheet: Implied Volatility ──")
    p = iv["params"]
    print(f"  Asset={p['Asset']}  Interest rate={p['Interest rate']}  Error={p['Error']}")
    print(iv["data"].to_string(index=False))

    return {"greeks": greeks, "iv": iv}


if __name__ == "__main__":
    run_full_replication()
