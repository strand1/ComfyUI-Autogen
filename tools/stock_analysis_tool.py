tool_name = "stock_analysis_tool"

import os
import asyncio
from datetime import datetime, timedelta
import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from pytz import timezone  # type: ignore


async def execute(ticker: str, save_dir: str = "coding") -> dict:  # type: ignore[type-arg]
    """
    Analyze stock data for a given ticker and generate metrics and a plot.

    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL").
        save_dir (str): Directory to save the plot image.

    Returns:
        dict: Dictionary containing stock metrics and plot file path.
    """
    try:
        # Fetch historical data (1 year)
        stock = yf.Ticker(ticker)
        end_date = datetime.now(timezone("UTC"))
        start_date = end_date - timedelta(days=365)
        hist = await asyncio.to_thread(stock.history, start=start_date, end=end_date)

        if hist.empty:
            return {"error": f"No historical data available for ticker {ticker}."}

        # Metrics calculation
        current_price = stock.info.get("currentPrice", hist["Close"].iloc[-1])
        year_high = stock.info.get("fiftyTwoWeekHigh", hist["High"].max())
        year_low = stock.info.get("fiftyTwoWeekLow", hist["Low"].min())
        ma_50 = hist["Close"].rolling(window=50).mean().iloc[-1]
        ma_200 = hist["Close"].rolling(window=200).mean().iloc[-1]
        ytd_start = datetime(end_date.year, 1, 1, tzinfo=timezone("UTC"))
        ytd_data = hist.loc[ytd_start:]
        price_change = ytd_data["Close"].iloc[-1] - ytd_data["Close"].iloc[0] if not ytd_data.empty else np.nan
        percent_change = (price_change / ytd_data["Close"].iloc[0]) * 100 if not ytd_data.empty else np.nan

        trend = (
            "Upward" if ma_50 > ma_200 else
            "Downward" if ma_50 < ma_200 else
            "Neutral"
        ) if pd.notna(ma_50) and pd.notna(ma_200) else "Insufficient data for trend analysis"

        daily_returns = hist["Close"].pct_change().dropna()
        volatility = daily_returns.std() * np.sqrt(252)  # Annualized

        # Convert numpy types for JSON serialization
        result = {
            "ticker": ticker,
            "current_price": current_price,
            "52_week_high": year_high,
            "52_week_low": year_low,
            "50_day_ma": ma_50,
            "200_day_ma": ma_200,
            "ytd_price_change": price_change,
            "ytd_percent_change": percent_change,
            "trend": trend,
            "volatility": volatility.item() if isinstance(volatility, np.generic) else volatility,
        }

        # Generate and save plot
        os.makedirs(save_dir, exist_ok=True)
        plot_file_path = os.path.join(save_dir, f"{ticker}_stockprice.png")

        plt.figure(figsize=(12, 6))
        plt.plot(hist.index, hist["Close"], label="Close Price", color="blue")
        plt.plot(hist.index, hist["Close"].rolling(window=50).mean(), label="50-day MA", color="orange")
        plt.plot(hist.index, hist["Close"].rolling(window=200).mean(), label="200-day MA", color="green")
        plt.title(f"{ticker} Stock Price Analysis (Past Year)")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.legend()
        plt.grid(True)
        plt.savefig(plot_file_path)
        plt.close()

        result["plot_file_path"] = plot_file_path
        return result

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
