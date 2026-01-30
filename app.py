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
# Changed to store data per source
price_history_by_source = {
    'goldprice': [],
    'emasku': []
}
max_history = 50000  # Increased to allow continuous tracking (up to 50k data points)
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
    """Background thread to update prices periodically from all sources"""
    while True:
        try:
            # Get prices from all sources
            all_prices = scraper.get_all_sources()
            
            with price_history_lock:
                # Update goldprice history
                if 'goldprice' in all_prices:
                    price_history_by_source['goldprice'].append(all_prices['goldprice'])
                    if len(price_history_by_source['goldprice']) > max_history:
                        price_history_by_source['goldprice'].pop(0)
                    print(f"Updated goldprice: ${all_prices['goldprice']['price']} at {all_prices['goldprice']['timestamp']}")
                
                # Update emasku history
                if 'emasku' in all_prices:
                    price_history_by_source['emasku'].append(all_prices['emasku'])
                    if len(price_history_by_source['emasku']) > max_history:
                        price_history_by_source['emasku'].pop(0)
                    print(f"Updated emasku: Rp{all_prices['emasku']['price']} at {all_prices['emasku']['timestamp']}")
        except Exception as e:
            print(f"Error updating prices: {e}")

        SCRAPE_INTERVAL = int(os.environ.get("SCRAPE_INTERVAL", 60))
        time.sleep(SCRAPE_INTERVAL)



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/current-price")
def get_current_price():
    """Get current price from primary source (goldprice.org)"""
    with price_history_lock:
        if price_history_by_source['goldprice']:
            return jsonify(price_history_by_source['goldprice'][-1])

    price_data = scraper.get_current_price()
    return jsonify(price_data)


@app.route("/api/current-prices-all")
def get_current_prices_all():
    """Get current prices from all sources"""
    with price_history_lock:
        result = {}
        for source_name, history in price_history_by_source.items():
            if history:
                result[source_name] = history[-1]
        return jsonify(result)


@app.route("/api/price-history")
def get_price_history():
    """Get price history from primary source (backward compatibility)"""
    limit = request.args.get("limit", 1000, type=int)
    limit = min(max(1, limit), max_history)

    with price_history_lock:
        return jsonify(price_history_by_source['goldprice'][-limit:])


@app.route("/api/price-history-all")
def get_price_history_all():
    """Get price history from all sources"""
    limit = request.args.get("limit", 1000, type=int)
    limit = min(max(1, limit), max_history)

    with price_history_lock:
        result = {}
        for source_name, history in price_history_by_source.items():
            result[source_name] = history[-limit:]
        return jsonify(result)


@app.route("/api/predict")
def predict_price():
    """API endpoint to get price prediction"""
    try:
        with price_history_lock:
            if len(price_history_by_source['goldprice']) < 60:
                return jsonify({
                    "error": "Not enough historical data",
                    "message": "Need at least 60 data points"
                }), 400

            prices = [p["price"] for p in price_history_by_source['goldprice']]

        prediction = predictor.predict_direction(prices)
        return jsonify(prediction)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/train-model", methods=["POST"])
def train_model():
    """Manual retraining endpoint (protect in real production)"""
    try:
        with price_history_lock:
            if len(price_history_by_source['goldprice']) < 100:
                return jsonify({
                    "error": "Not enough data",
                    "message": "Need at least 100 data points"
                }), 400

            prices = [p["price"] for p in price_history_by_source['goldprice']]

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
