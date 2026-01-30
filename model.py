"""
Deep Learning Model for Gold Price Prediction
Uses LSTM neural network to predict price direction
"""
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import pickle
import os


class GoldPricePredictor:
    """LSTM-based model for gold price prediction"""
    
    def __init__(self, sequence_length=60):
        self.sequence_length = sequence_length
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.is_trained = False
    
    def build_model(self, input_shape):
        """Build LSTM model architecture"""
        model = Sequential([
            LSTM(units=50, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(units=50, return_sequences=True),
            Dropout(0.2),
            LSTM(units=50),
            Dropout(0.2),
            Dense(units=25),
            Dense(units=1)
        ])
        
        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
        self.model = model
        return model
    
    def prepare_data(self, prices):
        """Prepare price data for training/prediction"""
        if isinstance(prices, list):
            prices = np.array(prices).reshape(-1, 1)
        elif isinstance(prices, pd.Series):
            prices = prices.values.reshape(-1, 1)
        elif isinstance(prices, np.ndarray) and prices.ndim == 1:
            prices = prices.reshape(-1, 1)
        
        # Scale the data
        scaled_data = self.scaler.fit_transform(prices)
        
        # Create sequences
        X, y = [], []
        for i in range(self.sequence_length, len(scaled_data)):
            X.append(scaled_data[i-self.sequence_length:i, 0])
            y.append(scaled_data[i, 0])
        
        return np.array(X), np.array(y)
    
    def train(self, prices, epochs=50, batch_size=32):
        """Train the model on historical price data"""
        X, y = self.prepare_data(prices)
        
        # Reshape for LSTM
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        
        # Build model if not exists
        if self.model is None:
            self.build_model((X.shape[1], 1))
        
        # Train
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            verbose=1
        )
        
        self.is_trained = True
        return history
    
    def predict_next(self, recent_prices):
        """Predict next price value"""
        if not self.is_trained or self.model is None:
            raise ValueError("Model must be trained before prediction")
        
        # Prepare input
        if isinstance(recent_prices, list):
            recent_prices = np.array(recent_prices).reshape(-1, 1)
        elif isinstance(recent_prices, np.ndarray) and recent_prices.ndim == 1:
            recent_prices = recent_prices.reshape(-1, 1)
        
        scaled_prices = self.scaler.transform(recent_prices[-self.sequence_length:])
        X_test = np.reshape(scaled_prices, (1, self.sequence_length, 1))
        
        # Predict
        predicted_scaled = self.model.predict(X_test, verbose=0)
        predicted_price = self.scaler.inverse_transform(predicted_scaled)[0][0]
        
        return predicted_price
    
    def predict_direction(self, recent_prices):
        """Predict if price will go up or down"""
        if len(recent_prices) < self.sequence_length + 1:
            return None
        
        current_price = recent_prices[-1]
        predicted_price = self.predict_next(recent_prices)
        
        direction = "UP" if predicted_price > current_price else "DOWN"
        confidence = abs(predicted_price - current_price) / current_price * 100
        
        return {
            'current_price': float(current_price),
            'predicted_price': float(predicted_price),
            'direction': direction,
            'confidence': float(confidence),
            'change': float(predicted_price - current_price)
        }
    
    def save_model(self, filepath='gold_model.h5'):
        """Save trained model"""
        if self.model:
            self.model.save(filepath)
            # Save scaler
            with open(filepath.replace('.h5', '_scaler.pkl'), 'wb') as f:
                pickle.dump(self.scaler, f)
    
    def load_model(self, filepath='gold_model.h5'):
        """Load trained model"""
        if os.path.exists(filepath):
            self.model = keras.models.load_model(filepath)
            # Load scaler
            scaler_path = filepath.replace('.h5', '_scaler.pkl')
            if os.path.exists(scaler_path):
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
            self.is_trained = True
            return True
        return False


def generate_sample_data(n_points=1000):
    """Generate sample gold price data for training"""
    np.random.seed(42)
    
    # Simulate gold price with trend and seasonality
    time = np.arange(n_points)
    trend = 1800 + time * 0.2  # Upward trend
    seasonality = 100 * np.sin(2 * np.pi * time / 365)  # Yearly pattern
    noise = np.random.normal(0, 20, n_points)  # Random noise
    
    prices = trend + seasonality + noise
    return prices


if __name__ == "__main__":
    # Demo: Train on sample data
    print("Generating sample data...")
    sample_prices = generate_sample_data(1000)
    
    print("Training model...")
    predictor = GoldPricePredictor(sequence_length=60)
    predictor.train(sample_prices, epochs=10)
    
    print("Making prediction...")
    prediction = predictor.predict_direction(sample_prices[-100:])
    print(f"Prediction: {prediction}")
    
    print("Saving model...")
    predictor.save_model()
    print("Done!")
