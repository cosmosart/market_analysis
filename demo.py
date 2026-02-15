"""
Quick Start Guide - Market Analysis Platform

This script demonstrates how to use the market analysis platform
with sample data when database/network is not available.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.ml.volatility import VolatilityMonitor

print("=" * 70)
print("MARKET ANALYSIS PLATFORM - QUICK START DEMO")
print("=" * 70)

# Generate sample stock data
print("\n1. Generating Sample Stock Data...")
print("-" * 70)

dates = pd.date_range(end=datetime.now(), periods=100, freq='D')

# Japanese stock (NISA - Conservative)
japanese_data = pd.DataFrame({
    'symbol': '7203.T',
    'date': dates,
    'close': 2000 + np.random.randn(100).cumsum() * 10
})

# Korean stock (Active - Higher volatility)
korean_data = pd.DataFrame({
    'symbol': '005930.KS',
    'date': dates,
    'close': 70000 + np.random.randn(100).cumsum() * 500
})

print(f"✓ Generated {len(japanese_data)} days of data for Japanese stock (7203.T - Toyota)")
print(f"✓ Generated {len(korean_data)} days of data for Korean stock (005930.KS - Samsung)")

# Demonstrate volatility monitoring
print("\n2. ML-Based Volatility Monitoring...")
print("-" * 70)

monitor = VolatilityMonitor(window=20, threshold=0.05)

# Analyze Japanese stock
print("\n   Analyzing Japanese Stock (Conservative NISA Investment):")
jp_analyzed = monitor.calculate_volatility(japanese_data)
jp_volatility = jp_analyzed['volatility'].dropna().iloc[-1]
print(f"   - Latest volatility: {jp_volatility:.6f}")
print(f"   - Volatility percentile: {jp_analyzed['volatility_percentile'].iloc[-1]:.2%}")

jp_alerts = monitor.detect_volatility_alerts(jp_analyzed)
print(f"   - Volatility alerts: {len(jp_alerts)} periods detected")

# Analyze Korean stock
print("\n   Analyzing Korean Stock (Active Trading):")
kr_analyzed = monitor.calculate_volatility(korean_data)
kr_volatility = kr_analyzed['volatility'].dropna().iloc[-1]
print(f"   - Latest volatility: {kr_volatility:.6f}")
print(f"   - Volatility percentile: {kr_analyzed['volatility_percentile'].iloc[-1]:.2%}")

kr_alerts = monitor.detect_volatility_alerts(kr_analyzed)
print(f"   - Volatility alerts: {len(kr_alerts)} periods detected")

# Show price trends
print("\n3. Price Trend Analysis...")
print("-" * 70)

jp_return = ((japanese_data['close'].iloc[-1] - japanese_data['close'].iloc[0]) / 
             japanese_data['close'].iloc[0]) * 100
kr_return = ((korean_data['close'].iloc[-1] - korean_data['close'].iloc[0]) / 
             korean_data['close'].iloc[0]) * 100

print(f"\n   Japanese Stock (7203.T):")
print(f"   - Start Price: ¥{japanese_data['close'].iloc[0]:.2f}")
print(f"   - Current Price: ¥{japanese_data['close'].iloc[-1]:.2f}")
print(f"   - Return: {jp_return:+.2f}%")

print(f"\n   Korean Stock (005930.KS):")
print(f"   - Start Price: ₩{korean_data['close'].iloc[0]:.2f}")
print(f"   - Current Price: ₩{korean_data['close'].iloc[-1]:.2f}")
print(f"   - Return: {kr_return:+.2f}%")

# Usage instructions
print("\n4. Next Steps - Full Platform Setup...")
print("-" * 70)
print("""
To use the complete platform with real data:

A. Database Setup:
   1. Install PostgreSQL on your TrueNAS server
   2. Create database: createdb market_analysis
   3. Configure .env file with your credentials
   4. Initialize schema: python init_db.py

B. Extract Real Data:
   # Daily data pipeline
   python -m src.etl.pipeline --mode daily
   
   # Intraday data pipeline (every 5 minutes)
   python -m src.etl.pipeline --mode intraday --interval 5m

C. Launch Dashboard:
   streamlit run dashboard.py
   
   Navigate to http://localhost:8501 to view:
   - Japanese Investments (NISA) - Conservative long-term
   - Korean Trading (Active) - High-risk short-term
   - Volatility Monitor - ML-based alerts

D. Schedule Automated Runs:
   Add to crontab:
   0 6 * * * cd /path/to/market_analysis && python -m src.etl.pipeline --mode daily
   */5 9-15 * * 1-5 cd /path/to/market_analysis && python -m src.etl.pipeline --mode intraday
""")

print("\n" + "=" * 70)
print("Demo completed! Platform is ready for production use.")
print("=" * 70)
