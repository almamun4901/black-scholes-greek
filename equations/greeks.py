# option greeks
import numpy as np
from scipy.stats import norm
from equations.black_scholes import d1, d2


def delta_call(S, K, T, r, sigma, q=0.0):
    return np.exp(-q * T) * norm.cdf(d1(S, K, T, r, sigma, q))

def delta_put(S, K, T, r, sigma, q=0.0):
    return np.exp(-q * T) * (norm.cdf(d1(S, K, T, r, sigma, q)) - 1.0)

def gamma(S, K, T, r, sigma, q=0.0):
    D1 = d1(S, K, T, r, sigma, q)
    return np.exp(-q * T) * norm.pdf(D1) / (S * sigma * np.sqrt(T))

def theta_call(S, K, T, r, sigma, q=0.0):
    D1 = d1(S, K, T, r, sigma, q)
    D2 = d2(S, K, T, r, sigma, q)
    t1 = -(S * np.exp(-q * T) * sigma * norm.pdf(D1)) / (2.0 * np.sqrt(T))
    t2 = q * S * np.exp(-q * T) * norm.cdf(D1)
    t3 = -r * K * np.exp(-r * T) * norm.cdf(D2)
    return t1 + t2 + t3

def theta_put(S, K, T, r, sigma, q=0.0):
    D1 = d1(S, K, T, r, sigma, q)
    D2 = d2(S, K, T, r, sigma, q)
    t1 = -(S * np.exp(-q * T) * sigma * norm.pdf(D1)) / (2.0 * np.sqrt(T))
    t2 = -q * S * np.exp(-q * T) * norm.cdf(-D1)
    t3 = r * K * np.exp(-r * T) * norm.cdf(-D2)
    return t1 + t2 + t3

def speed(S, K, T, r, sigma, q=0.0):
    D1 = d1(S, K, T, r, sigma, q)
    g = gamma(S, K, T, r, sigma, q)
    return -(g / S) * (D1 / (sigma * np.sqrt(T)) + 1.0)

def vega(S, K, T, r, sigma, q=0.0):
    D1 = d1(S, K, T, r, sigma, q)
    return S * np.exp(-q * T) * np.sqrt(T) * norm.pdf(D1)

def rho_call(S, K, T, r, sigma, q=0.0):
    D2 = d2(S, K, T, r, sigma, q)
    return K * T * np.exp(-r * T) * norm.cdf(D2)

def rho_put(S, K, T, r, sigma, q=0.0):
    D2 = d2(S, K, T, r, sigma, q)
    return -K * T * np.exp(-r * T) * norm.cdf(-D2)

def rhod_call(S, K, T, r, sigma, q=0.0):
    D1 = d1(S, K, T, r, sigma, q)
    return -S * T * np.exp(-q * T) * norm.cdf(D1)

def rhod_put(S, K, T, r, sigma, q=0.0):
    D1 = d1(S, K, T, r, sigma, q)
    return S * T * np.exp(-q * T) * norm.cdf(-D1)


# ═══════════════════════════════════════════════════════════════════════════
#  BINARY (DIGITAL) OPTIONS
# ═══════════════════════════════════════════════════════════════════════════

def binary_delta_call(S, K, T, r, sigma, q=0.0):
    D2 = d2(S, K, T, r, sigma, q)
    return np.exp(-r * T) * norm.pdf(D2) / (S * sigma * np.sqrt(T))

def binary_delta_put(S, K, T, r, sigma, q=0.0):
    return -binary_delta_call(S, K, T, r, sigma, q)

def binary_gamma_call(S, K, T, r, sigma, q=0.0):
    D1 = d1(S, K, T, r, sigma, q)
    D2 = d2(S, K, T, r, sigma, q)
    return -np.exp(-r * T) * norm.pdf(D2) * D1 / (S**2 * sigma**2 * T)

def binary_gamma_put(S, K, T, r, sigma, q=0.0):
    return -binary_gamma_call(S, K, T, r, sigma, q)

def _dd2_dT(S, K, T, r, sigma, q=0.0):
    return (-np.log(S / K) / (2 * sigma * T**1.5)
            + (r - q - 0.5 * sigma**2) / (2 * sigma * np.sqrt(T)))

def binary_theta_call(S, K, T, r, sigma, q=0.0):
    D2 = d2(S, K, T, r, sigma, q)
    dd2 = _dd2_dT(S, K, T, r, sigma, q)
    return r * np.exp(-r * T) * norm.cdf(D2) - np.exp(-r * T) * norm.pdf(D2) * dd2

