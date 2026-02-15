"""Configuration management for the market analysis platform."""
import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "market_analysis")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Database connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Stock symbols
JAPANESE_SYMBOLS = os.getenv("JAPANESE_SYMBOLS", "7203.T,6758.T,8306.T,9984.T,6861.T").split(",")
KOREAN_SYMBOLS = os.getenv("KOREAN_SYMBOLS", "005930.KS,000660.KS,035720.KS,051910.KS,035420.KS").split(",")

# Data refresh intervals (in minutes)
DAILY_REFRESH_INTERVAL = int(os.getenv("DAILY_REFRESH_INTERVAL", "1440"))
INTRADAY_REFRESH_INTERVAL = int(os.getenv("INTRADAY_REFRESH_INTERVAL", "5"))

# ML Monitoring Settings
VOLATILITY_THRESHOLD = float(os.getenv("VOLATILITY_THRESHOLD", "0.05"))
VOLATILITY_WINDOW = int(os.getenv("VOLATILITY_WINDOW", "20"))

# Project paths
BASE_DIR = Path(__file__).resolve().parent
SQL_DIR = BASE_DIR / "sql"
