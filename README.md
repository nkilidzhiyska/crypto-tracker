
# crypto-tracker
=======
## Crypto Tracker

This project tracks cryptocurrency prices using the **CoinGecko API**.  
It has two parts:
1. **Command Line Script (`crypto_tracker.py`)** → fetches prices for multiple coins, compares today vs. one week ago, saves results to CSV, and generates a bar chart.
2. **Streamlit Dashboard (`app.py`)** → interactive web app to view historical price charts and latest values.

---

## Features

- Tracks major cryptocurrencies:
  - Bitcoin, Ethereum, Cardano, Dogecoin, XRP, Solana, Polkadot, Litecoin, TRON
- Compares **current vs. one week ago** prices
- Prints a formatted **table** in the terminal
- Exports results to `crypto_prices.csv`
- Generates a bar chart (`crypto_changes.png`) of percentage changes
- Interactive **Streamlit dashboard** with:
  - Dropdown to select a coin
  - Timeframe options (7 days, 30 days, 365 days)
  - Live line chart of prices
  - Current price displayed as a metric

---

## Installation

Clone this repository:

```bash
git clone https://github.com/YOUR-USERNAME/crypto-tracker.git
cd crypto-tracker
>>>>>>> 37c9d7b (Work in progress before rebase)
