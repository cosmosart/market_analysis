"""Data extraction module using yfinance API."""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataExtractor:
    """Extracts stock data from yfinance API."""
    
    def __init__(self, symbols: List[str]):
        """
        Initialize extractor with stock symbols.
        
        Args:
            symbols: List of stock symbols (e.g., ['7203.T', '005930.KS'])
        """
        self.symbols = symbols
    
    def get_stock_info(self, symbol: str) -> Optional[Dict]:
        """
        Get stock information.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with stock info or None if failed
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'company_name': info.get('longName', ''),
                'sector': info.get('sector', ''),
                'currency': info.get('currency', '')
            }
        except Exception as e:
            logger.error(f"Failed to get info for {symbol}: {e}")
            return None
    
    def get_daily_data(self, symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """
        Get daily stock data.
        
        Args:
            symbol: Stock symbol
            period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            DataFrame with daily data or None if failed
        """
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)
            
            if df.empty:
                logger.warning(f"No data available for {symbol}")
                return None
            
            df.reset_index(inplace=True)
            df['symbol'] = symbol
            
            # Rename columns to match database schema
            df = df.rename(columns={
                'Date': 'date',
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })
            
            # Calculate adjusted close if not available
            if 'Adj Close' in df.columns:
                df = df.rename(columns={'Adj Close': 'adj_close'})
            else:
                df['adj_close'] = df['close']
            
            # Select relevant columns
            df = df[['symbol', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']]
            
            return df
        except Exception as e:
            logger.error(f"Failed to get daily data for {symbol}: {e}")
            return None
    
    def get_intraday_data(self, symbol: str, interval: str = "5m", period: str = "1d") -> Optional[pd.DataFrame]:
        """
        Get intraday stock data.
        
        Args:
            symbol: Stock symbol
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
            period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            DataFrame with intraday data or None if failed
        """
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            
            if df.empty:
                logger.warning(f"No intraday data available for {symbol}")
                return None
            
            df.reset_index(inplace=True)
            df['symbol'] = symbol
            
            # Rename columns to match database schema
            df = df.rename(columns={
                'Datetime': 'timestamp',
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })
            
            # Select relevant columns
            df = df[['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume']]
            
            return df
        except Exception as e:
            logger.error(f"Failed to get intraday data for {symbol}: {e}")
            return None
    
    def extract_all_daily_data(self) -> pd.DataFrame:
        """
        Extract daily data for all symbols.
        
        Returns:
            Combined DataFrame with all daily data
        """
        all_data = []
        
        for symbol in self.symbols:
            logger.info(f"Extracting daily data for {symbol}")
            df = self.get_daily_data(symbol)
            if df is not None:
                all_data.append(df)
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        else:
            logger.warning("No daily data extracted")
            return pd.DataFrame()
    
    def extract_all_intraday_data(self, interval: str = "5m") -> pd.DataFrame:
        """
        Extract intraday data for all symbols.
        
        Args:
            interval: Data interval
            
        Returns:
            Combined DataFrame with all intraday data
        """
        all_data = []
        
        for symbol in self.symbols:
            logger.info(f"Extracting intraday data for {symbol}")
            df = self.get_intraday_data(symbol, interval=interval)
            if df is not None:
                all_data.append(df)
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        else:
            logger.warning("No intraday data extracted")
            return pd.DataFrame()