def binary_theta_put(S, K, T, r, sigma, q=0.0):
    D2 = d2(S, K, T, r, sigma, q)
    dd2 = _dd2_dT(S, K, T, r, sigma, q)
    return r * np.exp(-r * T) * norm.cdf(-D2) + np.exp(-r * T) * norm.pdf(D2) * dd2

def binary_speed_call(S, K, T, r, sigma, q=0.0):
    D1 = d1(S, K, T, r, sigma, q)
    D2 = d2(S, K, T, r, sigma, q)
    sig_sqrtT = sigma * np.sqrt(T)
    bracket = (-D1 * D2 + 1) / sig_sqrtT - 2 * D1
    return -np.exp(-r * T) / (sigma**2 * T) * norm.pdf(D2) / S**3 * bracket

def binary_speed_put(S, K, T, r, sigma, q=0.0):
    return binary_speed_call(S, K, T, r, sigma, q)

def binary_vega_call(S, K, T, r, sigma, q=0.0):
    D1 = d1(S, K, T, r, sigma, q)
    D2 = d2(S, K, T, r, sigma, q)
    return -np.exp(-r * T) * norm.pdf(D2) * D1 / sigma

def binary_vega_put(S, K, T, r, sigma, q=0.0):
    return -binary_vega_call(S, K, T, r, sigma, q)

def binary_rho_call(S, K, T, r, sigma, q=0.0):
    D2 = d2(S, K, T, r, sigma, q)
    dd2_dr = np.sqrt(T) / sigma
    return -T * np.exp(-r * T) * norm.cdf(D2) + np.exp(-r * T) * norm.pdf(D2) * dd2_dr

def binary_rho_put(S, K, T, r, sigma, q=0.0):
    D2 = d2(S, K, T, r, sigma, q)
    dd2_dr = np.sqrt(T) / sigma
    return -T * np.exp(-r * T) * norm.cdf(-D2) - np.exp(-r * T) * norm.pdf(D2) * dd2_dr

def binary_rhod_call(S, K, T, r, sigma, q=0.0):
    D2 = d2(S, K, T, r, sigma, q)
    return -np.exp(-r * T) * norm.pdf(D2) * np.sqrt(T) / sigma

def binary_rhod_put(S, K, T, r, sigma, q=0.0):
    return -binary_rhod_call(S, K, T, r, sigma, q)


def all_vanilla_greeks(S, K, T, r, sigma, q=0.0, option_type="call"):
    is_call = option_type.lower() == "call"
    from equations.black_scholes import call_price, put_price
    return {
        "Value":  call_price(S, K, T, r, sigma, q) if is_call else put_price(S, K, T, r, sigma, q),
        "Delta":  delta_call(S, K, T, r, sigma, q) if is_call else delta_put(S, K, T, r, sigma, q),
        "Gamma":  gamma(S, K, T, r, sigma, q),
        "Theta":  theta_call(S, K, T, r, sigma, q) if is_call else theta_put(S, K, T, r, sigma, q),
        "Speed":  speed(S, K, T, r, sigma, q),
        "Vega":   vega(S, K, T, r, sigma, q),
        "Rho":    rho_call(S, K, T, r, sigma, q) if is_call else rho_put(S, K, T, r, sigma, q),
        "Rho D":  rhod_call(S, K, T, r, sigma, q) if is_call else rhod_put(S, K, T, r, sigma, q),
    }

def all_binary_greeks(S, K, T, r, sigma, q=0.0, option_type="call"):
    is_call = option_type.lower() == "call"
    from equations.black_scholes import binary_call_price, binary_put_price
    return {
        "Value":  binary_call_price(S, K, T, r, sigma, q) if is_call else binary_put_price(S, K, T, r, sigma, q),
        "Delta":  binary_delta_call(S, K, T, r, sigma, q) if is_call else binary_delta_put(S, K, T, r, sigma, q),
        "Gamma":  binary_gamma_call(S, K, T, r, sigma, q) if is_call else binary_gamma_put(S, K, T, r, sigma, q),
        "Theta":  binary_theta_call(S, K, T, r, sigma, q) if is_call else binary_theta_put(S, K, T, r, sigma, q),
        "Speed":  binary_speed_call(S, K, T, r, sigma, q) if is_call else binary_speed_put(S, K, T, r, sigma, q),
        "Vega":   binary_vega_call(S, K, T, r, sigma, q) if is_call else binary_vega_put(S, K, T, r, sigma, q),
        "Rho":    binary_rho_call(S, K, T, r, sigma, q) if is_call else binary_rho_put(S, K, T, r, sigma, q),
        "Rho D":  binary_rhod_call(S, K, T, r, sigma, q) if is_call else binary_rhod_put(S, K, T, r, sigma, q),
    }
