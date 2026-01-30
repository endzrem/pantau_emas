"""
Gold Price Web Scraper
Fetches live gold prices from various sources
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
        """Get current gold price from available sources"""
        # Try multiple sources
        price_data = self.scrape_goldprice_org()
        if not price_data:
            price_data = self.scrape_investing_com()
        if not price_data:
            # Fallback to mock data
            price_data = self.get_mock_price()
        
        return price_data


if __name__ == "__main__":
    scraper = GoldPriceScraper()
    price = scraper.get_current_price()
    print(json.dumps(price, indent=2))
