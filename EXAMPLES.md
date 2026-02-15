# Example Usage of Stock Market Analysis

This document provides practical examples of using the stock market analysis system.

## Quick Start

### 1. Basic Analysis
Analyze Apple stock with default settings:
```bash
python main.py
```

This will:
- Fetch 2 years of AAPL data
- Add technical indicators
- Train an LSTM model with 50 epochs
- Display predictions and performance metrics
- Show visualizations

### 2. Custom Stock and Period
Analyze Tesla stock with 5 years of data:
```bash
python main.py --ticker TSLA --period 5y
```

### 3. Save Results
Save all plots, models, and data:
```bash
python main.py --ticker GOOGL --save
```

This creates:
- `models/GOOGL_lstm_model.h5` - Trained LSTM model
- `data/GOOGL_data.csv` - Historical stock data
- `plots/ma_plot.png` - Moving averages plot
- `plots/indicators_plot.png` - Technical indicators
- `plots/predictions_plot.png` - Predictions comparison
- `plots/training_history.png` - Training loss history

### 4. Use Linear Regression (Faster)
For quicker results with a simpler model:
```bash
python main.py --ticker MSFT --model lr
```

### 5. Adjust Training Parameters
Train with more epochs and a longer lookback:
```bash
python main.py --ticker AAPL --epochs 100 --lookback 90
```

### 6. Headless Mode (No Plots)
Run without displaying plots:
```bash
python main.py --ticker AAPL --no-plot --save
```

## Demo with Synthetic Data

Test the system without internet connection:
```bash
python demo.py
```

This demonstrates:
- Data preprocessing
- Feature engineering
- Model training (both LSTM and Linear Regression)
- Performance comparison
- All functionality with synthetic data

## Example Output

### Successful Analysis Output:
```
======================================================================
               Stock Market Analysis with ML Prediction               
======================================================================

[1/6] Fetching data for AAPL...
✓ Successfully fetched 504 days of data

Stock Information:
  Name: Apple Inc.
  Sector: Technology
  Current Price: $172.50

[2/6] Preprocessing data and adding technical indicators...
✓ Data preprocessed successfully
  Features added: MA7, MA21, MA50, MACD, RSI, Bollinger Bands, etc.

[3/6] Preparing data for machine learning...
✓ Data prepared successfully
  Training samples: 283
  Testing samples: 71
  Lookback period: 60 days

[4/6] Training LSTM model...
  Training LSTM with 50 epochs...
✓ Model trained successfully
  Final loss: 0.001234

[5/6] Making predictions and evaluating performance...
✓ Predictions completed

LSTM Testing Performance Metrics:
==================================================
Mean Squared Error (MSE): 12.345678
Root Mean Squared Error (RMSE): 3.513934
Mean Absolute Error (MAE): 2.718281
R² Score: 0.956789
Mean Absolute Percentage Error (MAPE): 1.85%
==================================================

[6/6] Creating visualizations...
✓ Visualizations created successfully

======================================================================
                            Analysis Complete!                            
======================================================================

Future Prediction (Next Trading Day):
----------------------------------------------------------------------
Current Price: $172.50
Predicted Next Day Price: $174.20
Expected Change: $1.70 (+0.99%)
📈 Prediction: Price may go UP
======================================================================
```

## Analyzing Multiple Stocks

Create a simple batch script:
```bash
#!/bin/bash
for ticker in AAPL GOOGL MSFT TSLA AMZN; do
  echo "Analyzing $ticker..."
  python main.py --ticker $ticker --save --no-plot
  echo "---"
done
```

## Interpreting Results

### Performance Metrics:

1. **RMSE (Root Mean Squared Error)**: Lower is better
   - < 5: Excellent
   - 5-10: Good
   - 10-20: Fair
   - > 20: Poor (for typical stock prices)

2. **MAPE (Mean Absolute Percentage Error)**: Lower is better
   - < 2%: Excellent
   - 2-5%: Good
   - 5-10%: Fair
   - > 10%: Poor

3. **R² Score**: Higher is better (0-1)
   - > 0.95: Excellent
   - 0.90-0.95: Good
   - 0.80-0.90: Fair
   - < 0.80: Poor

### Technical Indicators:

- **Moving Averages (MA)**: Trend indicators
  - Price above MA: Bullish signal
  - Price below MA: Bearish signal

- **RSI (Relative Strength Index)**:
  - > 70: Overbought (potential sell signal)
  - < 30: Oversold (potential buy signal)

- **MACD**: Momentum indicator
  - MACD above Signal Line: Bullish
  - MACD below Signal Line: Bearish

- **Bollinger Bands**:
  - Price near upper band: Potentially overbought
  - Price near lower band: Potentially oversold

## Tips for Better Results

1. **Longer Training Period**: Use 2-5 years for better patterns
   ```bash
   python main.py --ticker AAPL --period 5y
   ```

2. **More Training Epochs**: Increase for better convergence
   ```bash
   python main.py --ticker AAPL --epochs 100
   ```

3. **Adjust Lookback**: Try different lookback periods
   ```bash
   python main.py --ticker AAPL --lookback 90
   ```

4. **Compare Models**: Run both LSTM and Linear Regression
   ```bash
   python main.py --ticker AAPL --model lstm --save
   python main.py --ticker AAPL --model lr --save
   ```

## Troubleshooting

### Issue: "No data found for ticker"
**Solution**: Check if the ticker symbol is correct and active

### Issue: Training takes too long
**Solution**: 
- Reduce epochs: `--epochs 20`
- Use Linear Regression: `--model lr`
- Use shorter period: `--period 1y`

### Issue: Poor prediction accuracy
**Solutions**:
- Try longer training period: `--period 5y`
- Increase epochs: `--epochs 100`
- Adjust lookback: `--lookback 90`
- Note: Some stocks are harder to predict due to high volatility

## Important Reminders

⚠️ **This tool is for educational purposes only**
- Past performance ≠ future results
- Many factors affect stock prices
- Always do your own research
- Consult financial advisors before trading
- Never invest money you can't afford to lose
