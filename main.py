#!/usr/bin/env python3
"""
Main script for Stock Market Analysis with ML Prediction.
"""

import argparse
import sys
import os
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_fetcher import StockDataFetcher
from data_preprocessor import DataPreprocessor
from ml_models import LSTMPredictor, LinearRegressionPredictor, ModelEvaluator
from visualizer import StockVisualizer


def main():
    """Main function to run stock market analysis."""
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Stock Market Analysis with ML Prediction',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze Apple stock with 2-year history
  python main.py --ticker AAPL --period 2y
  
  # Analyze Google stock and save results
  python main.py --ticker GOOGL --period 1y --save
  
  # Use Linear Regression instead of LSTM
  python main.py --ticker MSFT --model lr
        """
    )
    
    parser.add_argument('--ticker', type=str, default='AAPL',
                       help='Stock ticker symbol (default: AAPL)')
    parser.add_argument('--period', type=str, default='2y',
                       help='Time period to fetch (default: 2y)')
    parser.add_argument('--model', type=str, choices=['lstm', 'lr'], default='lstm',
                       help='ML model to use: lstm or lr (Linear Regression) (default: lstm)')
    parser.add_argument('--lookback', type=int, default=60,
                       help='Number of days to look back for prediction (default: 60)')
    parser.add_argument('--epochs', type=int, default=50,
                       help='Number of training epochs for LSTM (default: 50)')
    parser.add_argument('--save', action='store_true',
                       help='Save plots and model')
    parser.add_argument('--no-plot', action='store_true',
                       help='Skip plotting visualizations')
    
    args = parser.parse_args()
    
    print("="*70)
    print(f"Stock Market Analysis with ML Prediction".center(70))
    print("="*70)
    print()
    
    # Step 1: Fetch Data
    print(f"[1/6] Fetching data for {args.ticker}...")
    try:
        fetcher = StockDataFetcher(args.ticker)
        data = fetcher.fetch_data(period=args.period)
        print(f"✓ Successfully fetched {len(data)} days of data")
        
        # Display stock info
        info = fetcher.get_stock_info()
        print(f"\nStock Information:")
        print(f"  Name: {info.get('name', 'N/A')}")
        print(f"  Sector: {info.get('sector', 'N/A')}")
        print(f"  Current Price: ${info.get('current_price', 'N/A')}")
        print()
        
    except Exception as e:
        print(f"✗ Error fetching data: {e}")
        return
    
    # Step 2: Preprocess Data
    print("[2/6] Preprocessing data and adding technical indicators...")
    try:
        preprocessor = DataPreprocessor()
        data_with_indicators = preprocessor.add_technical_indicators(data)
        data_clean = preprocessor.handle_missing_data(data_with_indicators, method='drop')
        print(f"✓ Data preprocessed successfully")
        print(f"  Features added: MA7, MA21, MA50, MACD, RSI, Bollinger Bands, etc.")
        print()
    except Exception as e:
        print(f"✗ Error preprocessing data: {e}")
        return
    
    # Step 3: Prepare data for ML
    print("[3/6] Preparing data for machine learning...")
    try:
        X, y, scaler = preprocessor.prepare_data_for_lstm(data_clean, 'Close', args.lookback)
        X_train, X_test, y_train, y_test = preprocessor.split_data(X, y, train_ratio=0.8)
        print(f"✓ Data prepared successfully")
        print(f"  Training samples: {len(X_train)}")
        print(f"  Testing samples: {len(X_test)}")
        print(f"  Lookback period: {args.lookback} days")
        print()
    except Exception as e:
        print(f"✗ Error preparing data: {e}")
        return
    
    # Step 4: Train Model
    print(f"[4/6] Training {args.model.upper()} model...")
    try:
        if args.model == 'lstm':
            model = LSTMPredictor(lookback=args.lookback)
            print(f"  Training LSTM with {args.epochs} epochs...")
            history = model.train(X_train, y_train, epochs=args.epochs, verbose=0)
            print(f"✓ Model trained successfully")
            print(f"  Final loss: {history['loss'][-1]:.6f}")
        else:  # Linear Regression
            model = LinearRegressionPredictor()
            model.train(X_train, y_train)
            print(f"✓ Linear Regression model trained successfully")
        print()
    except Exception as e:
        print(f"✗ Error training model: {e}")
        return
    
    # Step 5: Make Predictions and Evaluate
    print("[5/6] Making predictions and evaluating performance...")
    try:
        # Make predictions
        train_predictions = model.predict(X_train)
        test_predictions = model.predict(X_test)
        
        # Inverse transform predictions
        train_predictions = preprocessor.inverse_scale(train_predictions)
        test_predictions = preprocessor.inverse_scale(test_predictions)
        y_train_actual = preprocessor.inverse_scale(y_train)
        y_test_actual = preprocessor.inverse_scale(y_test)
        
        # Calculate metrics
        evaluator = ModelEvaluator()
        train_metrics = evaluator.calculate_metrics(y_train_actual, train_predictions)
        test_metrics = evaluator.calculate_metrics(y_test_actual, test_predictions)
        
        print(f"✓ Predictions completed")
        evaluator.print_metrics(train_metrics, f"{args.model.upper()} Training")
        evaluator.print_metrics(test_metrics, f"{args.model.upper()} Testing")
        
    except Exception as e:
        print(f"✗ Error making predictions: {e}")
        return
    
    # Step 6: Visualize Results
    if not args.no_plot:
        print("[6/6] Creating visualizations...")
        try:
            visualizer = StockVisualizer()
            
            # Plot stock prices with moving averages
            visualizer.plot_with_moving_averages(
                data_clean.tail(365),
                title=f"{args.ticker} Stock Price with Moving Averages",
                save_path='plots/ma_plot.png' if args.save else None
            )
            
            # Plot technical indicators
            visualizer.plot_technical_indicators(
                data_clean.tail(365),
                save_path='plots/indicators_plot.png' if args.save else None
            )
            
            # Plot predictions
            # Prepare dates for test predictions
            test_dates = data_clean.index[-(len(y_test)):]
            visualizer.plot_predictions(
                test_dates,
                y_test_actual.flatten(),
                test_predictions.flatten(),
                title=f"{args.ticker} - {args.model.upper()} Predictions vs Actual",
                save_path='plots/predictions_plot.png' if args.save else None
            )
            
            # Plot training history for LSTM
            if args.model == 'lstm':
                visualizer.plot_training_history(
                    history,
                    save_path='plots/training_history.png' if args.save else None
                )
            
            print(f"✓ Visualizations created successfully")
            print()
            
        except Exception as e:
            print(f"✗ Error creating visualizations: {e}")
            return
    else:
        print("[6/6] Skipping visualizations (--no-plot flag used)")
        print()
    
    # Save model if requested
    if args.save:
        print("Saving model and data...")
        try:
            os.makedirs('models', exist_ok=True)
            os.makedirs('data', exist_ok=True)
            os.makedirs('plots', exist_ok=True)
            
            if args.model == 'lstm':
                model_path = f'models/{args.ticker}_lstm_model.h5'
                model.save_model(model_path)
                print(f"✓ Model saved to {model_path}")
            
            data_path = f'data/{args.ticker}_data.csv'
            fetcher.save_data(data_path)
            print(f"✓ Data saved to {data_path}")
            print()
            
        except Exception as e:
            print(f"✗ Error saving files: {e}")
            return
    
    print("="*70)
    print(f"Analysis Complete!".center(70))
    print("="*70)
    print()
    
    # Future predictions (next day)
    print("Future Prediction (Next Trading Day):")
    print("-" * 70)
    try:
        # Use the last lookback days to predict next day
        last_sequence = X_test[-1].reshape(1, args.lookback, 1)
        next_day_prediction = model.predict(last_sequence)
        next_day_price = preprocessor.inverse_scale(next_day_prediction)[0][0]
        current_price = y_test_actual[-1][0]
        change = next_day_price - current_price
        change_pct = (change / current_price) * 100
        
        print(f"Current Price: ${current_price:.2f}")
        print(f"Predicted Next Day Price: ${next_day_price:.2f}")
        print(f"Expected Change: ${change:.2f} ({change_pct:+.2f}%)")
        
        if change > 0:
            print("📈 Prediction: Price may go UP")
        else:
            print("📉 Prediction: Price may go DOWN")
        
    except Exception as e:
        print(f"Could not make future prediction: {e}")
    
    print("="*70)
    print()
    print("Note: This is for educational purposes only.")
    print("Always do your own research before making investment decisions.")
    print()


if __name__ == "__main__":
    main()
