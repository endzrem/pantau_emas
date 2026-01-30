"""
Gold Price Web Scraper
Fetches live gold prices from various sources

DATA SOURCE EXPLANATION:
========================
This module is responsible for fetching live gold prices from the internet.

How it works:
1. The scraper tries multiple sources in order of priority
2. If the first source fails, it tries the next one
3. If all real sources fail, it generates mock data for testing

Current Sources (in order):
1. goldprice.org - International gold price in USD/oz
2. investing.com - Financial data website with gold prices
3. Mock data - Randomly generated prices for testing/fallback

To add a new source (e.g., emasku.co.id):
1. Create a new method like scrape_emasku()
2. Add it to get_current_price() method
3. See DATA_SOURCES.md for detailed guide

Where data is used:
- app.py calls scraper.get_current_price() every 60 seconds
- Prices are stored in price_history list
- ML model uses this data to make predictions
"""
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time


class GoldPriceScraper:
    """Scraper for fetching live gold prices"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.min_valid_price = 1000.0  # Minimum valid gold price per oz
        self.max_valid_price = 5000.0  # Maximum valid gold price per oz
    
    def _validate_price(self, price):
        """Validate that price is within reasonable bounds"""
        if price is None:
            return False
        try:
            price_float = float(price)
            return self.min_valid_price <= price_float <= self.max_valid_price
        except (ValueError, TypeError):
            return False
    
    def scrape_goldprice_org(self):
        """Scrape gold price from goldprice.org"""
        try:
            url = "https://goldprice.org/"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find gold price - this selector may need adjustment
            price_element = soup.find('div', {'class': 'price'})
            if price_element:
                price_text = price_element.text.strip()
                # Extract numeric value
                price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
                
                # Validate price
                if not self._validate_price(price):
                    print(f"Invalid price detected from goldprice.org: {price}")
                    return None
                
                return {
                    'price': price,
                    'source': 'goldprice.org',
                    'timestamp': datetime.now().isoformat(),
                    'currency': 'USD',
                    'unit': 'oz'
                }
        except Exception as e:
            print(f"Error scraping goldprice.org: {e}")
            return None
    
    def scrape_investing_com(self):
        """Scrape gold price from investing.com"""
        try:
            url = "https://www.investing.com/commodities/gold"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find gold price
            price_element = soup.find('span', {'data-test': 'instrument-price-last'})
            if price_element:
                price_text = price_element.text.strip()
                price = float(price_text.replace(',', ''))
                
                # Validate price
                if not self._validate_price(price):
                    print(f"Invalid price detected from investing.com: {price}")
                    return None
                
                return {
                    'price': price,
                    'source': 'investing.com',
                    'timestamp': datetime.now().isoformat(),
                    'currency': 'USD',
                    'unit': 'oz'
                }
        except Exception as e:
            print(f"Error scraping investing.com: {e}")
            return None
    
    def scrape_emasku(self):
        """
        Scrape gold price from emasku.co.id
        
        Example implementation for Indonesian gold price website.
        Note: This is a template - you need to inspect the actual website
        and adjust the selectors based on the HTML structure.
        """
        try:
            url = "https://www.emasku.co.id/en/gold-price"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # TODO: Inspect the website to find the correct selector
            # Example selectors (adjust based on actual HTML):
            # price_element = soup.find('div', {'class': 'price-value'})
            # price_element = soup.find('span', {'id': 'gold-price'})
            # price_element = soup.select_one('.price-container .price')
            
            # For now, return None since we don't have the exact selector
            # Uncomment and adjust when you know the correct selector:
            """
            price_element = soup.find('div', {'class': 'YOUR_CLASS_HERE'})
            if price_element:
                price_text = price_element.text.strip()
                # Clean the price text (remove Rp, commas, etc.)
                price_text = price_text.replace('Rp', '').replace(',', '').replace('.', '').strip()
                price = float(price_text)
                
                # Note: emasku prices are typically in IDR per gram
                # You may want to convert to USD per oz for consistency
                # Example conversion (adjust based on current rates):
                # price_usd_oz = price / 15000 * 31.1035
                
                if not self._validate_price(price):
                    print(f"Invalid price detected from emasku.co.id: {price}")
                    return None
                
                return {
                    'price': price,
                    'source': 'emasku.co.id',
                    'timestamp': datetime.now().isoformat(),
                    'currency': 'IDR',
                    'unit': 'gram'
                }
            """
            return None
        except Exception as e:
            print(f"Error scraping emasku.co.id: {e}")
            return None
    
    def get_mock_price(self):
        """Generate mock price for testing when scraping fails"""
        import random
        base_price = 2000.0
        variation = random.uniform(-50, 50)
        return {
            'price': round(base_price + variation, 2),
            'source': 'mock',
            'timestamp': datetime.now().isoformat(),
            'currency': 'USD',
            'unit': 'oz'
        }
    
    def get_current_price(self):
        """
        Get current gold price from available sources
        
        This method tries multiple sources in order:
        1. goldprice.org (primary)
        2. investing.com (backup)
        3. Mock data (fallback for testing)
        
        To add a new source (e.g., emasku.co.id):
        - Add: price_data = self.scrape_emasku()
        - Place it where you want in the priority order
        
        Example with emasku.co.id as primary source:
        ```
        price_data = self.scrape_emasku()
        if not price_data:
            price_data = self.scrape_goldprice_org()
        if not price_data:
            price_data = self.scrape_investing_com()
        if not price_data:
            price_data = self.get_mock_price()
        ```
        
        Returns:
            dict: Price data with keys: price, source, timestamp, currency, unit
        """
        # Try multiple sources in order of preference
        price_data = self.scrape_goldprice_org()
        if not price_data:
            price_data = self.scrape_investing_com()
        if not price_data:
            # Fallback to mock data for testing/development
            price_data = self.get_mock_price()
        
        return price_data


if __name__ == "__main__":
    scraper = GoldPriceScraper()
    price = scraper.get_current_price()
    print(json.dumps(price, indent=2))
