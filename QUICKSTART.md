# Quick Reference Guide

## Common Commands

### Database Operations
```bash
# Initialize database schema
python init_db.py

# Test database connection
python -c "from src.database.connection import db; db.test_connection()"
```

### Data Pipeline
```bash
# Run daily data extraction
python -m src.etl.pipeline --mode daily

# Run intraday data extraction (5-minute intervals)
python -m src.etl.pipeline --mode intraday --interval 5m

# Run both pipelines
python -m src.etl.pipeline --mode both
```

### Dashboard
```bash
# Start Streamlit dashboard
streamlit run dashboard.py

# Start on specific port
streamlit run dashboard.py --server.port 8080

# Start with custom config
streamlit run dashboard.py --server.address 0.0.0.0
```

### Testing & Demo
```bash
# Run test suite
python test_platform.py

# Run demo with sample data
python demo.py
```

## File Structure
```
market_analysis/
├── config.py              # Configuration settings
├── dashboard.py           # Streamlit dashboard
├── init_db.py            # Database initialization
├── demo.py               # Usage demonstration
├── test_platform.py      # Test suite
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
├── README.md             # Setup instructions
├── SUMMARY.md            # Detailed documentation
├── sql/
│   └── schema.sql        # Database schema
└── src/
    ├── database/
    │   └── connection.py # Database utilities
    ├── etl/
    │   ├── extractor.py  # Data extraction
    │   ├── loader.py     # Data loading
    │   └── pipeline.py   # Pipeline orchestration
    └── ml/
        └── volatility.py # Volatility monitoring
```

## Stock Symbols

### Japanese Stocks (Tokyo Stock Exchange)
```python
JAPANESE_SYMBOLS = [
    "7203.T",   # Toyota Motor
    "6758.T",   # Sony Group
    "8306.T",   # Mitsubishi UFJ
    "9984.T",   # SoftBank Group
    "6861.T"    # Keyence
]
```

### Korean Stocks (Korea Exchange)
```python
KOREAN_SYMBOLS = [
    "005930.KS",  # Samsung Electronics
    "000660.KS",  # SK Hynix
    "035720.KS",  # Kakao
    "051910.KS",  # LG Chem
    "035420.KS"   # NAVER
]
```

## Configuration Parameters

### Database
- `DB_HOST`: PostgreSQL host (default: localhost)
- `DB_PORT`: PostgreSQL port (default: 5432)
- `DB_NAME`: Database name (default: market_analysis)
- `DB_USER`: Database user (default: postgres)
- `DB_PASSWORD`: Database password

### Data Refresh
- `DAILY_REFRESH_INTERVAL`: Minutes between daily updates (default: 1440)
- `INTRADAY_REFRESH_INTERVAL`: Minutes between intraday updates (default: 5)

### ML Settings
- `VOLATILITY_THRESHOLD`: Alert threshold (default: 0.05)
- `VOLATILITY_WINDOW`: Rolling window size (default: 20)

## Dashboard Pages

### 1. Overview
- Summary metrics for both markets
- Recent volatility alerts
- Quick statistics

### 2. Japanese Investments (NISA)
- Conservative long-term portfolio
- Price and volume charts
- Performance statistics
- Portfolio holdings

### 3. Korean Trading (Active)
- High-risk active trading
- Real-time metrics
- Intraday data visualization
- Trading statistics

### 4. Volatility Monitor
- ML-based alerts
- Alert classification (HIGH/MEDIUM/LOW)
- Historical trends
- Exchange filtering

## Troubleshooting

### Database Connection Failed
```bash
# Check if PostgreSQL is running
pg_isready -h localhost -p 5432

# Create database if missing
createdb market_analysis

# Verify credentials in .env
cat .env
```

### Module Import Errors
```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -E 'yfinance|psycopg2|streamlit'
```

### No Data in Dashboard
```bash
# Run pipeline first
python -m src.etl.pipeline --mode daily

# Verify data in database
psql -d market_analysis -c "SELECT COUNT(*) FROM daily_data;"
```

### yfinance API Errors
- Check internet connection
- Verify stock symbols are correct
- Check for API rate limits (usually none for yfinance)

## Cron Schedule Examples

### Linux/Mac (crontab -e)
```bash
# Daily data at 6 AM
0 6 * * * cd /path/to/market_analysis && python -m src.etl.pipeline --mode daily >> /var/log/market_analysis.log 2>&1

# Intraday every 5 minutes (9 AM - 3 PM, weekdays)
*/5 9-15 * * 1-5 cd /path/to/market_analysis && python -m src.etl.pipeline --mode intraday >> /var/log/market_analysis.log 2>&1
```

### Windows (Task Scheduler)
- Create Basic Task
- Trigger: Daily at 6:00 AM
- Action: Start a program
- Program: `python`
- Arguments: `-m src.etl.pipeline --mode daily`
- Start in: `C:\path\to\market_analysis`

## Database Queries

### View Recent Data
```sql
-- Latest daily data
SELECT * FROM daily_data ORDER BY date DESC LIMIT 10;

-- Recent volatility alerts
SELECT * FROM volatility_alerts ORDER BY alert_date DESC LIMIT 10;

-- Portfolio summary
SELECT * FROM portfolio;
```

### Data Statistics
```sql
-- Count records by symbol
SELECT symbol, COUNT(*) as records 
FROM daily_data 
GROUP BY symbol 
ORDER BY records DESC;

-- Average volatility by exchange
SELECT si.exchange, AVG(va.volatility_score) as avg_volatility
FROM volatility_alerts va
JOIN stock_info si ON va.symbol = si.symbol
GROUP BY si.exchange;
```

## Python API Examples

### Extract Data
```python
from src.etl.extractor import DataExtractor

extractor = DataExtractor(['7203.T'])
df = extractor.get_daily_data('7203.T', period='1mo')
print(df.head())
```

### Load Data
```python
from src.etl.loader import DataLoader

loader = DataLoader()
loader.load_daily_data(df)
```

### Volatility Analysis
```python
from src.ml.volatility import VolatilityMonitor

monitor = VolatilityMonitor()
analysis = monitor.analyze_symbol('7203.T', days=100)
print(analysis)
```

## Performance Tips

1. **Database**: Run VACUUM ANALYZE monthly
2. **Pipeline**: Use batch processing for multiple symbols
3. **Dashboard**: Limit query results with appropriate date ranges
4. **Logs**: Rotate logs regularly to save disk space

## Security Checklist

- [x] Use environment variables for credentials
- [x] Implement parameterized queries
- [x] Regular database backups
- [x] Secure PostgreSQL with strong passwords
- [x] Use firewall rules for database access
- [x] Keep dependencies updated

## Support Resources

- **README.md**: Setup and installation guide
- **SUMMARY.md**: Comprehensive technical documentation
- **demo.py**: Interactive demonstration
- **test_platform.py**: Validation tests

---
**Version**: 1.0.0
**Last Updated**: February 2026
