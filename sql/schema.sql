-- Market Analysis Database Schema
-- PostgreSQL 14+

-- Drop existing tables if needed
DROP TABLE IF EXISTS portfolio_holdings CASCADE;
DROP TABLE IF EXISTS portfolio CASCADE;
DROP TABLE IF EXISTS intraday_data CASCADE;
DROP TABLE IF EXISTS daily_data CASCADE;
DROP TABLE IF EXISTS stock_info CASCADE;
DROP TABLE IF EXISTS volatility_alerts CASCADE;

-- Stock information table
CREATE TABLE stock_info (
    symbol VARCHAR(20) PRIMARY KEY,
    exchange VARCHAR(10) NOT NULL CHECK (exchange IN ('JAPANESE', 'KOREAN')),
    company_name VARCHAR(255),
    sector VARCHAR(100),
    currency VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Daily stock data table
CREATE TABLE daily_data (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) REFERENCES stock_info(symbol) ON DELETE CASCADE,
    date DATE NOT NULL,
    open DECIMAL(15, 4),
    high DECIMAL(15, 4),
    low DECIMAL(15, 4),
    close DECIMAL(15, 4),
    adj_close DECIMAL(15, 4),
    volume BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, date)
);

-- Intraday stock data table (for active trading)
CREATE TABLE intraday_data (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) REFERENCES stock_info(symbol) ON DELETE CASCADE,
    timestamp TIMESTAMP NOT NULL,
    open DECIMAL(15, 4),
    high DECIMAL(15, 4),
    low DECIMAL(15, 4),
    close DECIMAL(15, 4),
    volume BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, timestamp)
);

-- Portfolio table (for tracking investments)
CREATE TABLE portfolio (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    portfolio_type VARCHAR(20) NOT NULL CHECK (portfolio_type IN ('NISA', 'ACTIVE')),
    exchange VARCHAR(10) NOT NULL CHECK (exchange IN ('JAPANESE', 'KOREAN')),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Portfolio holdings table
CREATE TABLE portfolio_holdings (
    id SERIAL PRIMARY KEY,
    portfolio_id INTEGER REFERENCES portfolio(id) ON DELETE CASCADE,
    symbol VARCHAR(20) REFERENCES stock_info(symbol) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    purchase_price DECIMAL(15, 4) NOT NULL,
    purchase_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Volatility alerts table (ML-based monitoring)
CREATE TABLE volatility_alerts (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) REFERENCES stock_info(symbol) ON DELETE CASCADE,
    alert_date DATE NOT NULL,
    volatility_score DECIMAL(10, 6) NOT NULL,
    price_at_alert DECIMAL(15, 4),
    alert_type VARCHAR(20) NOT NULL CHECK (alert_type IN ('HIGH', 'MEDIUM', 'LOW')),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, alert_date)
);

-- Create indexes for better query performance
CREATE INDEX idx_daily_data_symbol_date ON daily_data(symbol, date DESC);
CREATE INDEX idx_intraday_data_symbol_timestamp ON intraday_data(symbol, timestamp DESC);
CREATE INDEX idx_portfolio_holdings_portfolio_id ON portfolio_holdings(portfolio_id);
CREATE INDEX idx_volatility_alerts_symbol_date ON volatility_alerts(symbol, alert_date DESC);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for automatic timestamp updates
CREATE TRIGGER update_stock_info_updated_at BEFORE UPDATE ON stock_info
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_portfolio_updated_at BEFORE UPDATE ON portfolio
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_portfolio_holdings_updated_at BEFORE UPDATE ON portfolio_holdings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
