import numpy as np
import matplotlib.pyplot as plt
from equations.greeks import (delta_call, delta_put, gamma, vega, theta_call, theta_put, rho_call, rho_put, speed)


def plot_greeks_vs_strike(S, K_range, T, r, sigma, q=0.0, option_type="call", save_path=None):
    K = np.asarray(K_range, dtype=float)
    is_call = option_type.lower() == "call"

    deltas = delta_call(S, K, T, r, sigma, q) if is_call else delta_put(S, K, T, r, sigma, q)
    gammas = gamma(S, K, T, r, sigma, q)
    vegas = vega(S, K, T, r, sigma, q)
    thetas = (theta_call(S, K, T, r, sigma, q) if is_call else theta_put(S, K, T, r, sigma, q)) / 365
    rhos = rho_call(S, K, T, r, sigma, q) if is_call else rho_put(S, K, T, r, sigma, q)
    speeds = speed(S, K, T, r, sigma, q)

    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.suptitle(
        f"Black-Scholes Greeks vs Strike  |  S={S}, T={T:.2f}y, "
        f"\u03c3={sigma:.0%}, r={r:.1%}, q={q:.1%}  [{option_type.upper()}]",
        fontsize=14, fontweight="bold")

    plots = [
        (axes[0, 0], deltas, "Delta", "tab:blue"),
        (axes[0, 1], gammas, "Gamma", "tab:orange"),
        (axes[0, 2], vegas,  "Vega",  "tab:green"),
        (axes[1, 0], thetas, "Theta (per day)", "tab:red"),
        (axes[1, 1], rhos,   "Rho",   "tab:purple"),
        (axes[1, 2], speeds, "Speed", "tab:brown"),
    ]
    for ax, data, title, color in plots:
        ax.plot(K, data, color=color, linewidth=2)
        ax.axvline(S, color="gray", linestyle="--", alpha=0.5, label=f"Spot={S}")
        ax.set_title(title, fontsize=12)
        ax.set_xlabel("Strike")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_greeks_vs_spot(S_range, K, T, r, sigma, q=0.0, option_type="call", save_path=None):
    S = np.asarray(S_range, dtype=float)
    is_call = option_type.lower() == "call"

    deltas = delta_call(S, K, T, r, sigma, q) if is_call else delta_put(S, K, T, r, sigma, q)
    gammas = gamma(S, K, T, r, sigma, q)
    vegas = vega(S, K, T, r, sigma, q)
    thetas = (theta_call(S, K, T, r, sigma, q) if is_call else theta_put(S, K, T, r, sigma, q)) / 365
    rhos = rho_call(S, K, T, r, sigma, q) if is_call else rho_put(S, K, T, r, sigma, q)
    speeds = speed(S, K, T, r, sigma, q)

    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.suptitle(
        f"Black-Scholes Greeks vs Spot  |  K={K}, T={T:.2f}y, "
        f"\u03c3={sigma:.0%}, r={r:.1%}, q={q:.1%}  [{option_type.upper()}]",
        fontsize=14, fontweight="bold")

    plots = [
        (axes[0, 0], deltas, "Delta", "tab:blue"),
        (axes[0, 1], gammas, "Gamma", "tab:orange"),
        (axes[0, 2], vegas,  "Vega",  "tab:green"),
        (axes[1, 0], thetas, "Theta (per day)", "tab:red"),
        (axes[1, 1], rhos,   "Rho",   "tab:purple"),
        (axes[1, 2], speeds, "Speed", "tab:brown"),
    ]
    for ax, data, title, color in plots:
        ax.plot(S, data, color=color, linewidth=2)
        ax.axvline(K, color="gray", linestyle="--", alpha=0.5, label=f"Strike={K}")
        ax.set_title(title, fontsize=12)
        ax.set_xlabel("Spot Price")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig
