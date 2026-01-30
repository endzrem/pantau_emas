# Quick Start Guide

## Installation & Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Access the web interface:**
   Open your browser and navigate to: `http://localhost:5000`

## Usage

### Web Interface

- **Current Price:** View the live gold price (updates automatically every 60 seconds)
- **Get Prediction:** Click the "Get Prediction" button to get AI prediction for price direction
- **Refresh Price:** Manually refresh the current gold price
- **Update Chart:** Update the historical price chart

### API Usage Examples

**Get Current Price:**
```bash
curl http://localhost:5000/api/current-price
```

**Get Price History:**
```bash
curl http://localhost:5000/api/price-history?limit=100
```

**Get AI Prediction:**
```bash
curl http://localhost:5000/api/predict
```

**Retrain Model:**
```bash
curl -X POST http://localhost:5000/api/train-model
```

## Model Training

The LSTM model is automatically trained on first run with sample data. You can retrain it with real data by:

1. Accumulating enough historical data (60+ data points)
2. Using the API endpoint: `POST /api/train-model`

## Customization

### Change Update Frequency
Edit `app.py` line 48:
```python
time.sleep(60)  # Change to desired seconds
```

### Adjust Model Parameters
Edit `model.py`:
```python
predictor = GoldPricePredictor(sequence_length=60)  # Change sequence length
predictor.train(prices, epochs=50)  # Change number of epochs
```

### Add New Price Sources
Add new scraping methods in `scraper.py`:
```python
def scrape_new_source(self):
    # Your implementation
    pass
```

## Troubleshooting

**Issue:** Not enough data for prediction
- **Solution:** Wait for the app to collect at least 60 data points (about 1 hour with default settings)

**Issue:** Web scraping fails
- **Solution:** The app automatically falls back to mock data for testing purposes

**Issue:** Chart not displaying
- **Solution:** Ensure Plotly CDN is accessible or host Plotly locally

## Notes

- The application uses mock data by default when real scraping sources are unavailable
- Model accuracy improves with more historical data
- The LSTM model is saved as `gold_model.h5` and can be reloaded
