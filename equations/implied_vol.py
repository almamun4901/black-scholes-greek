# Implied Volatility
import numpy as np
from equations.black_scholes import call_price, put_price
from equations.greeks import vega


def implied_vol(
    market_price: float,
    S: float,  #asset price
    K: float,  #strike price
    T: float,  #time to expire
    r: float,  # interest rate
    q: float = 0.0,  #dividend
    option_type: str = "call",  #call or put
    tol: float = 0.001,  #tolerance
    max_iter: int = 100,  #max iterations
    initial_guess: float = 0.3,  #initial guess
) -> float:
    pricer = call_price if option_type.lower() == "call" else put_price

    if T <= 0 or market_price <= 0:
        return np.nan

    sigma = initial_guess

    for _ in range(max_iter):
        price = pricer(S, K, T, r, sigma, q)
        v = vega(S, K, T, r, sigma, q)

        if v < 1e-12:
            return _bisection_iv(market_price, S, K, T, r, q, pricer, tol)

        sigma_new = sigma - (price - market_price) / v

        if sigma_new <= 0:
            sigma = sigma / 2.0
            continue

        if abs(sigma_new - sigma) < tol:
            return sigma_new

        sigma = sigma_new

    return _bisection_iv(market_price, S, K, T, r, q, pricer, tol)


def _bisection_iv(market_price, S, K, T, r, q, pricer, tol, lo=0.001, hi=5.0, max_iter=200):
    for _ in range(max_iter):
        mid = (lo + hi) / 2.0
        price = pricer(S, K, T, r, mid, q)
        if abs(price - market_price) < tol:
            return mid
        if price > market_price:
            hi = mid
        else:
            lo = mid
        if (hi - lo) < tol:
            return mid
    return np.nan


def implied_vol_series(df, S, r, q=0.0, option_type="call", tol=0.001):
    price_col = "mid" if "mid" in df.columns else "lastPrice"
    ivs = []
    for _, row in df.iterrows():
        iv = implied_vol(
            market_price=row[price_col], S=S, K=row["strike"],
            T=row["timeToExpiry"], r=r, q=q, option_type=option_type, tol=tol,
        )
        ivs.append(iv)
    df = df.copy()
    df["impliedVol"] = ivs
    return df
