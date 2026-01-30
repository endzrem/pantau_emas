# 🎬 Getting Started in 5 Minutes

This is the **fastest way** to get started with Pantau Emas gold price prediction system.

---

## ⚡ Quick Start (Copy & Paste)

### 1️⃣ Check Python (30 seconds)

Open terminal and paste:

```bash
python --version
```

✅ If you see `Python 3.8` or higher: Great! Continue below.  
❌ If error: [Install Python](https://www.python.org/downloads/) first, then come back.

---

### 2️⃣ Download & Setup (2 minutes)

**Option A: Download ZIP**
1. Go to https://github.com/endzrem/pantau_emas
2. Click green "Code" button → "Download ZIP"
3. Extract to a folder

**Option B: Use Git**
```bash
git clone https://github.com/endzrem/pantau_emas.git
```

---

### 3️⃣ Install & Run (2 minutes)

Open terminal in the `pantau_emas` folder and paste these commands:

```bash
# Install packages (one time only)
pip install -r requirements.txt

# Start the app
python app.py
```

You should see: `* Running on http://127.0.0.1:5000`

✅ **Success!** Keep this terminal window open.

---

### 4️⃣ Open in Browser (30 seconds)

Open your web browser and go to:

```
http://localhost:5000
```

You'll see the Pantau Emas dashboard! 🎉

---

### 5️⃣ Test the Prediction (1 minute)

Open a **new** terminal in the same folder and run:

```bash
python demo.py
```

Follow the prompts (type `y` when asked).

Then refresh your browser and click **"Get Prediction"** to see the AI prediction!

---

## 🎯 What You'll See

### The Dashboard Has:

1. **Current Price Card** (Top Left)
   - Shows live gold price per ounce
   - Auto-updates every 60 seconds

2. **AI Prediction Card** (Top Right)
   - Click "Get Prediction" button
   - Shows UP 📈 or DOWN 📉
   - Shows predicted price & confidence

3. **Price Chart** (Middle)
   - Interactive graph of price history
   - Hover to see details

4. **Statistics** (Bottom)
   - Data points collected
   - 24-hour high/low
   - Average price

---

## ❓ Need More Help?

- **Detailed Guide:** Read [TUTORIAL.md](TUTORIAL.md) for complete step-by-step
- **Quick Reference:** Check [QUICKSTART.md](QUICKSTART.md)
- **Troubleshooting:** See TUTORIAL.md Troubleshooting section

---

## 🛑 Common Issues

**"Port 5000 already in use"**
- Close other applications or change port in `app.py` (line 140: `port=5000` → `port=5001`)

**"Module not found"**
- Make sure you ran `pip install -r requirements.txt`
- Try `pip3` instead of `pip`

**"Not enough data for prediction"**
- Run `python demo.py` to add test data
- Or wait 60 minutes for automatic collection

---

## 🎓 Understanding the System

**How It Works:**
1. 🌐 **Web Scraping** - Gets gold prices from websites
2. 💾 **Data Storage** - Saves prices in memory
3. 🤖 **Machine Learning** - LSTM neural network learns patterns
4. 🔮 **Prediction** - Predicts if price goes up or down
5. 📊 **Visualization** - Beautiful web dashboard

---

## 🚀 What's Next?

After you have it running:

1. **Let it collect data** - The more data, the better predictions
2. **Explore the interface** - Try all buttons and features
3. **Read the code** - Learn how it works
4. **Customize it** - Change colors, intervals, model parameters
5. **Deploy it** - Put it online (see PRODUCTION.md)

---

## 💡 Pro Tips

- Leave the app running to collect more data
- The model improves with more historical data
- Check predictions regularly to see accuracy
- Read TUTORIAL.md for deep dive into features

---

**Happy predicting!** 🎉

Need help? Open an issue on GitHub or read TUTORIAL.md for detailed instructions.
