
import numpy as np
import pandas as pd
from core.black_scholes import call_price_vec, put_price_vec
from core.greeks import all_vanilla_greeks
from core.implied_vol import implied_vol


def clean_chain(df, spot, option_type="call"):
    df = df.copy()
    df = df[(df["bid"] > 0) & (df["ask"] > 0)].copy()
    df = df[(df["strike"] >= spot * 0.7) & (df["strike"] <= spot * 1.3)].copy()
    df["mid"] = (df["bid"] + df["ask"]) / 2.0
    df["moneyness"] = df["strike"] / spot
    return df.reset_index(drop=True)


def enrich_with_iv(df, spot, r, q=0.0, option_type="call"):
    df = df.copy()
    ivs = []
    for _, row in df.iterrows():
        iv = implied_vol(row["mid"], spot, row["strike"], row["timeToExpiry"], r, q, option_type)
        ivs.append(iv)
    df["impliedVol"] = ivs
    return df


def enrich_with_greeks(df, spot, r, q=0.0, option_type="call"):
    df = df.copy()
    greek_names = ["delta", "gamma", "vega", "theta", "rho", "speed"]
    for g in greek_names:
        df[g] = np.nan
    for idx, row in df.iterrows():
        sig = row.get("impliedVol", 0.30)
        if np.isnan(sig) or sig <= 0:
            sig = 0.30
        greeks = all_vanilla_greeks(spot, row["strike"], row["timeToExpiry"], r, sig, q, option_type)
        for g in greek_names:
            key = g.capitalize() if g != "speed" else "Speed"
            if key == "Gamma" or key == "Speed":
                df.at[idx, g] = greeks.get(key, np.nan)
            else:
                df.at[idx, g] = greeks.get(key, np.nan)
    return df


def full_pipeline(df, spot, r, option_type="call", q=0.0):
    df = clean_chain(df, spot, option_type)
    df = enrich_with_iv(df, spot, r, q, option_type)
    df = enrich_with_greeks(df, spot, r, q, option_type)
    return df
