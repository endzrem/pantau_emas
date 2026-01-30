# Pantau Emas 📊

Real-Time Gold Price Monitoring and AI-Powered Prediction System

## Overview

Pantau Emas is a web application that monitors gold prices in real-time and uses deep learning (LSTM neural networks) to predict whether the price will go up or down. The system includes:

- **Real-time Price Scraping**: Fetches live gold prices from multiple sources
- **Interactive Web Dashboard**: Beautiful UI showing current prices, historical charts, and statistics
- **Deep Learning Predictions**: LSTM-based model predicts price direction (up/down)
- **RESTful API**: Clean API endpoints for integration

## Features

✨ **Live Gold Price**: Real-time gold price updates from web scraping
📈 **Interactive Charts**: Beautiful Plotly-based charts showing price history
🤖 **AI Predictions**: Deep learning model predicts price trends
📊 **Statistics Dashboard**: 24h high/low, averages, and data points
🔄 **Auto-refresh**: Automatic price updates every 60 seconds
📱 **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Deep Learning**: TensorFlow/Keras with LSTM architecture
- **Web Scraping**: BeautifulSoup4 + Requests
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Plotly.js for interactive visualizations
- **Data Processing**: Pandas, NumPy, scikit-learn

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/endzrem/pantau_emas.git
   cd pantau_emas
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## Project Structure

```
pantau_emas/
├── app.py                  # Flask web application
├── model.py                # Deep learning LSTM model
├── scraper.py              # Gold price web scraper
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Main web page
├── static/
│   ├── css/
│   │   └── style.css      # Stylesheet
│   └── js/
│       └── app.js         # Frontend JavaScript
└── README.md              # This file
```

## API Endpoints

### Get Current Price
```
GET /api/current-price
```
Returns the current gold price with timestamp and source.

### Get Price History
```
GET /api/price-history?limit=100
```
Returns historical price data. Optional `limit` parameter (default: 100).

### Get Prediction
```
GET /api/predict
```
Returns AI prediction for price direction with confidence level.

### Train Model
```
POST /api/train-model
```
Retrains the model with current historical data.

## How It Works

### 1. Web Scraping
The scraper module fetches live gold prices from multiple sources:
- goldprice.org
- investing.com
- Falls back to mock data if sources are unavailable

### 2. Deep Learning Model
- Uses LSTM (Long Short-Term Memory) neural network
- Trained on historical price sequences
- Predicts next price value
- Determines direction (UP/DOWN) with confidence level

### 3. Web Application
- Flask serves the web interface and API
- Background thread updates prices every 60 seconds
- Frontend polls API for real-time updates
- Plotly renders interactive charts

## Model Architecture

The LSTM model consists of:
- 3 LSTM layers (50 units each) with dropout (0.2)
- 2 Dense layers (25 and 1 units)
- Adam optimizer with MSE loss
- Sequence length: 60 time steps

## Customization

### Change Price Update Interval
In `app.py`, modify the sleep time in `update_prices_periodically()`:
```python
time.sleep(60)  # Change to desired seconds
```

### Add New Price Sources
Add new scraping methods in `scraper.py`:
```python
def scrape_new_source(self):
    # Your scraping logic here
    pass
```

### Adjust Model Parameters
In `model.py`, modify the model architecture or training parameters:
```python
predictor = GoldPricePredictor(sequence_length=60)  # Change sequence length
predictor.train(prices, epochs=50)  # Change epochs
```

## Development

### Testing the Scraper
```bash
python scraper.py
```

### Testing the Model
```bash
python model.py
```

### Running in Development Mode
The Flask app runs in debug mode by default for development.

## Production Deployment

For production deployment:

1. **Disable debug mode** in `app.py`:
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

2. **Use a production server** like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Set up a database** for persistent price history storage

4. **Configure HTTPS** for secure connections

5. **Add monitoring** and logging for production reliability

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Gold price data from various public sources
- TensorFlow/Keras for deep learning framework
- Flask for web framework
- Plotly for chart visualizations

## Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ for gold price analysis**
