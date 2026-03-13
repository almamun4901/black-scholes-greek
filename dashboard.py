# streamlit dashboard

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from equations.black_scholes import call_price, put_price, binary_call_price, binary_put_price
from equations.greeks import all_vanilla_greeks, all_binary_greeks
from equations.implied_vol import implied_vol
from visualization.greeks_plotter import plot_greeks_vs_strike, plot_greeks_vs_spot

st.set_page_config(page_title="BS Greeks Dashboard", layout="wide")
st.title("Black-Scholes & Greeks")

# default parameters
st.sidebar.header("Model Parameters")
S = st.sidebar.number_input("Asset Price (S)", value=100.0, step=1.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0, step=1.0)
T = st.sidebar.slider("Expiry (years)", 0.01, 3.0, 1.0, 0.01)
sigma = st.sidebar.slider("Volatility (\u03c3)", 0.05, 1.0, 0.20, 0.01, format="%.2f")
r = st.sidebar.slider("Interest Rate (r)", 0.0, 0.15, 0.05, 0.005, format="%.3f")
q = st.sidebar.slider("Dividend Yield (q)", 0.0, 0.10, 0.0, 0.005, format="%.3f")

tab1, tab2, tab3, tab4 = st.tabs([
    "Greeks (Wilmott Sheet)", "Greeks Plots",
    "Implied Volatility", "Live Data"
])

# Tab 1: Greeks
with tab1:
    col_left, col_mid, col_right = st.columns([1, 2, 2])
    with col_left:
        st.subheader("Inputs")
        st.write(f"**Asset:** {S}")
        st.write(f"**Volatility:** {sigma}")
        st.write(f"**Div. Yield:** {q}")
        st.write(f"**Int. rate:** {r}")
        st.write(f"**Strike:** {K}")
        st.write(f"**Expiry:** {T}")

    vc = all_vanilla_greeks(S, K, T, r, sigma, q, "call")
    vp = all_vanilla_greeks(S, K, T, r, sigma, q, "put")
    bc = all_binary_greeks(S, K, T, r, sigma, q, "call")
    bp = all_binary_greeks(S, K, T, r, sigma, q, "put")

    with col_mid:
        st.subheader("CALL")
        for name, val in vc.items():
            st.metric(name, f"{val:.6f}")
        st.markdown("---")
        st.subheader("BINARY CALL")
        for name, val in bc.items():
            st.metric(name, f"{val:.6f}")

    with col_right:
        st.subheader("PUT")
        for name, val in vp.items():
            st.metric(name, f"{val:.6f}")
        st.markdown("---")
        st.subheader("BINARY PUT")
        for name, val in bp.items():
            st.metric(name, f"{val:.6f}")

# Tab 2: Greeks plots
with tab2:
    st.subheader("Greeks vs Strike")
    K_range = np.linspace(S * 0.7, S * 1.3, 200)
    opt = st.radio("Option type", ["call", "put"], key="plot_type", horizontal=True)
    fig1 = plot_greeks_vs_strike(S, K_range, T, r, sigma, q, opt)
    st.pyplot(fig1)
    plt.close(fig1)

    st.subheader("Greeks vs Spot")
    S_range = np.linspace(K * 0.7, K * 1.3, 200)
    fig2 = plot_greeks_vs_spot(S_range, K, T, r, sigma, q, opt)
    st.pyplot(fig2)
    plt.close(fig2)

# Tab 3: IV 
with tab3:
    st.subheader("Implied Volatility Solver")
    st.write("Enter market call prices to back out implied volatility")

    iv_r = st.number_input("Interest rate for IV", value=0.08, step=0.01, format="%.3f")
    iv_tol = st.number_input("Error tolerance", value=0.001, step=0.0001, format="%.4f")

    cols = st.columns(5)
    defaults_mkt = [18.6, 14.8, 11.5, 8.9, 7.0]
    defaults_K = [90.0, 95.0, 100.0, 105.0, 110.0]
    defaults_T = [1.0, 1.0, 1.0, 1.0, 1.0]

    mkts, Ks, Ts = [], [], []
    for i, col in enumerate(cols):
        with col:
            mkts.append(st.number_input(f"Mkt Price {i+1}", value=defaults_mkt[i], key=f"mkt{i}"))
            Ks.append(st.number_input(f"Strike {i+1}", value=defaults_K[i], key=f"K{i}"))
            Ts.append(st.number_input(f"Expiry {i+1}", value=defaults_T[i], key=f"T{i}"))

    if st.button("Compute Implied Volatilities"):
        ivs = []
        for mkt, strike, exp in zip(mkts, Ks, Ts):
            iv = implied_vol(mkt, S, strike, exp, iv_r, 0.0, "call", tol=iv_tol)
            ivs.append(iv)
        st.subheader("Results")
        for i in range(len(ivs)):
            st.write(f"K={Ks[i]:.0f}, Mkt={mkts[i]:.1f} → **IV = {ivs[i]:.6f}** ({ivs[i]*100:.2f}%)")

        # Plotting
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(Ks, [iv * 100 for iv in ivs], "o-", color="tab:blue", markersize=8)
        ax.set_xlabel("Strike")
        ax.set_ylabel("Implied Volatility (%)")
        ax.set_title("Implied Volatility Smile")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)

# Tab 4: Live data
with tab4:
    st.subheader("Fetch Real Options Data")
    ticker = st.text_input("Ticker", value="SPY")
    if st.button("Fetch & Analyze"):
        with st.spinner("Fetching..."):
            try:
                from data.fetcher import get_options_chain
                from data.processor import full_pipeline
                from visualization.vol_smile import plot_vol_smile_calls_puts

                chain = get_options_chain(ticker, 0)
                spot, rfr = chain["spot"], chain["r"]
                st.success(f"Spot: ${spot:.2f} | Rate: {rfr:.2%} | Expiry: {chain['expiry']}")

                calls = full_pipeline(chain["calls"], spot, rfr, "call")
                puts = full_pipeline(chain["puts"], spot, rfr, "put")

                fig = plot_vol_smile_calls_puts(calls, puts, spot,
                                                f"{ticker} | Expiry: {chain['expiry']}")
                st.pyplot(fig)
                plt.close(fig)

                st.subheader("Enriched Call Data")
                show_cols = [c for c in ["strike","mid","impliedVol","delta","gamma","vega","theta","speed","rho"]
                             if c in calls.columns]
                st.dataframe(calls[show_cols].head(20).round(6))
            except Exception as e:
                st.error(f"Error: {e}")
