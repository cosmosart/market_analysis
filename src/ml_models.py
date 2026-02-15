"""
Module for ML prediction models for stock market analysis.
"""

import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os


class LSTMPredictor:
    """LSTM model for stock price prediction."""
    
    def __init__(self, lookback: int = 60):
        """
        Initialize LSTM predictor.
        
        Args:
            lookback: Number of previous time steps to use as input
        """
        self.lookback = lookback
        self.model = None
        self.history = None
    
    def build_model(self, input_shape: tuple) -> Sequential:
        """
        Build LSTM model architecture.
        
        Args:
            input_shape: Shape of input data (time_steps, features)
        
        Returns:
            Compiled LSTM model
        """
        model = Sequential([
            LSTM(units=50, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(units=50, return_sequences=True),
            Dropout(0.2),
            LSTM(units=50, return_sequences=False),
            Dropout(0.2),
            Dense(units=25),
            Dense(units=1)
        ])
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        self.model = model
        return model
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray, 
              epochs: int = 50, batch_size: int = 32, 
              validation_split: float = 0.1, verbose: int = 1) -> dict:
        """
        Train the LSTM model.
        
        Args:
            X_train: Training input data
            y_train: Training target data
            epochs: Number of training epochs
            batch_size: Batch size for training
            validation_split: Validation split ratio
            verbose: Verbosity mode
        
        Returns:
            Training history
        """
        if self.model is None:
            self.build_model((X_train.shape[1], X_train.shape[2]))
        
        self.history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=verbose
        )
        
        return self.history.history
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions using the trained model.
        
        Args:
            X: Input data for prediction
        
        Returns:
            Predicted values
        """
        if self.model is None:
            raise ValueError("Model not trained. Train the model first.")
        
        return self.model.predict(X)
    
    def save_model(self, filepath: str):
        """
        Save the trained model.
        
        Args:
            filepath: Path to save the model
        """
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")
        
        self.model.save(filepath)
    
    def load_model(self, filepath: str):
        """
        Load a saved model.
        
        Args:
            filepath: Path to the saved model
        """
        self.model = keras.models.load_model(filepath)


class LinearRegressionPredictor:
    """Linear Regression model for stock price prediction (baseline)."""
    
    def __init__(self):
        """Initialize Linear Regression predictor."""
        self.model = LinearRegression()
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Train the Linear Regression model.
        
        Args:
            X_train: Training input data
            y_train: Training target data
        """
        # Reshape if needed
        if len(X_train.shape) == 3:
            X_train = X_train.reshape(X_train.shape[0], -1)
        
        self.model.fit(X_train, y_train)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions using the trained model.
        
        Args:
            X: Input data for prediction
        
        Returns:
            Predicted values
        """
        # Reshape if needed
        if len(X.shape) == 3:
            X = X.reshape(X.shape[0], -1)
        
        return self.model.predict(X)


class ModelEvaluator:
    """Class to evaluate model performance."""
    
    @staticmethod
    def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
        """
        Calculate evaluation metrics.
        
        Args:
            y_true: True values
            y_pred: Predicted values
        
        Returns:
            Dictionary containing evaluation metrics
        """
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        # Calculate MAPE (Mean Absolute Percentage Error)
        # Avoid division by zero
        mask = y_true != 0
        mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
        
        return {
            'MSE': mse,
            'RMSE': rmse,
            'MAE': mae,
            'R2': r2,
            'MAPE': mape
        }
    
    @staticmethod
    def print_metrics(metrics: dict, model_name: str = "Model"):
        """
        Print evaluation metrics.
        
        Args:
            metrics: Dictionary containing metrics
            model_name: Name of the model
        """
        print(f"\n{model_name} Performance Metrics:")
        print(f"{'='*50}")
        print(f"Mean Squared Error (MSE): {metrics['MSE']:.6f}")
        print(f"Root Mean Squared Error (RMSE): {metrics['RMSE']:.6f}")
        print(f"Mean Absolute Error (MAE): {metrics['MAE']:.6f}")
        print(f"R² Score: {metrics['R2']:.6f}")
        print(f"Mean Absolute Percentage Error (MAPE): {metrics['MAPE']:.2f}%")
        print(f"{'='*50}\n")
