# Black-Scholes Options Pricing & Greeks Dashboard

A Python recreation of the Black Scholes and Greeks spreadsheet from
*Paul Wilmott Introduces Quantitative Finance* (2nd ed.).


1. **Contents** — Black Scholes Greek Coded Simulation
2. **Spreadsheet functions / VB functions** — Reference for Excel vs VB function syntax
3. **Greeks** — Black-Scholes pricing and all Greeks for:
   - Vanilla European Call & Put (Value, Delta, Gamma, Theta, Speed, Vega, Rho, Rho D)
   - Binary (Digital) Call & Put (Value, Delta, Gamma, Theta, Speed, Vega, Rho, Rho D)
   - With continuous dividend yield support
4. **Implied Volatility** — Newton-Raphson solver backing out market vol from 5 call option prices


## Novel Contribution

1. Fetching **real options data** via `yfinance` for any ticker
2. Computing **implied volatilities** across strikes and plotting the **volatility smile**
3. Visualizing all Greeks as functions of strike and spot price
4. Providing an **Streamlit dashboard** for simulation of different parameters

## Project Structure

```
wilmott-project/
├── equations/
│   ├── black_scholes.py      # BS vanilla + binary pricing (with div yield)
│   ├── greeks.py              # all the greeks
│   └── implied_vol.py         # Newton-Raphson IV solver
├── data/
│   ├── fetcher.py             # yfinance options chain data
│   └── processor.py           # Data cleaning
├── visualization/
│   ├── greeks_plotter.py      # Greeks vs strike/spot multi-panel plots
│   └── vol_smile.py           # Implied volatility smile charts
├── wilmott_replication/
│   └── chapter8_sheet.py      # Wilmott Sheet replication
├── dashboard.py               # Streamlit interactive dashboard
├── main.py                    # CLI entry point
├── requirements.txt
└── README.md
```

## Setup & Usage

```bash
# create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# CLI pipeline
python main.py --ticker AAPL

# Theoretical plots only
python main.py --skip-live

# Interactive dashboard
streamlit run dashboard.py
```

## online demo
[Dashboard](https://black-scholes-greek-dashboard.streamlit.app/)


## Citations

- Model, implementation, and interpretation was done by @mdalmamun
- Streamlit Dashboard was completed by @mdalmamun with assistance from Claude AI
- Project Structure and debugging was done by @mdalmamun with assistance from ChatGPT
- Equation references are from the book *Paul Wilmott Introduces Quantitative Finance* (2nd ed.)
