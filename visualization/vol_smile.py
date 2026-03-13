import numpy as np
import matplotlib.pyplot as plt


def plot_vol_smile(df, spot, expiry_label="", save_path=None):
    df_clean = df.dropna(subset=["impliedVol"]).copy()
    df_clean = df_clean[df_clean["impliedVol"] > 0.01]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.scatter(df_clean["strike"], df_clean["impliedVol"] * 100,
                s=30, alpha=0.7, color="tab:blue", edgecolors="navy", linewidth=0.5)
    ax1.axvline(spot, color="red", linestyle="--", alpha=0.6, label=f"Spot = {spot:.2f}")
    ax1.set_xlabel("Strike Price")
    ax1.set_ylabel("Implied Volatility (%)")
    ax1.set_title(f"IV vs Strike\n{expiry_label}")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.scatter(df_clean["moneyness"], df_clean["impliedVol"] * 100,
                s=30, alpha=0.7, color="tab:green", edgecolors="darkgreen", linewidth=0.5)
    ax2.axvline(1.0, color="red", linestyle="--", alpha=0.6, label="ATM (K/S = 1)")
    ax2.set_xlabel("Moneyness (K / S)")
    ax2.set_ylabel("Implied Volatility (%)")
    ax2.set_title(f"IV vs Moneyness\n{expiry_label}")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_vol_smile_calls_puts(calls_df, puts_df, spot, expiry_label="", save_path=None):
    fig, ax = plt.subplots(figsize=(10, 6))
    for df, label, color in [(calls_df, "Calls", "tab:blue"), (puts_df, "Puts", "tab:red")]:
        dc = df.dropna(subset=["impliedVol"])
        dc = dc[dc["impliedVol"] > 0.01]
        ax.scatter(dc["strike"], dc["impliedVol"] * 100, s=30, alpha=0.6,
                   color=color, label=label, edgecolors="black", linewidth=0.3)
    ax.axvline(spot, color="gray", linestyle="--", alpha=0.6, label=f"Spot = {spot:.2f}")
    ax.set_xlabel("Strike Price")
    ax.set_ylabel("Implied Volatility (%)")
    ax.set_title(f"Calls vs Puts — Implied Volatility\n{expiry_label}", fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig
