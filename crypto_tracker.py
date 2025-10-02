# crypto_tracker.py 
# This script compares crypto prices from today vs. one week ago.
# It prints a table, saves results to CSV, and generates a bar chart.
# Optimized to reduce API calls by fetching market data in ranges.

from pycoingecko import CoinGeckoAPI   # CoinGecko API client
from datetime import datetime, timedelta, UTC   # for handling dates and times
import pandas as pd    # for tables and data handling
import matplotlib.pyplot as plt   # for chart plotting
import os   # for saving files

# Create an API client object
cg = CoinGeckoAPI()

# Cryptocurrencies we want to track (using CoinGecko IDs)
coins = [
    "bitcoin", "ethereum", "cardano", "dogecoin", "ripple",
    "solana", "polkadot", "litecoin", "tron"
]

# Mapping IDs to nicer display names for output
name_map = {
    "bitcoin": "Bitcoin",
    "ethereum": "Ethereum",
    "cardano": "Cardano",
    "dogecoin": "Dogecoin",
    "ripple": "XRP",
    "solana": "Solana",
    "polkadot": "Polkadot",
    "litecoin": "Litecoin",
    "tron": "TRON"
}

def fetch_weekly_comparison():
    # Get the most recent prices for all coins
    print("🔄 Fetching current prices...")
    now_prices = cg.get_price(ids=",".join(coins), vs_currencies="usd")

    # Calculate UNIX timestamps for "one week ago" and "now"
    one_week_ago = datetime.now(UTC) - timedelta(days=7)
    start = int(one_week_ago.timestamp())
    end = int(datetime.now(UTC).timestamp())

    # Dictionary to hold historical prices from a week ago
    historical = {}
    print("🔄 Fetching historical data (optimized)...")
    for coin in coins:
        try:
            # Pull price data for the last 7 days in a single request
            chart = cg.get_coin_market_chart_range_by_id(
                id=coin, vs_currency="usd",
                from_timestamp=start, to_timestamp=end
            )
            prices = chart["prices"]  # each element looks like [timestamp, price]

            # Approximate "1 week ago" price by taking the first value returned
            past_price = prices[0][1] if prices else None
            historical[coin] = past_price
            print(f"✅ {coin}: {past_price}")
        except Exception as e:
            # If the API fails, record None instead of stopping the program
            print(f"❌ Error {coin}: {e}")
            historical[coin] = None

    # Build a table with coin name, old price, new price, and percent change
    rows = []
    for coin in coins:
        name = name_map.get(coin, coin.capitalize())
        past = historical.get(coin)
        curr = now_prices.get(coin, {}).get("usd")
        # Compute percent change if both prices exist
        change = (curr - past) / past * 100 if past and curr else None
        rows.append([name, past, curr, change])

    # Create a pandas DataFrame for nicer formatting
    df = pd.DataFrame(rows, columns=[
        "Coin",
        "Price 1 Week Ago (USD)",
        "Current Price (USD)",
        "Change (%)"
    ])

    # Round values to make output easier to read
    df = df.round({
        "Price 1 Week Ago (USD)": 4,
        "Current Price (USD)": 4,
        "Change (%)": 2
    })

    # Print the table in the console
    print("\n📊 Weekly Comparison:\n")
    print(df.to_string(index=False))

    # Save the table as a CSV file
    df.to_csv("crypto_prices.csv", index=False)
    print("\n✅ Saved table to crypto_prices.csv")

    # Create and save a bar chart showing percent changes
    plt.figure(figsize=(10,6))
    plt.bar(df["Coin"], df["Change (%)"], color="skyblue", edgecolor="black")
    plt.axhline(0, color="black", linewidth=0.8)  # horizontal line at 0%
    plt.title("Crypto Price Change Over the Last Week")
    plt.ylabel("Percent Change (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("crypto_changes.png")
    print("✅ Saved chart to crypto_changes.png")

    return df

if __name__ == "__main__":
    fetch_weekly_comparison()
