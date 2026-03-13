# Black Scholes
import numpy as np
from scipy.stats import norm

def d1(S, K, T, r, sigma, q=0.0):
    return (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))


def d2(S, K, T, r, sigma, q=0.0):
    return d1(S, K, T, r, sigma, q) - sigma * np.sqrt(T)


def call_price(S, K, T, r, sigma, q=0.0):
    if T <= 0:
        return max(S - K, 0.0)
    D1 = d1(S, K, T, r, sigma, q)
    D2 = d2(S, K, T, r, sigma, q)
    return S * np.exp(-q * T) * norm.cdf(D1) - K * np.exp(-r * T) * norm.cdf(D2)


def put_price(S, K, T, r, sigma, q=0.0):
    if T <= 0:
        return max(K - S, 0.0)
    D1 = d1(S, K, T, r, sigma, q)
    D2 = d2(S, K, T, r, sigma, q)
    return K * np.exp(-r * T) * norm.cdf(-D2) - S * np.exp(-q * T) * norm.cdf(-D1)



def binary_call_price(S, K, T, r, sigma, q=0.0):
    if T <= 0:
        return 1.0 if S > K else 0.0
    D2 = d2(S, K, T, r, sigma, q)
    return np.exp(-r * T) * norm.cdf(D2)


def binary_put_price(S, K, T, r, sigma, q=0.0):
    if T <= 0:
        return 1.0 if S < K else 0.0
    D2 = d2(S, K, T, r, sigma, q)
    return np.exp(-r * T) * norm.cdf(-D2)


def call_price_vec(S, K, T, r, sigma, q=0.0):
    S, K = np.asarray(S, dtype=float), np.asarray(K, dtype=float)
    D1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    D2 = D1 - sigma * np.sqrt(T)
    return S * np.exp(-q * T) * norm.cdf(D1) - K * np.exp(-r * T) * norm.cdf(D2)


def put_price_vec(S, K, T, r, sigma, q=0.0):
    S, K = np.asarray(S, dtype=float), np.asarray(K, dtype=float)
    D1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    D2 = D1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * norm.cdf(-D2) - S * np.exp(-q * T) * norm.cdf(-D1)
