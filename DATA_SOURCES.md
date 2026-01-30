# 📊 Data Sources Guide

## Where Does the Gold Price Data Come From?

The Pantau Emas system fetches live gold prices from **multiple sources** on the internet through a process called **web scraping**.

### Current Data Sources

The system currently uses these sources (in order of priority):

1. **goldprice.org** - Primary source
2. **investing.com** - Backup source
3. **Mock data** - Fallback for testing/development

### How It Works

```
┌─────────────────────────────────────────┐
│  1. Try goldprice.org                   │
│     ↓                                    │
│  2. If fails, try investing.com         │
│     ↓                                    │
│  3. If both fail, use mock data         │
└─────────────────────────────────────────┘
```

The system attempts to fetch prices every **60 seconds** and stores them in memory for analysis.

---

## 🔧 How to Add a New Data Source

Want to use a different website like **emasku.co.id**? Follow these steps:

### Step 1: Understand the Website Structure

Before you can scrape a website, you need to inspect its HTML structure:

1. Open the website in your browser (e.g., https://www.emasku.co.id/en/gold-price)
2. Right-click on the price → Select "Inspect" or "Inspect Element"
3. Find the HTML element that contains the price
4. Note the element type, class name, or ID

Example:
```html
<div class="price-value">2,050.00</div>
<!-- or -->
<span id="gold-price">Rp 950,000</span>
```

### Step 2: Create a New Scraper Method

Open `scraper.py` and add a new method in the `GoldPriceScraper` class:

```python
def scrape_emasku(self):
    """Scrape gold price from emasku.co.id"""
    try:
        url = "https://www.emasku.co.id/en/gold-price"
        response = requests.get(url, headers=self.headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the price element (adjust selector based on website)
        price_element = soup.find('div', {'class': 'price-value'})
        # OR: price_element = soup.find('span', {'id': 'gold-price'})
        
        if price_element:
            price_text = price_element.text.strip()
            # Clean and convert to float
            # Remove currency symbols, commas, etc.
            price_text = price_text.replace('Rp', '').replace(',', '').strip()
            price = float(price_text)
            
            # Validate price
            if not self._validate_price(price):
                print(f"Invalid price detected from emasku.co.id: {price}")
                return None
            
            return {
                'price': price,
                'source': 'emasku.co.id',
                'timestamp': datetime.now().isoformat(),
                'currency': 'IDR',  # or 'USD' depending on the price
                'unit': 'gram'      # or 'oz' depending on unit
            }
    except Exception as e:
        print(f"Error scraping emasku.co.id: {e}")
        return None
```

### Step 3: Add to Source Priority List

In the same file, update the `get_current_price()` method:

```python
def get_current_price(self):
    """Get current gold price from available sources"""
    # Try multiple sources
    price_data = self.scrape_emasku()  # Try emasku first
    if not price_data:
        price_data = self.scrape_goldprice_org()
    if not price_data:
        price_data = self.scrape_investing_com()
    if not price_data:
        # Fallback to mock data
        price_data = self.get_mock_price()
    
    return price_data
```

### Step 4: Test Your Scraper

Run the scraper directly to test:

```bash
python scraper.py
```

You should see output like:
```json
{
  "price": 950000.0,
  "source": "emasku.co.id",
  "timestamp": "2026-01-30T10:45:00.123456",
  "currency": "IDR",
  "unit": "gram"
}
```

---

## 💡 Important Notes

### Currency Conversion

If your new source uses a different currency (e.g., IDR, EUR), you may need to:
1. Convert to USD for consistency
2. Or update the UI to display the correct currency

### Unit Conversion

Gold prices can be in different units:
- **Troy Ounce (oz)** - International standard
- **Gram** - Common in Indonesia
- **Kilogram** - Some markets

Make sure your scraper specifies the correct unit.

### Price Validation

The system validates that prices are between $1,000 and $5,000 per oz. If your source uses different units or currency, you may need to adjust these limits in the `__init__` method:

```python
def __init__(self):
    self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    # Adjust these based on your currency/unit
    self.min_valid_price = 1000.0
    self.max_valid_price = 5000.0
```

---

## 🔍 Debugging Tips

### Problem: Can't find the price element

**Solution:** Use Chrome DevTools or Firefox Inspector to find the exact selector:
1. Right-click on price → Inspect
2. Look for unique identifiers (class, id, data-attributes)
3. Test selector in browser console: `document.querySelector('.price-value')`

### Problem: Price extraction returns wrong value

**Solution:** Check the text content:
```python
print(f"Raw text: {price_element.text}")
print(f"Stripped: {price_element.text.strip()}")
```

### Problem: Website blocks scraping

**Solution:** 
- Add delay between requests: `time.sleep(2)`
- Use different User-Agent headers
- Respect robots.txt
- Consider using the website's API if available

### Problem: Price validation fails

**Solution:** Adjust validation bounds or convert to standard unit:
```python
# For gram prices in IDR
if self.currency == 'IDR' and self.unit == 'gram':
    # Convert gram to oz and IDR to USD for validation
    price_oz_usd = price * 31.1035 / 15000  # approximate conversion
    if not self._validate_price(price_oz_usd):
        return None
```

---

## 📁 File Locations

- **scraper.py** - Main scraping logic (add new methods here)
- **app.py** - Uses the scraper (line 15: `scraper = GoldPriceScraper()`)
- **test_system.py** - Tests for scraper

---

## 🎓 Complete Example: Adding Emasku.co.id

Here's a complete example you can copy-paste:

```python
# In scraper.py, add this method to GoldPriceScraper class:

def scrape_emasku(self):
    """Scrape gold price from emasku.co.id"""
    try:
        url = "https://www.emasku.co.id/en/gold-price"
        response = requests.get(url, headers=self.headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Note: You need to inspect the actual website to find correct selector
        # This is a template - adjust based on actual HTML structure
        price_element = soup.find('div', {'class': 'price'})
        
        if price_element:
            price_text = price_element.text.strip()
            # Remove common symbols
            price_text = price_text.replace('Rp', '').replace(',', '').replace('.', '')
            price = float(price_text)
            
            # If price is in IDR per gram, convert to USD per oz for consistency
            # (This is optional - adjust based on your needs)
            # price_usd_oz = price / 15000 * 31.1035  # Rough conversion
            
            if not self._validate_price(price):
                print(f"Invalid price from emasku.co.id: {price}")
                return None
            
            return {
                'price': price,
                'source': 'emasku.co.id',
                'timestamp': datetime.now().isoformat(),
                'currency': 'IDR',
                'unit': 'gram'
            }
    except Exception as e:
        print(f"Error scraping emasku.co.id: {e}")
        return None

# Then update get_current_price() to include the new source:
def get_current_price(self):
    """Get current gold price from available sources"""
    price_data = self.scrape_emasku()  # Try emasku first
    if not price_data:
        price_data = self.scrape_goldprice_org()
    if not price_data:
        price_data = self.scrape_investing_com()
    if not price_data:
        price_data = self.get_mock_price()
    
    return price_data
```

---

## ⚖️ Legal & Ethical Considerations

When scraping websites:
- ✅ **Check robots.txt** - Respect the website's scraping policy
- ✅ **Add delays** - Don't overwhelm the server
- ✅ **Use responsibly** - For personal/educational use
- ✅ **Consider alternatives** - Check if the site has an API
- ❌ **Don't abuse** - Excessive requests can harm the website

---

## 🆘 Need Help?

1. Read the website's HTML using browser DevTools
2. Try the selector in browser console first
3. Test your scraper method independently
4. Check the error messages in terminal
5. Look at existing scrapers in `scraper.py` as examples

---

## 📚 Related Documentation

- **scraper.py** - Implementation details
- **TUTORIAL.md** - General usage guide
- **README.md** - Project overview
