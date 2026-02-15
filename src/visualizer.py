"""
Module for visualizing stock market data and predictions.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class StockVisualizer:
    """Class to create visualizations for stock market analysis."""
    
    def __init__(self, figsize: tuple = (14, 7)):
        """
        Initialize the visualizer.
        
        Args:
            figsize: Default figure size for plots
        """
        self.figsize = figsize
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def plot_stock_prices(self, data: pd.DataFrame, title: str = "Stock Prices", 
                         columns: list = None, save_path: str = None):
        """
        Plot stock price data.
        
        Args:
            data: DataFrame with stock data
            title: Plot title
            columns: List of columns to plot (default: ['Close'])
            save_path: Path to save the plot
        """
        if columns is None:
            columns = ['Close']
        
        plt.figure(figsize=self.figsize)
        
        for col in columns:
            if col in data.columns:
                plt.plot(data.index, data[col], label=col, linewidth=2)
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_with_moving_averages(self, data: pd.DataFrame, title: str = "Stock Price with Moving Averages",
                                  save_path: str = None):
        """
        Plot stock price with moving averages.
        
        Args:
            data: DataFrame with stock data including moving averages
            title: Plot title
            save_path: Path to save the plot
        """
        plt.figure(figsize=self.figsize)
        
        plt.plot(data.index, data['Close'], label='Close Price', linewidth=2, color='blue')
        
        if 'MA7' in data.columns:
            plt.plot(data.index, data['MA7'], label='7-Day MA', linewidth=1.5, alpha=0.7, color='orange')
        if 'MA21' in data.columns:
            plt.plot(data.index, data['MA21'], label='21-Day MA', linewidth=1.5, alpha=0.7, color='green')
        if 'MA50' in data.columns:
            plt.plot(data.index, data['MA50'], label='50-Day MA', linewidth=1.5, alpha=0.7, color='red')
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_predictions(self, dates: pd.DatetimeIndex, actual: np.ndarray, 
                        predicted: np.ndarray, title: str = "Actual vs Predicted Prices",
                        save_path: str = None):
        """
        Plot actual vs predicted stock prices.
        
        Args:
            dates: Date index for x-axis
            actual: Actual stock prices
            predicted: Predicted stock prices
            title: Plot title
            save_path: Path to save the plot
        """
        plt.figure(figsize=self.figsize)
        
        plt.plot(dates, actual, label='Actual Price', linewidth=2, color='blue')
        plt.plot(dates, predicted, label='Predicted Price', linewidth=2, color='red', alpha=0.7)
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_technical_indicators(self, data: pd.DataFrame, save_path: str = None):
        """
        Plot technical indicators.
        
        Args:
            data: DataFrame with stock data including technical indicators
            save_path: Path to save the plot
        """
        fig, axes = plt.subplots(3, 1, figsize=(14, 12))
        
        # Plot 1: Price with Bollinger Bands
        axes[0].plot(data.index, data['Close'], label='Close Price', linewidth=2, color='blue')
        if 'BB_upper' in data.columns and 'BB_lower' in data.columns:
            axes[0].plot(data.index, data['BB_upper'], label='Upper BB', linewidth=1, 
                        linestyle='--', color='red', alpha=0.7)
            axes[0].plot(data.index, data['BB_lower'], label='Lower BB', linewidth=1, 
                        linestyle='--', color='red', alpha=0.7)
            axes[0].fill_between(data.index, data['BB_lower'], data['BB_upper'], alpha=0.1, color='gray')
        axes[0].set_title('Price with Bollinger Bands', fontsize=14, fontweight='bold')
        axes[0].set_ylabel('Price ($)', fontsize=12)
        axes[0].legend(loc='best')
        axes[0].grid(True, alpha=0.3)
        
        # Plot 2: MACD
        if 'MACD' in data.columns and 'Signal_Line' in data.columns:
            axes[1].plot(data.index, data['MACD'], label='MACD', linewidth=2, color='blue')
            axes[1].plot(data.index, data['Signal_Line'], label='Signal Line', linewidth=2, color='red')
            axes[1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
            axes[1].set_title('MACD (Moving Average Convergence Divergence)', fontsize=14, fontweight='bold')
            axes[1].set_ylabel('MACD', fontsize=12)
            axes[1].legend(loc='best')
            axes[1].grid(True, alpha=0.3)
        
        # Plot 3: RSI
        if 'RSI' in data.columns:
            axes[2].plot(data.index, data['RSI'], label='RSI', linewidth=2, color='purple')
            axes[2].axhline(y=70, color='red', linestyle='--', linewidth=1, label='Overbought (70)')
            axes[2].axhline(y=30, color='green', linestyle='--', linewidth=1, label='Oversold (30)')
            axes[2].set_title('RSI (Relative Strength Index)', fontsize=14, fontweight='bold')
            axes[2].set_xlabel('Date', fontsize=12)
            axes[2].set_ylabel('RSI', fontsize=12)
            axes[2].legend(loc='best')
            axes[2].grid(True, alpha=0.3)
            axes[2].set_ylim(0, 100)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_training_history(self, history: dict, save_path: str = None):
        """
        Plot model training history.
        
        Args:
            history: Training history dictionary
            save_path: Path to save the plot
        """
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(history['loss'], label='Training Loss', linewidth=2)
        if 'val_loss' in history:
            plt.plot(history['val_loss'], label='Validation Loss', linewidth=2)
        plt.title('Model Loss', fontsize=14, fontweight='bold')
        plt.xlabel('Epoch', fontsize=12)
        plt.ylabel('Loss', fontsize=12)
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_volume(self, data: pd.DataFrame, title: str = "Trading Volume", 
                   save_path: str = None):
        """
        Plot trading volume.
        
        Args:
            data: DataFrame with stock data including Volume
            title: Plot title
            save_path: Path to save the plot
        """
        if 'Volume' not in data.columns:
            print("Volume data not available.")
            return
        
        plt.figure(figsize=self.figsize)
        
        plt.bar(data.index, data['Volume'], label='Volume', color='steelblue', alpha=0.7)
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Volume', fontsize=12)
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
