"""Data loading module for PostgreSQL."""
import pandas as pd
from typing import List, Dict
import logging
from src.database.connection import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Loads extracted data into PostgreSQL database."""
    
    def __init__(self):
        self.db = db
    
    def load_stock_info(self, stock_info: Dict, exchange: str) -> bool:
        """
        Load stock information into database.
        
        Args:
            stock_info: Dictionary with stock info
            exchange: Exchange type ('JAPANESE' or 'KOREAN')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            query = """
                INSERT INTO stock_info (symbol, exchange, company_name, sector, currency)
                VALUES (%(symbol)s, %(exchange)s, %(company_name)s, %(sector)s, %(currency)s)
                ON CONFLICT (symbol) 
                DO UPDATE SET 
                    company_name = EXCLUDED.company_name,
                    sector = EXCLUDED.sector,
                    currency = EXCLUDED.currency,
                    updated_at = CURRENT_TIMESTAMP
            """
            stock_info['exchange'] = exchange
            self.db.execute_query(query, stock_info, fetch=False)
            logger.info(f"Loaded stock info for {stock_info['symbol']}")
            return True
        except Exception as e:
            logger.error(f"Failed to load stock info: {e}")
            return False
    
    def load_daily_data(self, df: pd.DataFrame) -> int:
        """
        Load daily data into database.
        
        Args:
            df: DataFrame with daily data
            
        Returns:
            Number of rows loaded
        """
        if df.empty:
            logger.warning("No daily data to load")
            return 0
        
        try:
            query = """
                INSERT INTO daily_data (symbol, date, open, high, low, close, adj_close, volume)
                VALUES (%(symbol)s, %(date)s, %(open)s, %(high)s, %(low)s, %(close)s, %(adj_close)s, %(volume)s)
                ON CONFLICT (symbol, date) 
                DO UPDATE SET 
                    open = EXCLUDED.open,
                    high = EXCLUDED.high,
                    low = EXCLUDED.low,
                    close = EXCLUDED.close,
                    adj_close = EXCLUDED.adj_close,
                    volume = EXCLUDED.volume
            """
            
            records = df.to_dict('records')
            self.db.execute_many(query, records)
            logger.info(f"Loaded {len(records)} daily data records")
            return len(records)
        except Exception as e:
            logger.error(f"Failed to load daily data: {e}")
            return 0
    
    def load_intraday_data(self, df: pd.DataFrame) -> int:
        """
        Load intraday data into database.
        
        Args:
            df: DataFrame with intraday data
            
        Returns:
            Number of rows loaded
        """
        if df.empty:
            logger.warning("No intraday data to load")
            return 0
        
        try:
            query = """
                INSERT INTO intraday_data (symbol, timestamp, open, high, low, close, volume)
                VALUES (%(symbol)s, %(timestamp)s, %(open)s, %(high)s, %(low)s, %(close)s, %(volume)s)
                ON CONFLICT (symbol, timestamp) 
                DO UPDATE SET 
                    open = EXCLUDED.open,
                    high = EXCLUDED.high,
                    low = EXCLUDED.low,
                    close = EXCLUDED.close,
                    volume = EXCLUDED.volume
            """
            
            records = df.to_dict('records')
            self.db.execute_many(query, records)
            logger.info(f"Loaded {len(records)} intraday data records")
            return len(records)
        except Exception as e:
            logger.error(f"Failed to load intraday data: {e}")
            return 0
    
    def get_daily_data(self, symbol: str = None, limit: int = 100) -> pd.DataFrame:
        """
        Retrieve daily data from database.
        
        Args:
            symbol: Optional stock symbol filter
            limit: Number of records to retrieve
            
        Returns:
            DataFrame with daily data
        """
        try:
            if symbol:
                query = """
                    SELECT * FROM daily_data 
                    WHERE symbol = %s 
                    ORDER BY date DESC 
                    LIMIT %s
                """
                results = self.db.execute_query(query, (symbol, limit))
            else:
                query = """
                    SELECT * FROM daily_data 
                    ORDER BY date DESC, symbol 
                    LIMIT %s
                """
                results = self.db.execute_query(query, (limit,))
            
            return pd.DataFrame(results)
        except Exception as e:
            logger.error(f"Failed to retrieve daily data: {e}")
            return pd.DataFrame()
    
    def get_intraday_data(self, symbol: str = None, limit: int = 100) -> pd.DataFrame:
        """
        Retrieve intraday data from database.
        
        Args:
            symbol: Optional stock symbol filter
            limit: Number of records to retrieve
            
        Returns:
            DataFrame with intraday data
        """
        try:
            if symbol:
                query = """
                    SELECT * FROM intraday_data 
                    WHERE symbol = %s 
                    ORDER BY timestamp DESC 
                    LIMIT %s
                """
                results = self.db.execute_query(query, (symbol, limit))
            else:
                query = """
                    SELECT * FROM intraday_data 
                    ORDER BY timestamp DESC, symbol 
                    LIMIT %s
                """
                results = self.db.execute_query(query, (limit,))
            
            return pd.DataFrame(results)
        except Exception as e:
            logger.error(f"Failed to retrieve intraday data: {e}")
            return pd.DataFrame()
