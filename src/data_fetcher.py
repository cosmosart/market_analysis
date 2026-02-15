"""
Module for fetching stock market data from Yahoo Finance.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


class StockDataFetcher:
    """Class to fetch and manage stock market data."""
    
    def __init__(self, ticker: str):
        """
        Initialize the data fetcher with a stock ticker symbol.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        """
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(self.ticker)
        self.data = None
    
    def fetch_data(self, period: str = "2y", interval: str = "1d") -> pd.DataFrame:
        """
        Fetch historical stock data.
        
        Args:
            period: Time period to fetch (e.g., '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
            interval: Data interval (e.g., '1d', '1wk', '1mo')
        
        Returns:
            DataFrame containing stock data with OHLCV columns
        """
        try:
            self.data = self.stock.history(period=period, interval=interval)
            
            if self.data.empty:
                raise ValueError(f"No data found for ticker {self.ticker}")
            
            # Remove timezone information for consistency
            self.data.index = self.data.index.tz_localize(None)
            
            return self.data
        
        except Exception as e:
            raise Exception(f"Error fetching data for {self.ticker}: {str(e)}")
    
    def fetch_data_range(self, start_date: str, end_date: str, interval: str = "1d") -> pd.DataFrame:
        """
        Fetch historical stock data for a specific date range.
        
        Args:
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            interval: Data interval (e.g., '1d', '1wk', '1mo')
        
        Returns:
            DataFrame containing stock data
        """
        try:
            self.data = self.stock.history(start=start_date, end=end_date, interval=interval)
            
            if self.data.empty:
                raise ValueError(f"No data found for ticker {self.ticker}")
            
            # Remove timezone information for consistency
            self.data.index = self.data.index.tz_localize(None)
            
            return self.data
        
        except Exception as e:
            raise Exception(f"Error fetching data for {self.ticker}: {str(e)}")
    
    def get_stock_info(self) -> dict:
        """
        Get general information about the stock.
        
        Returns:
            Dictionary containing stock information
        """
        try:
            info = self.stock.info
            return {
                'symbol': info.get('symbol', self.ticker),
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'current_price': info.get('currentPrice', 'N/A')
            }
        except Exception as e:
            return {'symbol': self.ticker, 'error': str(e)}
    
    def save_data(self, filepath: str):
        """
        Save the fetched data to a CSV file.
        
        Args:
            filepath: Path to save the CSV file
        """
        if self.data is None or self.data.empty:
            raise ValueError("No data to save. Fetch data first.")
        
        self.data.to_csv(filepath)
    
    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Load stock data from a CSV file.
        
        Args:
            filepath: Path to the CSV file
        
        Returns:
            DataFrame containing stock data
        """
        self.data = pd.read_csv(filepath, index_col=0, parse_dates=True)
        return self.data
