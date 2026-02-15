"""
Unit tests for the stock market analysis modules.
"""

import unittest
import numpy as np
import pandas as pd
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_preprocessor import DataPreprocessor
from ml_models import LSTMPredictor, LinearRegressionPredictor, ModelEvaluator


class TestDataPreprocessor(unittest.TestCase):
    """Test cases for DataPreprocessor class."""
    
    def setUp(self):
        """Set up test data."""
        self.preprocessor = DataPreprocessor()
        
        # Create synthetic data
        dates = pd.date_range(end=pd.Timestamp.now(), periods=100, freq='D')
        self.test_data = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 100),
            'High': np.random.uniform(100, 200, 100),
            'Low': np.random.uniform(100, 200, 100),
            'Close': np.random.uniform(100, 200, 100),
            'Volume': np.random.randint(1000000, 10000000, 100)
        }, index=dates)
    
    def test_add_technical_indicators(self):
        """Test adding technical indicators."""
        result = self.preprocessor.add_technical_indicators(self.test_data)
        
        # Check that indicators were added
        self.assertIn('MA7', result.columns)
        self.assertIn('MA21', result.columns)
        self.assertIn('RSI', result.columns)
        self.assertIn('MACD', result.columns)
        self.assertIn('BB_upper', result.columns)
    
    def test_prepare_data_for_lstm(self):
        """Test LSTM data preparation."""
        lookback = 10
        X, y, scaler = self.preprocessor.prepare_data_for_lstm(
            self.test_data, 'Close', lookback
        )
        
        # Check shapes
        self.assertEqual(X.shape[1], lookback)
        self.assertEqual(X.shape[2], 1)
        self.assertEqual(len(y), len(X))
    
    def test_split_data(self):
        """Test data splitting."""
        X = np.random.rand(100, 10, 1)
        y = np.random.rand(100)
        
        X_train, X_test, y_train, y_test = self.preprocessor.split_data(
            X, y, train_ratio=0.8
        )
        
        # Check split ratios
        self.assertEqual(len(X_train), 80)
        self.assertEqual(len(X_test), 20)
    
    def test_handle_missing_data(self):
        """Test missing data handling."""
        # Create data with missing values
        data_with_nan = self.test_data.copy()
        data_with_nan.loc[data_with_nan.index[5], 'Close'] = np.nan
        
        result = self.preprocessor.handle_missing_data(data_with_nan, method='ffill')
        
        # Check that no NaN values remain
        self.assertEqual(result['Close'].isna().sum(), 0)


class TestMLModels(unittest.TestCase):
    """Test cases for ML models."""
    
    def setUp(self):
        """Set up test data."""
        # Create synthetic training data
        np.random.seed(42)
        self.X_train = np.random.rand(100, 10, 1)
        self.y_train = np.random.rand(100)
        self.X_test = np.random.rand(20, 10, 1)
        self.y_test = np.random.rand(20)
    
    def test_lstm_build_model(self):
        """Test LSTM model building."""
        lstm = LSTMPredictor(lookback=10)
        model = lstm.build_model((10, 1))
        
        self.assertIsNotNone(model)
        # Check that the model has LSTM and Dense layers
        layer_types = [type(layer).__name__ for layer in model.layers]
        self.assertIn('LSTM', layer_types)
        self.assertIn('Dense', layer_types)
    
    def test_lstm_train(self):
        """Test LSTM model training."""
        lstm = LSTMPredictor(lookback=10)
        history = lstm.train(self.X_train, self.y_train, epochs=2, verbose=0)
        
        self.assertIn('loss', history)
        self.assertEqual(len(history['loss']), 2)
    
    def test_linear_regression_train(self):
        """Test Linear Regression training."""
        lr = LinearRegressionPredictor()
        lr.train(self.X_train, self.y_train)
        
        self.assertIsNotNone(lr.model)
    
    def test_model_evaluator(self):
        """Test model evaluation metrics."""
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.1, 2.1, 2.9, 4.2, 4.8])
        
        metrics = ModelEvaluator.calculate_metrics(y_true, y_pred)
        
        # Check that all metrics are present
        self.assertIn('MSE', metrics)
        self.assertIn('RMSE', metrics)
        self.assertIn('MAE', metrics)
        self.assertIn('R2', metrics)
        self.assertIn('MAPE', metrics)
        
        # Check that metrics are reasonable
        self.assertGreater(metrics['R2'], 0.9)  # Should be high for good predictions


if __name__ == '__main__':
    unittest.main()
