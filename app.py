"""
Flask Web Application for Gold Price Monitoring and Prediction
"""
from flask import Flask, render_template, jsonify, request
from scraper import GoldPriceScraper
from model import GoldPricePredictor, generate_sample_data
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
price_history_lock = threading.Lock()

# Model path (Render filesystem is ephemeral but OK for demo)
model_path = "gold_model.h5"

# Load or train model (DO NOT retrain every startup if model exists)
if not predictor.load_model(model_path):
    print("No saved model found. Training with sample data...")
    sample_data = generate_sample_data(1000)
    predictor.train(sample_data, epochs=10)
    predictor.save_model(model_path)
    print("Model trained and saved.")


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

        time.sleep(60)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/current-price")
def get_current_price():
    with price_history_lock:
        if price_history:
            return jsonify(price_history[-1])

    price_data = scraper.get_current_price()
    return jsonify(price_data)


@app.route("/api/price-history")
def get_price_history():
    limit = request.args.get("limit", 100, type=int)
    limit = min(max(1, limit), 1000)

    with price_history_lock:
        return jsonify(price_history[-limit:])


@app.route("/api/predict")
def predict_price():
    try:
        with price_history_lock:
            if len(price_history) < 60:
                return jsonify({
                    "error": "Not enough historical data",
                    "message": "Need at least 60 data points"
                }), 400

            prices = [p["price"] for p in price_history]

        prediction = predictor.predict_direction(prices)
        return jsonify(prediction)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/train-model", methods=["POST"])
def train_model():
    """Manual retraining endpoint (protect in real production)"""
    try:
        with price_history_lock:
            if len(price_history) < 100:
                return jsonify({
                    "error": "Not enough data",
                    "message": "Need at least 100 data points"
                }), 400

            prices = [p["price"] for p in price_history]

        predictor.train(prices, epochs=20, verbose=0)
        predictor.save_model(model_path)

        return jsonify({
            "message": "Model retrained successfully",
            "data_points": len(prices)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Start background thread
    update_thread = threading.Thread(
        target=update_prices_periodically,
        daemon=True
    )
    update_thread.start()

    # Render-compatible PORT handling
    port = int(os.environ.get("PORT", 5000))

    # Disable debug in production
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
