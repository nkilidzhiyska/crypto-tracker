# app.py
# A simple Streamlit dashboard for visualizing cryptocurrency prices.
# Lets the user select a coin and timeframe, then displays a line chart
# of price history and shows the most recent price as a metric.

import streamlit as st   # Streamlit handles the web dashboard
import pandas as pd      # for handling the price data
from pycoingecko import CoinGeckoAPI   # to get data from CoinGecko API

# Create API client
cg = CoinGeckoAPI()

# Coins we want to include (display name → CoinGecko ID)
coins = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Cardano": "cardano",
    "Dogecoin": "dogecoin",
    "XRP": "ripple",   # CoinGecko uses "ripple" for XRP
    "Solana": "solana",
    "Polkadot": "polkadot",
    "Litecoin": "litecoin",
    "TRON": "tron",
    "Polygon": "polygon"
}

# Title of the dashboard
st.title("📊 Cryptocurrency Dashboard")
st.write("Track prices and view historical trends using data from CoinGecko.")

# Dropdown menu for selecting a cryptocurrency
choice = st.selectbox("Choose a cryptocurrency:", list(coins.keys()))

# Radio buttons for choosing timeframe
days = st.radio("Select timeframe:", ["7 Days", "30 Days", "365 Days"])
day_map = {"7 Days": 7, "30 Days": 30, "365 Days": 365}

# Fetch price history for the selected coin and timeframe
data = cg.get_coin_market_chart_by_id(
    id=coins[choice], vs_currency="usd", days=day_map[days]
)

# Convert to a DataFrame for easier plotting
df = pd.DataFrame(data["prices"], columns=["Timestamp", "Price"])
df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="ms")

# Show line chart in the dashboard
st.subheader(f"{choice} Price Chart - Last {days}")
st.line_chart(df.set_index("Timestamp")["Price"])

# Show the latest price as a metric widget
latest_price = df["Price"].iloc[-1]
st.metric(label=f"Current {choice} Price (USD)", value=f"${latest_price:,.2f}")
