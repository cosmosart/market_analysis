"""Sample data generation and testing script."""
import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from src.database.connection import db
from src.etl.extractor import DataExtractor
from src.etl.loader import DataLoader
from src.ml.volatility import VolatilityMonitor
import config

def test_database_connection():
    """Test database connection."""
    print("\n=== Testing Database Connection ===")
    try:
        result = db.test_connection()
        if result:
            print("✓ Database connection successful")
            return True
        else:
            print("✗ Database connection failed")
            return False
    except Exception as e:
        print(f"✗ Database connection error: {e}")
        return False


def test_data_extraction():
    """Test data extraction from yfinance."""
    print("\n=== Testing Data Extraction ===")
    try:
        # Test with a single Japanese stock
        test_symbol = "7203.T"  # Toyota
        extractor = DataExtractor([test_symbol])
        
        # Test stock info
        print(f"Extracting info for {test_symbol}...")
        info = extractor.get_stock_info(test_symbol)
        if info:
            print(f"✓ Stock info: {info.get('company_name', 'N/A')}")
        
        # Test daily data
        print(f"Extracting daily data for {test_symbol}...")
        df = extractor.get_daily_data(test_symbol, period="5d")
        if df is not None and not df.empty:
            print(f"✓ Extracted {len(df)} days of data")
            print(f"  Latest close price: {df['close'].iloc[-1]:.2f}")
            return True
        else:
            print("✗ No data extracted")
            return False
    except Exception as e:
        print(f"✗ Data extraction error: {e}")
        return False


def generate_sample_data():
    """Generate sample data for testing without database."""
    print("\n=== Generating Sample Data ===")
    try:
        # Generate sample daily data
        dates = pd.date_range(end=datetime.now(), periods=100, freq='D')
        
        sample_data = []
        for symbol in ['TEST1.T', 'TEST2.KS']:
            base_price = 1000 if '.T' in symbol else 50000
            prices = base_price + np.random.randn(100).cumsum() * 10
            
            df = pd.DataFrame({
                'symbol': symbol,
                'date': dates,
                'open': prices + np.random.randn(100),
                'high': prices + abs(np.random.randn(100)) * 2,
                'low': prices - abs(np.random.randn(100)) * 2,
                'close': prices,
                'adj_close': prices,
                'volume': np.random.randint(1000000, 10000000, 100)
            })
            sample_data.append(df)
        
        combined_df = pd.concat(sample_data, ignore_index=True)
        print(f"✓ Generated {len(combined_df)} sample records")
        print(f"  Symbols: {combined_df['symbol'].unique().tolist()}")
        return combined_df
    except Exception as e:
        print(f"✗ Sample data generation error: {e}")
        return None


def test_volatility_calculation():
    """Test volatility calculation without database."""
    print("\n=== Testing Volatility Calculation ===")
    try:
        # Generate sample data
        sample_df = generate_sample_data()
        if sample_df is None:
            return False
        
        # Test volatility monitor
        monitor = VolatilityMonitor()
        
        # Test with first symbol
        test_symbol_data = sample_df[sample_df['symbol'] == 'TEST1.T'].copy()
        test_symbol_data = test_symbol_data.sort_values('date')
        
        # Calculate volatility
        result = monitor.calculate_volatility(test_symbol_data)
        
        if 'volatility' in result.columns:
            latest_volatility = result['volatility'].dropna().iloc[-1]
            print(f"✓ Volatility calculated successfully")
            print(f"  Latest volatility: {latest_volatility:.6f}")
            
            # Test alert detection
            alerts = monitor.detect_volatility_alerts(result)
            print(f"  Detected {len(alerts)} volatility alerts")
            return True
        else:
            print("✗ Volatility calculation failed")
            return False
    except Exception as e:
        print(f"✗ Volatility calculation error: {e}")
        return False


def test_pipeline_import():
    """Test pipeline module imports."""
    print("\n=== Testing Pipeline Imports ===")
    try:
        from src.etl.pipeline import ELTPipeline
        print("✓ ELTPipeline imported successfully")
        
        pipeline = ELTPipeline()
        print("✓ Pipeline instance created")
        return True
    except Exception as e:
        print(f"✗ Pipeline import error: {e}")
        return False


def test_dashboard_import():
    """Test dashboard module imports."""
    print("\n=== Testing Dashboard Imports ===")
    try:
        # Just test if we can import streamlit and the required modules
        import streamlit
        print("✓ Streamlit imported successfully")
        
        import plotly.graph_objects
        print("✓ Plotly imported successfully")
        
        # Test that dashboard.py exists and is readable
        dashboard_file = Path(__file__).parent / "dashboard.py"
        if dashboard_file.exists():
            print("✓ Dashboard file exists")
            return True
        else:
            print("✗ Dashboard file not found")
            return False
    except Exception as e:
        print(f"✗ Dashboard import error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Market Analysis Platform - Test Suite")
    print("=" * 60)
    
    results = {
        'Database Connection': test_database_connection(),
        'Data Extraction': test_data_extraction(),
        'Volatility Calculation': test_volatility_calculation(),
        'Pipeline Import': test_pipeline_import(),
        'Dashboard Import': test_dashboard_import()
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:.<40} {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print("\n" + "=" * 60)
    print(f"Total: {passed_tests}/{total_tests} tests passed")
    print("=" * 60)
    
    return passed_tests == total_tests


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
