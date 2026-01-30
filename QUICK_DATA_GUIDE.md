# 📊 Quick Answer: Where Data Comes From & How to Add emasku.co.id

## ✅ Where Does the Data Come From?

The gold price data comes from **web scraping** - automatically fetching prices from websites.

### Current Sources (in order):

```
1. goldprice.org     → Try first
   ↓ (if fails)
2. investing.com     → Try second  
   ↓ (if fails)
3. Mock data         → Fallback for testing
```

### Where in the Code?

File: **`scraper.py`**
- Line 32-60: `scrape_goldprice_org()` - Gets price from goldprice.org
- Line 62-89: `scrape_investing_com()` - Gets price from investing.com  
- Line 104-132: `get_current_price()` - Tries all sources in order

---

## 🔧 How to Add emasku.co.id?

### Quick Steps:

1. **Open `scraper.py`**

2. **Add this method** (around line 91, before `get_mock_price()`):

```python
def scrape_emasku(self):
    """Scrape gold price from emasku.co.id"""
    try:
        url = "https://www.emasku.co.id/en/gold-price"
        response = requests.get(url, headers=self.headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # TODO: Inspect the website to find the correct HTML selector
        # Example: price_element = soup.find('div', {'class': 'price-value'})
        price_element = soup.find('div', {'class': 'YOUR_CLASS_HERE'})
        
        if price_element:
            price_text = price_element.text.strip()
            # Clean the price (remove Rp, commas, etc.)
            price_text = price_text.replace('Rp', '').replace(',', '').strip()
            price = float(price_text)
            
            if not self._validate_price(price):
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
```

3. **Update `get_current_price()` method** (around line 104):

```python
def get_current_price(self):
    # Try emasku first!
    price_data = self.scrape_emasku()
    if not price_data:
        price_data = self.scrape_goldprice_org()
    if not price_data:
        price_data = self.scrape_investing_com()
    if not price_data:
        price_data = self.get_mock_price()
    
    return price_data
```

4. **Find the correct HTML selector**:
   - Open https://www.emasku.co.id/en/gold-price in browser
   - Right-click on the price → "Inspect"
   - Look for the HTML element containing the price
   - Replace `'YOUR_CLASS_HERE'` with the actual class name

5. **Test it**:
```bash
python scraper.py
```

---

## 📚 More Details?

- **Complete Guide**: Read [DATA_SOURCES.md](DATA_SOURCES.md)
- **FAQ**: Check [README.md](README.md#frequently-asked-questions)
- **Example Code**: Look at `scraper.py` line 91-145

---

## 💡 Quick Tips

### Where to Make Changes:
- ✅ **scraper.py** - Add new scraping methods here
- ❌ **app.py** - Don't need to change this
- ❌ **model.py** - Don't need to change this

### Testing:
```bash
# Test just the scraper
python scraper.py

# Test full application
python app.py
# Then open http://localhost:5000
```

### Common Issues:

**Problem**: Can't find the price element
- **Solution**: Inspect the website HTML and find the correct selector

**Problem**: Price validation fails
- **Solution**: Adjust `min_valid_price` and `max_valid_price` in `__init__`

**Problem**: Currency is different (IDR vs USD)
- **Solution**: You can convert or just specify the correct currency in the return data

---

## 🎯 Summary

**Where data comes from**: Web scraping from goldprice.org and investing.com

**Where to change it**: `scraper.py` file
1. Add new method like `scrape_emasku()`
2. Update `get_current_price()` to include it
3. Test with `python scraper.py`

**Need help?**: Read [DATA_SOURCES.md](DATA_SOURCES.md) for the complete guide!
