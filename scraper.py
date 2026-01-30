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
        
        Indonesian gold price website with prices in IDR per gram.
        """
        try:
            url = "https://www.emasku.co.id/en/gold-price"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find gold price elements
            # Look for common patterns on gold price websites
            price_element = None
            
            # Try various selectors
            selectors_to_try = [
                ('div', {'class': 'price'}),
                ('span', {'class': 'price'}),
                ('td', {'class': 'text-right'}),
                ('div', {'class': 'gold-price'}),
            ]
            
            for tag, attrs in selectors_to_try:
                elements = soup.find_all(tag, attrs)
                for element in elements:
                    text = element.text.strip()
                    # Look for numbers that might be prices
                    if any(char.isdigit() for char in text):
                        price_element = element
                        break
                if price_element:
                    break
            
            if price_element:
                price_text = price_element.text.strip()
                # Clean the price text (remove Rp, commas, dots used as thousand separators)
                price_text = price_text.replace('Rp', '').replace(',', '').replace('.', '').strip()
                # Extract just numbers
                import re
                numbers = re.findall(r'\d+', price_text)
                if numbers:
                    price = float(numbers[0])
                    
                    # Note: emasku prices are in IDR per gram
                    # Validation range should be different for IDR
                    if 800000 <= price <= 2000000:  # Typical range for IDR per gram
                        return {
                            'price': price,
                            'source': 'emasku.co.id',
                            'timestamp': datetime.now().isoformat(),
                            'currency': 'IDR',
                            'unit': 'gram'
                        }
            
            # If scraping fails, generate mock IDR price
            import random
            base_price_idr = 1000000  # ~1 million IDR per gram
            variation = random.uniform(-50000, 50000)
            return {
                'price': round(base_price_idr + variation, 2),
                'source': 'emasku.co.id (mock)',
                'timestamp': datetime.now().isoformat(),
                'currency': 'IDR',
                'unit': 'gram'
            }
        except Exception as e:
            print(f"Error scraping emasku.co.id: {e}")
            # Return mock data as fallback
            import random
            base_price_idr = 1000000
            variation = random.uniform(-50000, 50000)
            return {
                'price': round(base_price_idr + variation, 2),
                'source': 'emasku.co.id (mock)',
                'timestamp': datetime.now().isoformat(),
                'currency': 'IDR',
                'unit': 'gram'
            }
    
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
    
    def get_all_sources(self):
        """
        Get current gold price from ALL available sources simultaneously.
        
        Returns:
            dict: Dictionary with source names as keys and price data as values
        """
        sources = {}
        
        # Try goldprice.org
        try:
            goldprice_data = self.scrape_goldprice_org()
            if not goldprice_data:
                goldprice_data = self.get_mock_price()
            sources['goldprice'] = goldprice_data
        except Exception as e:
            print(f"Error getting goldprice.org: {e}")
            sources['goldprice'] = self.get_mock_price()
        
        # Try emasku.co.id
        try:
            emasku_data = self.scrape_emasku()
            sources['emasku'] = emasku_data
        except Exception as e:
            print(f"Error getting emasku.co.id: {e}")
            # Fallback mock for emasku
            import random
            base_price_idr = 1000000
            variation = random.uniform(-50000, 50000)
            sources['emasku'] = {
                'price': round(base_price_idr + variation, 2),
                'source': 'emasku.co.id (mock)',
                'timestamp': datetime.now().isoformat(),
                'currency': 'IDR',
                'unit': 'gram'
            }
        
        return sources


if __name__ == "__main__":
    scraper = GoldPriceScraper()
    price = scraper.get_current_price()
    print(json.dumps(price, indent=2))
