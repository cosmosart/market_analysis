"""
Demo script to test the stock market analysis system with synthetic data.
This is useful when there's no internet connection or for testing purposes.
"""

import numpy as np
import pandas as pd
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_preprocessor import DataPreprocessor
from ml_models import LSTMPredictor, LinearRegressionPredictor, ModelEvaluator
from visualizer import StockVisualizer


def generate_synthetic_stock_data(n_days=500, start_price=100, trend=0.001, volatility=0.02):
    """
    Generate synthetic stock data for testing.
    
    Args:
        n_days: Number of days to generate
        start_price: Starting stock price
        trend: Daily trend factor
        volatility: Daily volatility factor
    
    Returns:
        DataFrame with synthetic stock data
    """
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=n_days, freq='D')
    
    # Generate price with trend and random walk
    returns = np.random.normal(trend, volatility, n_days)
    price_multipliers = np.exp(returns)
    prices = start_price * np.cumprod(price_multipliers)
    
    # Generate OHLCV data
    data = pd.DataFrame({
        'Open': prices * np.random.uniform(0.98, 1.02, n_days),
        'High': prices * np.random.uniform(1.00, 1.05, n_days),
        'Low': prices * np.random.uniform(0.95, 1.00, n_days),
        'Close': prices,
        'Volume': np.random.randint(1000000, 10000000, n_days)
    }, index=dates)
    
    # Ensure High is highest and Low is lowest
    data['High'] = data[['Open', 'High', 'Low', 'Close']].max(axis=1)
    data['Low'] = data[['Open', 'High', 'Low', 'Close']].min(axis=1)
    
    return data


def main():
    """Main demo function."""
    
    print("="*70)
    print("Stock Market Analysis Demo with Synthetic Data".center(70))
    print("="*70)
    print()
    
    # Generate synthetic data
    print("[1/6] Generating synthetic stock data...")
    data = generate_synthetic_stock_data(n_days=500, start_price=150, trend=0.0005, volatility=0.02)
    print(f"✓ Generated {len(data)} days of synthetic data")
    print(f"  Price range: ${data['Close'].min():.2f} - ${data['Close'].max():.2f}")
    print()
    
    # Preprocess data
    print("[2/6] Preprocessing data and adding technical indicators...")
    preprocessor = DataPreprocessor()
    data_with_indicators = preprocessor.add_technical_indicators(data)
    data_clean = preprocessor.handle_missing_data(data_with_indicators, method='drop')
    print(f"✓ Data preprocessed successfully")
    print(f"  Features added: MA7, MA21, MA50, MACD, RSI, Bollinger Bands, etc.")
    print()
    
    # Prepare data for ML
    print("[3/6] Preparing data for machine learning...")
    lookback = 60
    X, y, scaler = preprocessor.prepare_data_for_lstm(data_clean, 'Close', lookback)
    X_train, X_test, y_train, y_test = preprocessor.split_data(X, y, train_ratio=0.8)
    print(f"✓ Data prepared successfully")
    print(f"  Training samples: {len(X_train)}")
    print(f"  Testing samples: {len(X_test)}")
    print(f"  Lookback period: {lookback} days")
    print()
    
    # Train LSTM Model
    print("[4/6] Training LSTM model...")
    lstm_model = LSTMPredictor(lookback=lookback)
    print("  Training with 20 epochs...")
    history = lstm_model.train(X_train, y_train, epochs=20, verbose=0)
    print(f"✓ LSTM model trained successfully")
    print(f"  Final loss: {history['loss'][-1]:.6f}")
    print()
    
    # Train Linear Regression Model
    print("[5/6] Training Linear Regression model for comparison...")
    lr_model = LinearRegressionPredictor()
    lr_model.train(X_train, y_train)
    print(f"✓ Linear Regression model trained successfully")
    print()
    
    # Make predictions and evaluate
    print("[6/6] Making predictions and evaluating performance...")
    
    # LSTM predictions
    lstm_train_pred = lstm_model.predict(X_train)
    lstm_test_pred = lstm_model.predict(X_test)
    lstm_train_pred = preprocessor.inverse_scale(lstm_train_pred)
    lstm_test_pred = preprocessor.inverse_scale(lstm_test_pred)
    
    # LR predictions
    lr_train_pred = lr_model.predict(X_train)
    lr_test_pred = lr_model.predict(X_test)
    lr_train_pred = preprocessor.inverse_scale(lr_train_pred)
    lr_test_pred = preprocessor.inverse_scale(lr_test_pred)
    
    # Actual values
    y_train_actual = preprocessor.inverse_scale(y_train)
    y_test_actual = preprocessor.inverse_scale(y_test)
    
    # Calculate metrics
    evaluator = ModelEvaluator()
    
    lstm_train_metrics = evaluator.calculate_metrics(y_train_actual, lstm_train_pred)
    lstm_test_metrics = evaluator.calculate_metrics(y_test_actual, lstm_test_pred)
    
    lr_train_metrics = evaluator.calculate_metrics(y_train_actual, lr_train_pred)
    lr_test_metrics = evaluator.calculate_metrics(y_test_actual, lr_test_pred)
    
    print("✓ Predictions completed")
    print()
    
    # Display metrics
    evaluator.print_metrics(lstm_train_metrics, "LSTM Training")
    evaluator.print_metrics(lstm_test_metrics, "LSTM Testing")
    evaluator.print_metrics(lr_train_metrics, "Linear Regression Training")
    evaluator.print_metrics(lr_test_metrics, "Linear Regression Testing")
    
    print("="*70)
    print("Comparison Summary".center(70))
    print("="*70)
    print(f"\n{'Model':<20} {'Test RMSE':<15} {'Test MAPE':<15} {'Test R²':<15}")
    print("-"*70)
    print(f"{'LSTM':<20} {lstm_test_metrics['RMSE']:<15.4f} {lstm_test_metrics['MAPE']:<15.2f} {lstm_test_metrics['R2']:<15.4f}")
    print(f"{'Linear Regression':<20} {lr_test_metrics['RMSE']:<15.4f} {lr_test_metrics['MAPE']:<15.2f} {lr_test_metrics['R2']:<15.4f}")
    print("-"*70)
    
    # Determine which model performed better
    if lstm_test_metrics['RMSE'] < lr_test_metrics['RMSE']:
        print("\n🏆 LSTM model performed better (lower RMSE)")
    else:
        print("\n🏆 Linear Regression performed better (lower RMSE)")
    
    print("\n" + "="*70)
    print("Demo Complete!".center(70))
    print("="*70)
    print("\nNote: This demo used synthetic data for testing purposes.")
    print("Use main.py with real stock tickers to analyze actual market data.")
    print()


if __name__ == "__main__":
    main()
