"""
Module for preprocessing stock market data and feature engineering.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class DataPreprocessor:
    """Class to preprocess stock market data for ML models."""
    
    def __init__(self):
        """Initialize the preprocessor with a scaler."""
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaled_data = None
        self.original_shape = None
    
    def add_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Add technical indicators to the data.
        
        Args:
            data: DataFrame with stock data
        
        Returns:
            DataFrame with additional technical indicator columns
        """
        df = data.copy()
        
        # Moving Averages
        df['MA7'] = df['Close'].rolling(window=7).mean()
        df['MA21'] = df['Close'].rolling(window=21).mean()
        df['MA50'] = df['Close'].rolling(window=50).mean()
        
        # Exponential Moving Averages
        df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
        
        # MACD (Moving Average Convergence Divergence)
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        # RSI (Relative Strength Index)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['BB_middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_upper'] = df['BB_middle'] + (bb_std * 2)
        df['BB_lower'] = df['BB_middle'] - (bb_std * 2)
        
        # Volatility
        df['Volatility'] = df['Close'].pct_change().rolling(window=20).std()
        
        # Daily Returns
        df['Daily_Return'] = df['Close'].pct_change()
        
        return df
    
    def prepare_data_for_lstm(self, data: pd.DataFrame, column: str = 'Close', 
                              lookback: int = 60) -> tuple:
        """
        Prepare data for LSTM model training.
        
        Args:
            data: DataFrame with stock data
            column: Column to use for prediction
            lookback: Number of previous time steps to use as input
        
        Returns:
            Tuple of (X_train, y_train, scaler)
        """
        # Get the column data
        dataset = data[column].values.reshape(-1, 1)
        
        # Scale the data
        scaled_data = self.scaler.fit_transform(dataset)
        self.scaled_data = scaled_data
        self.original_shape = dataset.shape
        
        # Create sequences
        X, y = [], []
        for i in range(lookback, len(scaled_data)):
            X.append(scaled_data[i-lookback:i, 0])
            y.append(scaled_data[i, 0])
        
        X, y = np.array(X), np.array(y)
        
        # Reshape for LSTM [samples, time steps, features]
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        
        return X, y, self.scaler
    
    def split_data(self, X: np.ndarray, y: np.ndarray, 
                   train_ratio: float = 0.8) -> tuple:
        """
        Split data into training and testing sets.
        
        Args:
            X: Input features
            y: Target values
            train_ratio: Ratio of training data (0-1)
        
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        split_idx = int(len(X) * train_ratio)
        
        X_train = X[:split_idx]
        X_test = X[split_idx:]
        y_train = y[:split_idx]
        y_test = y[split_idx:]
        
        return X_train, X_test, y_train, y_test
    
    def inverse_scale(self, scaled_data: np.ndarray) -> np.ndarray:
        """
        Inverse transform scaled data back to original scale.
        
        Args:
            scaled_data: Scaled data to transform
        
        Returns:
            Data in original scale
        """
        return self.scaler.inverse_transform(scaled_data.reshape(-1, 1))
    
    def handle_missing_data(self, data: pd.DataFrame, method: str = 'ffill') -> pd.DataFrame:
        """
        Handle missing data in the dataset.
        
        Args:
            data: DataFrame with potential missing values
            method: Method to handle missing data ('ffill', 'bfill', 'interpolate', 'drop')
        
        Returns:
            DataFrame with missing data handled
        """
        df = data.copy()
        
        if method == 'ffill':
            df = df.ffill()
        elif method == 'bfill':
            df = df.bfill()
        elif method == 'interpolate':
            df = df.interpolate(method='linear')
        elif method == 'drop':
            df = df.dropna()
        else:
            raise ValueError(f"Unknown method: {method}")
        
        return df
