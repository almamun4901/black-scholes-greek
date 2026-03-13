import argparse
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from wilmott_replication.chapter8_sheet import run_full_replication
from visualization.greeks_plotter import plot_greeks_vs_strike, plot_greeks_vs_spot


def main():
    parser = argparse.ArgumentParser(description="Black-Scholes & Greeks")
    parser.add_argument("--ticker", type=str, default="SPY", help="Ticker symbol")
    parser.add_argument("--expiry", type=int, default=0, help="Expiry index (0=nearest)")
    parser.add_argument("--output", type=str, default="output", help="Output directory")
    parser.add_argument("--skip-live", action="store_true", help="Skip live data fetch")
    args = parser.parse_args()
    os.makedirs(args.output, exist_ok=True)

    # Step 1: Wilmott replication
    print("\n" + "=" * 65)
    print("STEP 1: Wilmott Chapter 8 Replication")
    print("=" * 65)
    run_full_replication()

    # Step 2: Theoretical Greeks plots 
    print("\nSTEP 2: Generating theoretical Greeks plots...")
    S0, K0, T0, r0, sigma0, q0 = 100, 100, 1.0, 0.05, 0.20, 0.0
    K_range = np.linspace(70, 130, 200)
    S_range = np.linspace(70, 130, 200)

    plot_greeks_vs_strike(S0, K_range, T0, r0, sigma0, q0, "call",
                          save_path=f"{args.output}/greeks_vs_strike_call.png")
    plot_greeks_vs_strike(S0, K_range, T0, r0, sigma0, q0, "put",
                          save_path=f"{args.output}/greeks_vs_strike_put.png")
    plot_greeks_vs_spot(S_range, K0, T0, r0, sigma0, q0, "call",
                        save_path=f"{args.output}/greeks_vs_spot_call.png")
    print("  \u2713 Theoretical plots saved.")

    if args.skip_live:
        print("\n[Skipping live data — done.]")
        plt.close("all")
        return

    # Step 3: Fetch live data
    print(f"\nSTEP 3: Fetching live options data for {args.ticker}...")
    try:
        from data.fetcher import get_options_chain
        from data.processor import full_pipeline
        from visualization.vol_smile import plot_vol_smile, plot_vol_smile_calls_puts

        chain = get_options_chain(args.ticker, args.expiry)
        spot, r = chain["spot"], chain["r"]
        expiry_label = f"{args.ticker} | Expiry: {chain['expiry']} | Spot: ${spot:.2f}"
        print(f"  Spot: ${spot:.2f}  |  r: {r:.2%}  |  Expiry: {chain['expiry']}")

        # Step 4: Process & enrich
        print("\nSTEP 4: Computing implied vols & Greeks...")
        calls = full_pipeline(chain["calls"], spot, r, "call")
        puts = full_pipeline(chain["puts"], spot, r, "put")
        print(f"  \u2713 Calls: {len(calls)} strikes  |  Puts: {len(puts)} strikes")

        calls.to_csv(f"{args.output}/{args.ticker}_calls_enriched.csv", index=False)
        puts.to_csv(f"{args.output}/{args.ticker}_puts_enriched.csv", index=False)

        # Step 5: Market plots
        print("\nSTEP 5: Generating market-data plots...")
        plot_vol_smile(calls, spot, f"Calls | {expiry_label}",
                       save_path=f"{args.output}/vol_smile_calls.png")
        plot_vol_smile(puts, spot, f"Puts | {expiry_label}",
                       save_path=f"{args.output}/vol_smile_puts.png")
        plot_vol_smile_calls_puts(calls, puts, spot, expiry_label,
                                  save_path=f"{args.output}/vol_smile_overlay.png")
        print("  \u2713 All plots saved.")

    except Exception as e:
        print(f"  \u2717 Failed: {e}")
        print("  Run with --skip-live for theoretical plots only.")

    plt.close("all")
    print(f"\n{'=' * 65}")
    print(f"DONE — outputs in ./{args.output}/")
    print(f"{'=' * 65}")


if __name__ == "__main__":
    main()
