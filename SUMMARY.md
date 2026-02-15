# Project Summary: Market Analysis Platform

## Overview
A comprehensive Python-based ELT (Extract-Load-Transform) pipeline and interactive Streamlit dashboard for analyzing Japanese and Korean stock markets. The platform is designed for a private financial analytics use case with two distinct investment strategies:

1. **Japanese Stocks (NISA)**: Conservative long-term investments
2. **Korean Stocks (Active)**: High-risk active trading

## Architecture

### Components

#### 1. Data Extraction Layer (`src/etl/extractor.py`)
- **Technology**: yfinance API
- **Features**:
  - Daily OHLCV (Open, High, Low, Close, Volume) data extraction
  - Intraday data extraction (configurable intervals: 1m, 5m, 15m, 1h)
  - Supports Tokyo Stock Exchange (.T) and Korea Exchange (.KS) symbols
  - Automatic retry and error handling
  - Batch processing for multiple symbols

#### 2. Data Storage Layer (`sql/schema.sql`, `src/database/connection.py`)
- **Technology**: PostgreSQL 14+
- **Schema Design**:
  - `stock_info`: Stock metadata (symbol, exchange, company name, sector)
  - `daily_data`: Daily OHLCV data with indexes for fast queries
  - `intraday_data`: Intraday OHLCV data for active trading
  - `portfolio`: Portfolio definitions (NISA or ACTIVE)
  - `portfolio_holdings`: Individual holdings with purchase tracking
  - `volatility_alerts`: ML-generated alerts
- **Features**:
  - Connection pooling and context managers
  - Parameterized queries for security
  - Automatic timestamp updates via triggers
  - Optimized indexes for query performance

#### 3. Data Loading Layer (`src/etl/loader.py`)
- **Features**:
  - Upsert operations (INSERT ... ON CONFLICT DO UPDATE)
  - Batch loading for efficiency
  - Data validation and error handling
  - Query methods for dashboard

#### 4. ML Monitoring Layer (`src/ml/volatility.py`)
- **Technology**: scikit-learn, pandas
- **Features**:
  - Rolling volatility calculation (standard deviation of returns)
  - Alert classification: HIGH, MEDIUM, LOW
  - Percentile ranking for contextualization
  - Historical alert storage
  - Multi-symbol monitoring

#### 5. Dashboard Layer (`dashboard.py`)
- **Technology**: Streamlit, Plotly
- **Pages**:
  1. **Overview**: Summary metrics and recent alerts
  2. **Japanese Investments (NISA)**: Conservative long-term tracking
  3. **Korean Trading (Active)**: High-risk active trading metrics
  4. **Volatility Monitor**: ML-based alerts and trends
- **Features**:
  - Interactive charts (price, volume, volatility)
  - Real-time data refresh
  - Filtering and date range selection
  - Color-coded alerts

#### 6. Pipeline Orchestration (`src/etl/pipeline.py`)
- **Features**:
  - Daily pipeline: Full historical data refresh
  - Intraday pipeline: Active trading data updates
  - Combined mode: Both pipelines
  - Command-line interface
  - Logging and error tracking

## Data Flow

```
┌─────────────────┐
│  yfinance API   │
│  (Yahoo Finance)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Data Extract  │ ← src/etl/extractor.py
│  (Daily/Intraday)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Loading   │ ← src/etl/loader.py
│   (PostgreSQL)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │
│    Database     │
└────┬───────┬────┘
     │       │
     │       └──────────┐
     │                  │
     ▼                  ▼
┌──────────┐    ┌──────────────┐
│ ML Model │    │  Dashboard   │
│Volatility│    │  (Streamlit) │
└────┬─────┘    └──────────────┘
     │
     ▼
┌──────────┐
│  Alerts  │
└──────────┘
```

## Technology Stack

### Core
- **Python 3.9+**: Main programming language
- **PostgreSQL 14+**: Relational database
- **yfinance 0.2.36**: Financial data API

### Data Processing
- **pandas 2.2.0**: Data manipulation
- **numpy 1.26.4**: Numerical computing
- **scikit-learn 1.4.0**: Machine learning

### Visualization
- **Streamlit 1.31.1**: Dashboard framework
- **Plotly 5.19.0**: Interactive charts
- **Altair 5.2.0**: Statistical visualizations

### Database
- **psycopg2-binary 2.9.9**: PostgreSQL adapter
- **SQLAlchemy 2.0.25**: SQL toolkit

### Configuration
- **python-dotenv 1.0.1**: Environment management
- **pydantic 2.6.0**: Data validation

