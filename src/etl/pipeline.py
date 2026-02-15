"""Main ELT pipeline orchestrator."""
import logging
from typing import List
from datetime import datetime
from src.etl.extractor import DataExtractor
from src.etl.loader import DataLoader
from src.ml.volatility import VolatilityMonitor
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ELTPipeline:
    """Orchestrates the ELT pipeline for market data."""
    
    def __init__(self):
        self.loader = DataLoader()
        self.volatility_monitor = VolatilityMonitor()
    
    def run_daily_pipeline(self):
        """Run the daily data pipeline for all configured symbols."""
        logger.info("=" * 50)
        logger.info("Starting daily ELT pipeline")
        logger.info(f"Timestamp: {datetime.now()}")
        logger.info("=" * 50)
        
        # Process Japanese stocks
        logger.info("\n--- Processing Japanese Stocks ---")
        self._process_symbols(config.JAPANESE_SYMBOLS, 'JAPANESE', data_type='daily')
        
        # Process Korean stocks
        logger.info("\n--- Processing Korean Stocks ---")
        self._process_symbols(config.KOREAN_SYMBOLS, 'KOREAN', data_type='daily')
        
        # Run volatility monitoring
        logger.info("\n--- Running Volatility Monitoring ---")
        all_symbols = config.JAPANESE_SYMBOLS + config.KOREAN_SYMBOLS
        self.volatility_monitor.monitor_all_symbols(all_symbols)
        
        logger.info("\n" + "=" * 50)
        logger.info("Daily ELT pipeline completed")
        logger.info("=" * 50)
    
    def run_intraday_pipeline(self, interval: str = "5m"):
        """
        Run the intraday data pipeline for active trading symbols.
        
        Args:
            interval: Data interval (e.g., '5m', '15m', '1h')
        """
        logger.info("=" * 50)
        logger.info(f"Starting intraday ELT pipeline (interval: {interval})")
        logger.info(f"Timestamp: {datetime.now()}")
        logger.info("=" * 50)
        
        # Process Korean stocks (active trading)
        logger.info("\n--- Processing Korean Stocks (Intraday) ---")
        self._process_symbols(config.KOREAN_SYMBOLS, 'KOREAN', data_type='intraday', interval=interval)
        
        logger.info("\n" + "=" * 50)
        logger.info("Intraday ELT pipeline completed")
        logger.info("=" * 50)
    
    def _process_symbols(self, symbols: List[str], exchange: str, data_type: str = 'daily', interval: str = '5m'):
        """
        Process a list of symbols.
        
        Args:
            symbols: List of stock symbols
            exchange: Exchange type ('JAPANESE' or 'KOREAN')
            data_type: Type of data to extract ('daily' or 'intraday')
            interval: Interval for intraday data
        """
        extractor = DataExtractor(symbols)
        
        for symbol in symbols:
            try:
                # Extract and load stock info
                logger.info(f"Processing {symbol}...")
                stock_info = extractor.get_stock_info(symbol)
                if stock_info:
                    self.loader.load_stock_info(stock_info, exchange)
                
                # Extract and load price data
                if data_type == 'daily':
                    df = extractor.get_daily_data(symbol)
                    if df is not None and not df.empty:
                        self.loader.load_daily_data(df)
                        logger.info(f"  ✓ Loaded {len(df)} daily records for {symbol}")
                else:  # intraday
                    df = extractor.get_intraday_data(symbol, interval=interval)
                    if df is not None and not df.empty:
                        self.loader.load_intraday_data(df)
                        logger.info(f"  ✓ Loaded {len(df)} intraday records for {symbol}")
                
            except Exception as e:
                logger.error(f"  ✗ Failed to process {symbol}: {e}")
                continue


def main():
    """Main entry point for the ELT pipeline."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Market Analysis ELT Pipeline')
    parser.add_argument(
        '--mode',
        choices=['daily', 'intraday', 'both'],
        default='daily',
        help='Pipeline mode: daily, intraday, or both'
    )
    parser.add_argument(
        '--interval',
        default='5m',
        help='Intraday data interval (e.g., 5m, 15m, 1h)'
    )
    
    args = parser.parse_args()
    
    pipeline = ELTPipeline()
    
    if args.mode == 'daily':
        pipeline.run_daily_pipeline()
    elif args.mode == 'intraday':
        pipeline.run_intraday_pipeline(interval=args.interval)
    else:  # both
        pipeline.run_daily_pipeline()
        pipeline.run_intraday_pipeline(interval=args.interval)


if __name__ == '__main__':
    main()
