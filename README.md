# Market Analysis Platform

A comprehensive Python-based ELT pipeline and Streamlit dashboard for financial analytics, focusing on Japanese and Korean stock markets.

## Features

- **Data Extraction**: Real-time daily and intraday stock data from yfinance API
- **Data Storage**: PostgreSQL database with optimized schema for market data
- **ML Monitoring**: Machine learning-based volatility detection and alerts
- **Interactive Dashboard**: Streamlit-powered visualization for portfolio tracking
- **Market Focus**: 
  - Japanese stocks (Tokyo Stock Exchange) - NISA long-term investments
  - Korean stocks (Korea Exchange) - Active trading strategies

## Architecture

```
market_analysis/
├── config.py                 # Configuration management
├── dashboard.py              # Streamlit dashboard
├── init_db.py               # Database initialization script
├── requirements.txt         # Python dependencies
├── sql/
│   └── schema.sql          # PostgreSQL database schema
└── src/
    ├── database/
    │   └── connection.py   # Database connection utilities
    ├── etl/
    │   ├── extractor.py    # Data extraction from yfinance
    │   ├── loader.py       # Data loading to PostgreSQL
    │   └── pipeline.py     # ELT pipeline orchestration
    └── ml/
        └── volatility.py   # ML-based volatility monitoring
```

## Prerequisites

- Python 3.9+
- PostgreSQL 14+ (running on local TrueNAS server or any PostgreSQL instance)
- Internet connection for yfinance API access

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/cosmosart/market_analysis.git
cd market_analysis
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure database

Copy the example environment file and configure your database settings:

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=market_analysis
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### 4. Initialize database

Create the database schema:

```bash
python init_db.py
```

## Usage

### Running the ELT Pipeline

#### Daily Data Pipeline

Extract and load daily stock data:

```bash
python -m src.etl.pipeline --mode daily
```

#### Intraday Data Pipeline

Extract and load intraday data for active trading:

```bash
python -m src.etl.pipeline --mode intraday --interval 5m
```

#### Both Pipelines

Run both daily and intraday pipelines:

```bash
python -m src.etl.pipeline --mode both
```

### Launching the Dashboard

Start the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

The dashboard will be available at `http://localhost:8501`

## Dashboard Features

### 1. Overview
- Summary statistics for all markets
- Recent volatility alerts
- Portfolio overview

### 2. Japanese Investments (NISA)
- Conservative long-term investment tracking
- Stock performance charts
- Volume analysis
- Portfolio holdings

### 3. Korean Trading (Active)
- High-risk active trading metrics
- Real-time performance tracking
- Intraday data visualization
- Trading volume analysis

### 4. Volatility Monitor
- ML-based price volatility detection
- Alert classification (HIGH, MEDIUM, LOW)
- Historical volatility trends
- Exchange-specific filtering

## Database Schema

### Tables

- **stock_info**: Stock metadata (symbol, exchange, company name, sector)
- **daily_data**: Daily OHLCV data
- **intraday_data**: Intraday OHLCV data (5-minute intervals)
- **portfolio**: Portfolio information (NISA or ACTIVE)
- **portfolio_holdings**: Individual holdings within portfolios
- **volatility_alerts**: ML-generated volatility alerts

## Configuration

### Stock Symbols

Edit `config.py` or `.env` to customize the stock symbols:

**Japanese Stocks (Tokyo Stock Exchange):**
```python
JAPANESE_SYMBOLS=7203.T,6758.T,8306.T,9984.T,6861.T
# Examples: Toyota (7203.T), Sony (6758.T), Mitsubishi UFJ (8306.T)
```

**Korean Stocks (Korea Exchange):**
```python
KOREAN_SYMBOLS=005930.KS,000660.KS,035720.KS,051910.KS,035420.KS
# Examples: Samsung (005930.KS), SK Hynix (000660.KS), Kakao (035720.KS)
```

### Volatility Settings

Adjust ML monitoring parameters:

```python
VOLATILITY_THRESHOLD=0.05      # Threshold for high volatility alerts
VOLATILITY_WINDOW=20           # Rolling window for volatility calculation
```

## Scheduling

### Using Cron (Linux/Mac)

Add to crontab for automated execution:

```bash
# Daily data pipeline at 6 AM
0 6 * * * cd /path/to/market_analysis && python -m src.etl.pipeline --mode daily

# Intraday data pipeline every 5 minutes during market hours
*/5 9-15 * * 1-5 cd /path/to/market_analysis && python -m src.etl.pipeline --mode intraday
```

### Using Task Scheduler (Windows)

Create scheduled tasks for regular pipeline execution.

## Development

### Running Tests

```bash
# Run all tests (if test infrastructure exists)
pytest tests/

# Run specific test module
pytest tests/test_extractor.py
```

### Code Style

The project follows PEP 8 style guidelines. Format code using:

```bash
black src/
```

## Troubleshooting

### Database Connection Issues

- Verify PostgreSQL is running: `pg_isready -h localhost`
- Check credentials in `.env` file
- Ensure database exists: `createdb market_analysis`

### yfinance API Issues

- Check internet connectivity
- Verify stock symbols are correct
- Some exchanges may have data delays

### Dashboard Not Loading Data

- Ensure database is initialized: `python init_db.py`
- Run pipeline to populate data: `python -m src.etl.pipeline --mode daily`
- Check database has data: `SELECT COUNT(*) FROM daily_data;`

## Security Notes

- Never commit `.env` file with real credentials
- Use strong passwords for PostgreSQL
- Consider using environment variables in production
- Implement proper access controls for dashboard deployment

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.

## Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) - Financial data extraction
- [Streamlit](https://streamlit.io/) - Dashboard framework
- [PostgreSQL](https://www.postgresql.org/) - Database system
- [scikit-learn](https://scikit-learn.org/) - Machine learning library