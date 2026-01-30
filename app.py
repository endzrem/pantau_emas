"""
Flask Web Application for Gold Price Monitoring and Prediction
"""
from flask import Flask, render_template, jsonify, request
from scraper import GoldPriceScraper
from model import GoldPricePredictor, generate_sample_data
import json
from datetime import datetime
import os
import threading
import time

app = Flask(__name__)

# Initialize scraper and predictor
scraper = GoldPriceScraper()
predictor = GoldPricePredictor(sequence_length=60)

# Store recent prices in memory (in production, use database)
price_history = []
max_history = 1000
price_history_lock = threading.Lock()  # Thread-safe access to price_history

# Load or train model
model_path = 'gold_model.h5'
if not predictor.load_model(model_path):
    print("Training new model with sample data...")
    sample_data = generate_sample_data(1000)
    predictor.train(sample_data, epochs=10)
    predictor.save_model(model_path)
    print("Model trained and saved!")


def update_prices_periodically():
    """Background thread to update prices periodically"""
    while True:
        try:
            price_data = scraper.get_current_price()
            with price_history_lock:
                price_history.append(price_data)
                
                # Keep only recent history
                if len(price_history) > max_history:
                    price_history.pop(0)
            
            print(f"Updated price: ${price_data['price']} at {price_data['timestamp']}")
        except Exception as e:
            print(f"Error updating prices: {e}")
        
        # Update every 60 seconds
        time.sleep(60)


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/current-price')
def get_current_price():
    """API endpoint to get current gold price"""
    # Return the most recent price from history if available
    with price_history_lock:
        if price_history:
            return jsonify(price_history[-1])
    
    # Otherwise fetch a new price
    price_data = scraper.get_current_price()
    return jsonify(price_data)


@app.route('/api/price-history')
def get_price_history():
    """API endpoint to get price history"""
    limit = request.args.get('limit', 100, type=int)
    # Validate and constrain limit
    limit = min(max(1, limit), 1000)
    
    with price_history_lock:
        return jsonify(price_history[-limit:])


@app.route('/api/predict')
def predict_price():
    """API endpoint to get price prediction"""
    try:
        with price_history_lock:
            if len(price_history) < 60:
                return jsonify({
                    'error': 'Not enough historical data for prediction',
                    'message': 'Need at least 60 data points'
                }), 400
            
            # Extract prices from history
            prices = [p['price'] for p in price_history]
        
        # Get prediction
        prediction = predictor.predict_direction(prices)
        
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/train-model', methods=['POST'])
def train_model():
    """API endpoint to retrain model with current history
    Note: In production, add authentication and rate limiting to this endpoint"""
    try:
        with price_history_lock:
            if len(price_history) < 100:
                return jsonify({
                    'error': 'Not enough data to train model',
                    'message': 'Need at least 100 data points'
                }), 400
            
            prices = [p['price'] for p in price_history]
        
        predictor.train(prices, epochs=20, verbose=0)
        predictor.save_model(model_path)
        
        return jsonify({
            'message': 'Model trained successfully',
            'data_points': len(prices)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Start background price update thread
    update_thread = threading.Thread(target=update_prices_periodically, daemon=True)
    update_thread.start()
    
    # Run Flask app
    # WARNING: Debug mode is enabled for development only
    # For production deployment:
    # 1. Set debug=False
    # 2. Use a production WSGI server like Gunicorn: gunicorn -w 4 app:app
    # 3. Set up proper authentication for admin endpoints
    # 4. Configure HTTPS
    debug_mode = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
