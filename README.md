# Stock Market Analysis with ML Prediction

A comprehensive Python application for stock market analysis using machine learning models to predict future stock prices. The project implements LSTM (Long Short-Term Memory) neural networks and Linear Regression models for time series prediction, along with technical indicators and data visualization.

## Features

- 📈 **Stock Data Fetching**: Automatically fetch historical stock data from Yahoo Finance
- 🔧 **Technical Indicators**: Calculate popular indicators including:
  - Moving Averages (MA7, MA21, MA50)
  - Exponential Moving Averages (EMA12, EMA26)
  - MACD (Moving Average Convergence Divergence)
  - RSI (Relative Strength Index)
  - Bollinger Bands
  - Volatility and Daily Returns
- 🤖 **ML Models**: 
  - LSTM Neural Network for time series prediction
  - Linear Regression as baseline model
- 📊 **Visualizations**: Multiple plot types for data analysis
- 📉 **Performance Metrics**: Comprehensive model evaluation (MSE, RMSE, MAE, R², MAPE)
- 💾 **Save/Load**: Save trained models and data for future use

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/cosmosart/market_analysis.git
cd market_analysis
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Analyze a stock with default settings (AAPL, 2-year history, LSTM model):
```bash
python main.py
```

### Custom Stock Analysis

Analyze a specific stock ticker:
```bash
python main.py --ticker GOOGL --period 1y
```

### Choose Different Models

Use Linear Regression instead of LSTM:
```bash
python main.py --ticker MSFT --model lr
```

### Save Results

Save plots, models, and data:
```bash
python main.py --ticker AAPL --save
```

### Advanced Options

```bash
python main.py --ticker TSLA --period 5y --lookback 90 --epochs 100 --save
```

### Command-Line Arguments

- `--ticker`: Stock ticker symbol (default: AAPL)
- `--period`: Time period to fetch (1mo, 3mo, 6mo, 1y, 2y, 5y, max) (default: 2y)
- `--model`: ML model to use (lstm, lr) (default: lstm)
- `--lookback`: Number of days to look back for prediction (default: 60)
- `--epochs`: Number of training epochs for LSTM (default: 50)
- `--save`: Save plots, models, and data
- `--no-plot`: Skip creating visualizations

## Examples

### Example 1: Quick Analysis
```bash
python main.py --ticker AAPL
```

### Example 2: Long-term Analysis with Saving
```bash
python main.py --ticker GOOGL --period 5y --epochs 100 --save
```

### Example 3: Multiple Stocks Analysis
```bash
python main.py --ticker AAPL --save
python main.py --ticker GOOGL --save
python main.py --ticker MSFT --save
```

### Example 4: Baseline Model Comparison
```bash
python main.py --ticker TSLA --model lr
```

## Project Structure

```
market_analysis/
├── main.py                      # Main application script
├── requirements.txt             # Python dependencies
├── README.md                    # Documentation
├── src/                         # Source code modules
│   ├── __init__.py
│   ├── data_fetcher.py         # Stock data fetching
│   ├── data_preprocessor.py    # Data preprocessing & feature engineering
│   ├── ml_models.py            # ML prediction models
│   └── visualizer.py           # Visualization functions
├── data/                        # Stored stock data (created when --save is used)
├── models/                      # Saved ML models (created when --save is used)
└── plots/                       # Generated plots (created when --save is used)
```

## How It Works

1. **Data Fetching**: The application fetches historical stock data from Yahoo Finance using the `yfinance` library.

2. **Preprocessing**: 
   - Adds technical indicators (MA, EMA, MACD, RSI, Bollinger Bands)
   - Handles missing data
   - Normalizes data using MinMaxScaler

3. **Feature Engineering**: Creates sequences of historical data to predict future prices using a sliding window approach.

4. **Model Training**:
   - **LSTM**: Deep learning model with multiple LSTM layers and dropout for regularization
   - **Linear Regression**: Simple baseline model for comparison

5. **Prediction & Evaluation**: Makes predictions on test data and calculates performance metrics.

6. **Visualization**: Creates multiple plots to visualize stock prices, technical indicators, and predictions.

## Model Performance

The LSTM model typically achieves:
- **MAPE**: 2-5% on well-behaved stocks
- **R² Score**: 0.95+ on test data

Performance varies based on:
- Stock volatility
- Training period length
- Model hyperparameters (epochs, lookback window)

## Technical Indicators Explained

- **Moving Averages (MA)**: Average price over a specific period
- **MACD**: Momentum indicator showing relationship between two moving averages
- **RSI**: Measures speed and magnitude of price changes (0-100 scale)
- **Bollinger Bands**: Volatility bands around a moving average

## Limitations & Disclaimer

⚠️ **Important Notes**:

- This project is for **educational purposes only**
- Past performance does not guarantee future results
- Stock markets are influenced by many factors not captured in historical price data
- Always conduct thorough research and consult financial advisors before making investment decisions
- The predictions should not be used as the sole basis for trading decisions

## Dependencies

- **numpy**: Numerical computing
- **pandas**: Data manipulation and analysis
- **matplotlib**: Data visualization
- **scikit-learn**: Machine learning utilities and metrics
- **yfinance**: Yahoo Finance data fetching
- **tensorflow**: Deep learning framework for LSTM

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms specified in the LICENSE file.

## Acknowledgments

- Data provided by Yahoo Finance via the `yfinance` library
- Built with TensorFlow/Keras for deep learning capabilities

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

---

**Remember**: This tool is for educational and research purposes. Always do your own research and never invest money you cannot afford to lose.