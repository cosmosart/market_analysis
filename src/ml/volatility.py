"""Machine Learning module for volatility monitoring."""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple
import logging
from datetime import datetime
from src.database.connection import db
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VolatilityMonitor:
    """ML-based volatility monitoring for price movements."""
    
    def __init__(self, window: int = None, threshold: float = None):
        """
        Initialize volatility monitor.
        
        Args:
            window: Rolling window size for volatility calculation
            threshold: Threshold for high volatility alerts
        """
        self.window = window or config.VOLATILITY_WINDOW
        self.threshold = threshold or config.VOLATILITY_THRESHOLD
        self.scaler = StandardScaler()
    
    def calculate_returns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate daily returns from price data.
        
        Args:
            df: DataFrame with price data
            
        Returns:
            DataFrame with calculated returns
        """
        df = df.copy()
        df['returns'] = df['close'].pct_change()
        return df
    
    def calculate_volatility(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate rolling volatility (standard deviation of returns).
        
        Args:
            df: DataFrame with returns data
            
        Returns:
            DataFrame with volatility scores
        """
        df = df.copy()
        
        # Calculate returns if not already present
        if 'returns' not in df.columns:
            df = self.calculate_returns(df)
        
        # Calculate rolling volatility
        df['volatility'] = df['returns'].rolling(window=self.window).std()
        
        # Calculate percentile ranking for contextualization
        df['volatility_percentile'] = df['volatility'].rank(pct=True)
        
        return df
    
    def detect_volatility_alerts(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect high volatility periods.
        
        Args:
            df: DataFrame with volatility data
            
        Returns:
            DataFrame with volatility alerts
        """
        df = df.copy()
        
        # Ensure volatility is calculated
        if 'volatility' not in df.columns:
            df = self.calculate_volatility(df)
        
        # Remove NaN values
        df = df.dropna(subset=['volatility'])
        
        # Classify volatility levels
        def classify_volatility(vol):
            if vol > self.threshold * 2:
                return 'HIGH'
            elif vol > self.threshold:
                return 'MEDIUM'
            else:
                return 'LOW'
        
        df['alert_type'] = df['volatility'].apply(classify_volatility)
        
        # Filter for medium and high alerts
        alerts = df[df['alert_type'].isin(['MEDIUM', 'HIGH'])].copy()
        
        return alerts
    
    def analyze_symbol(self, symbol: str, days: int = 100) -> Dict:
        """
        Analyze volatility for a specific symbol.
        
        Args:
            symbol: Stock symbol
            days: Number of days to analyze
            
        Returns:
            Dictionary with volatility analysis results
        """
        try:
            # Fetch data from database
            query = """
                SELECT symbol, date, close 
                FROM daily_data 
                WHERE symbol = %s 
                ORDER BY date DESC 
                LIMIT %s
            """
            results = db.execute_query(query, (symbol, days))
            
            if not results:
                logger.warning(f"No data available for {symbol}")
                return {}
            
            df = pd.DataFrame(results)
            df = df.sort_values('date')
            
            # Calculate volatility
            df = self.calculate_volatility(df)
            
            # Detect alerts
            alerts = self.detect_volatility_alerts(df)
            
            # Get latest metrics
            latest = df.iloc[-1]
            
            analysis = {
                'symbol': symbol,
                'current_price': float(latest['close']),
                'current_volatility': float(latest.get('volatility', 0)),
                'volatility_percentile': float(latest.get('volatility_percentile', 0)),
                'alert_type': alerts.iloc[-1]['alert_type'] if not alerts.empty else 'LOW',
                'recent_alerts': len(alerts),
                'analysis_date': datetime.now().date()
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze volatility for {symbol}: {e}")
            return {}
    
    def save_volatility_alert(self, alert_data: Dict) -> bool:
        """
        Save volatility alert to database.
        
        Args:
            alert_data: Dictionary with alert information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            query = """
                INSERT INTO volatility_alerts 
                (symbol, alert_date, volatility_score, price_at_alert, alert_type, message)
                VALUES (%(symbol)s, %(alert_date)s, %(volatility_score)s, 
                        %(price_at_alert)s, %(alert_type)s, %(message)s)
                ON CONFLICT (symbol, alert_date) 
                DO UPDATE SET 
                    volatility_score = EXCLUDED.volatility_score,
                    price_at_alert = EXCLUDED.price_at_alert,
                    alert_type = EXCLUDED.alert_type,
                    message = EXCLUDED.message
            """
            
            db.execute_query(query, alert_data, fetch=False)
            logger.info(f"Saved volatility alert for {alert_data['symbol']}")
            return True
        except Exception as e:
            logger.error(f"Failed to save volatility alert: {e}")
            return False
    
    def monitor_all_symbols(self, symbols: List[str]) -> List[Dict]:
        """
        Monitor volatility for all symbols and save alerts.
        
        Args:
            symbols: List of stock symbols to monitor
            
        Returns:
            List of analysis results
        """
        results = []
        
        for symbol in symbols:
            logger.info(f"Monitoring volatility for {symbol}")
            analysis = self.analyze_symbol(symbol)
            
            if analysis and analysis.get('alert_type') in ['MEDIUM', 'HIGH']:
                # Save alert to database
                alert_data = {
                    'symbol': analysis['symbol'],
                    'alert_date': analysis['analysis_date'],
                    'volatility_score': analysis['current_volatility'],
                    'price_at_alert': analysis['current_price'],
                    'alert_type': analysis['alert_type'],
                    'message': f"Volatility at {analysis['volatility_percentile']:.1%} percentile"
                }
                self.save_volatility_alert(alert_data)
            
            results.append(analysis)
        
        return results
    
    def get_recent_alerts(self, days: int = 7) -> pd.DataFrame:
        """
        Get recent volatility alerts from database.
        
        Args:
            days: Number of days to look back
            
        Returns:
            DataFrame with recent alerts
        """
        try:
            query = """
                SELECT va.*, si.company_name, si.exchange
                FROM volatility_alerts va
                JOIN stock_info si ON va.symbol = si.symbol
                WHERE va.alert_date >= CURRENT_DATE - INTERVAL '1 day' * %s
                ORDER BY va.alert_date DESC, va.volatility_score DESC
            """
            results = db.execute_query(query, (days,))
            return pd.DataFrame(results)
        except Exception as e:
            logger.error(f"Failed to retrieve recent alerts: {e}")
            return pd.DataFrame()
