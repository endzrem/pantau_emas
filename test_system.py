"""
Simple tests for Pantau Emas gold price prediction system
"""
import unittest
import numpy as np
from scraper import GoldPriceScraper
from model import GoldPricePredictor, generate_sample_data


class TestGoldPriceScraper(unittest.TestCase):
    """Test web scraping functionality"""
    
    def setUp(self):
        self.scraper = GoldPriceScraper()
    
    def test_get_current_price(self):
        """Test that we can get a price (real or mock)"""
        price_data = self.scraper.get_current_price()
        self.assertIsNotNone(price_data)
        self.assertIn('price', price_data)
        self.assertIn('source', price_data)
        self.assertIn('timestamp', price_data)
        self.assertGreater(price_data['price'], 0)
    
    def test_get_mock_price(self):
        """Test mock price generation"""
        price_data = self.scraper.get_mock_price()
        self.assertIsNotNone(price_data)
        self.assertEqual(price_data['source'], 'mock')
        self.assertGreater(price_data['price'], 1900)
        self.assertLess(price_data['price'], 2100)


class TestGoldPricePredictor(unittest.TestCase):
    """Test ML model functionality"""
    
    def setUp(self):
        self.predictor = GoldPricePredictor(sequence_length=60)
        self.sample_data = generate_sample_data(500)
    
    def test_generate_sample_data(self):
        """Test sample data generation"""
        self.assertEqual(len(self.sample_data), 500)
        self.assertTrue(np.all(self.sample_data > 1500))
        self.assertTrue(np.all(self.sample_data < 2500))
    
    def test_prepare_data(self):
        """Test data preparation"""
        X, y = self.predictor.prepare_data(self.sample_data)
        self.assertEqual(len(X), len(self.sample_data) - 60)
        self.assertEqual(X.shape[1], 60)
    
    def test_model_training(self):
        """Test model training"""
        history = self.predictor.train(self.sample_data, epochs=2)
        self.assertTrue(self.predictor.is_trained)
        self.assertIsNotNone(self.predictor.model)
    
    def test_prediction(self):
        """Test price prediction"""
        # Train model first
        self.predictor.train(self.sample_data, epochs=2)
        
        # Test prediction
        prediction = self.predictor.predict_direction(self.sample_data[-100:])
        
        self.assertIsNotNone(prediction)
        self.assertIn('direction', prediction)
        self.assertIn('predicted_price', prediction)
        self.assertIn('confidence', prediction)
        self.assertIn(prediction['direction'], ['UP', 'DOWN'])
    
    def test_model_save_load(self):
        """Test model persistence"""
        import tempfile
        import os
        
        # Create temp file
        with tempfile.NamedTemporaryFile(suffix='.h5', delete=False) as f:
            temp_path = f.name
        
        try:
            # Train and save
            self.predictor.train(self.sample_data, epochs=2)
            self.predictor.save_model(temp_path)
            
            # Create new predictor and load
            new_predictor = GoldPricePredictor(sequence_length=60)
            result = new_predictor.load_model(temp_path)
            
            self.assertTrue(result)
            self.assertTrue(new_predictor.is_trained)
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
            scaler_path = temp_path.replace('.h5', '_scaler.pkl')
            if os.path.exists(scaler_path):
                os.remove(scaler_path)


if __name__ == '__main__':
    unittest.main()
