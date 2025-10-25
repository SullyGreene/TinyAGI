# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/tools/yfinance_tool.py

import logging
import yfinance as yf
from .base_tool import BaseTool

logger = logging.getLogger(__name__)

class YFinanceTool(BaseTool):
    def __init__(self, config):
        super().__init__(config)
        self.name = "YFinanceTool"
        self.description = "Fetches financial data from Yahoo Finance."

    def execute(self, ticker: str, period: str = "1mo"):
        """
        Fetches historical market data for a given ticker.

        :param ticker: The stock ticker symbol (e.g., 'GC=F' for Gold).
        :param period: The period for which to fetch data (e.g., '1d', '5d', '1mo', '3mo', '6mo', '1y').
        :return: A summary of the historical data or an error message.
        """
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            if hist.empty:
                return f"No data found for ticker {ticker} for the period {period}."
            return hist.describe().to_string()
        except Exception as e:
            logger.error(f"Error fetching data for ticker {ticker}: {e}")
            return f"An error occurred while fetching data for {ticker}."