## Configuration

### Environment Variables (.env)
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=market_analysis
DB_USER=postgres
DB_PASSWORD=your_password

JAPANESE_SYMBOLS=7203.T,6758.T,8306.T,9984.T,6861.T
KOREAN_SYMBOLS=005930.KS,000660.KS,035720.KS,051910.KS,035420.KS

VOLATILITY_THRESHOLD=0.05
VOLATILITY_WINDOW=20
```

### Stock Symbols

**Japanese Stocks (Tokyo Stock Exchange)**:
- 7203.T: Toyota Motor Corporation
- 6758.T: Sony Group Corporation
- 8306.T: Mitsubishi UFJ Financial Group
- 9984.T: SoftBank Group Corp
- 6861.T: Keyence Corporation

**Korean Stocks (Korea Exchange)**:
- 005930.KS: Samsung Electronics
- 000660.KS: SK Hynix
- 035720.KS: Kakao Corporation
- 051910.KS: LG Chem
- 035420.KS: NAVER Corporation

## Deployment

### Local Development
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your settings

# 3. Initialize database
python init_db.py

# 4. Run pipeline
python -m src.etl.pipeline --mode daily

# 5. Launch dashboard
streamlit run dashboard.py
```

### Production (TrueNAS Server)
```bash
# 1. Setup PostgreSQL on TrueNAS
# 2. Configure firewall rules
# 3. Setup scheduled tasks:

# Daily data refresh (6 AM)
0 6 * * * cd /path/to/market_analysis && python -m src.etl.pipeline --mode daily

# Intraday updates (every 5 min, market hours)
*/5 9-15 * * 1-5 cd /path/to/market_analysis && python -m src.etl.pipeline --mode intraday

# 4. Run dashboard as service
# Use systemd or supervisor for persistent operation
```

## Security Features

### Implemented
1. **SQL Injection Prevention**:
   - Parameterized queries throughout
   - Proper INTERVAL handling in PostgreSQL
   - No string concatenation in SQL

2. **Connection Security**:
   - Context managers for automatic cleanup
   - Transaction management with rollback
   - Password stored in environment variables

3. **Data Validation**:
   - Input validation in all API endpoints
   - Type checking with Pydantic
   - Error handling and logging

4. **Code Quality**:
   - Passed CodeQL security scanning (0 alerts)
   - No SQL injection vulnerabilities
   - No path traversal issues

## Performance Optimization

1. **Database**:
   - Indexes on frequently queried columns
   - Batch inserts for data loading
   - Upsert operations to avoid duplicates

2. **Data Processing**:
   - Vectorized operations with pandas
   - Rolling window calculations
   - Efficient date filtering

3. **Dashboard**:
   - Lazy loading of data
   - Caching where appropriate
   - Optimized query limits

## Monitoring & Maintenance

### Logs
- Pipeline execution logs
- Database connection logs
- Error tracking with timestamps

### Alerts
- Volatility alerts stored in database
- Configurable thresholds
- Historical alert tracking

### Backups
- Regular PostgreSQL backups recommended
- Export data periodically
- Version control for code

## Testing

### Test Suite (`test_platform.py`)
- Database connection testing
- Data extraction validation
- Volatility calculation testing
- Module import verification
- Dashboard component testing

### Demo (`demo.py`)
- Sample data generation
- ML model demonstration
- Usage instructions

## Future Enhancements

### Potential Improvements
1. Real-time WebSocket data feeds
2. Advanced ML models (LSTM, Prophet)
3. Portfolio optimization algorithms
4. Risk metrics (Sharpe ratio, VaR)
5. Alert notifications (email, SMS)
6. Multi-user authentication
7. Mobile-responsive dashboard
8. API for external integrations

## Maintenance Guide

### Daily Operations
- Monitor pipeline execution logs
- Review volatility alerts
- Check database disk space
- Verify data completeness

### Weekly Tasks
- Review ML model performance
- Analyze portfolio performance
- Update stock symbol lists
- Check for API rate limits

### Monthly Tasks
- Database maintenance (VACUUM, ANALYZE)
- Review and archive old data
- Update dependencies
- Backup configuration files

## License & Acknowledgments

- **License**: MIT License
- **Data Provider**: Yahoo Finance (via yfinance)
- **Framework**: Streamlit
- **Database**: PostgreSQL
- **ML Library**: scikit-learn

## Contact & Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/cosmosart/market_analysis/issues
- Documentation: README.md
- Demo: demo.py

---

**Last Updated**: February 2026
**Version**: 1.0.0
**Status**: Production Ready
