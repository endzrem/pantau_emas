# 📚 Complete Step-by-Step Tutorial for Beginners

Welcome! This tutorial will guide you through using the Pantau Emas gold price prediction system, even if you're new to programming.

## 📋 Table of Contents
1. [What You Need](#what-you-need)
2. [Step 1: Install Python](#step-1-install-python)
3. [Step 2: Get the Code](#step-2-get-the-code)
4. [Step 3: Install Required Packages](#step-3-install-required-packages)
5. [Step 4: Start the Application](#step-4-start-the-application)
6. [Step 5: Use the Web Interface](#step-5-use-the-web-interface)
7. [Troubleshooting](#troubleshooting)
8. [What's Next?](#whats-next)

---

## What You Need

Before starting, make sure you have:
- A computer with Windows, Mac, or Linux
- Internet connection
- Basic knowledge of using the command line/terminal
- At least 2GB of free disk space

---

## Step 1: Install Python

### Check if Python is Already Installed

1. Open your terminal/command prompt:
   - **Windows**: Press `Win + R`, type `cmd`, press Enter
   - **Mac**: Press `Cmd + Space`, type `terminal`, press Enter
   - **Linux**: Press `Ctrl + Alt + T`

2. Type this command and press Enter:
   ```bash
   python --version
   ```
   
3. If you see something like `Python 3.8.0` or higher, you're good! Skip to Step 2.
   
   If you get an error, continue below.

### Install Python (if needed)

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.8 or newer
3. Run the installer
4. ⚠️ **IMPORTANT**: Check the box "Add Python to PATH" during installation
5. Click "Install Now"
6. Verify installation by running `python --version` again

---

## Step 2: Get the Code

### Option A: Download as ZIP (Easiest)

1. Go to: https://github.com/endzrem/pantau_emas
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to a folder (e.g., `C:\pantau_emas` or `~/pantau_emas`)
5. Open terminal and navigate to that folder:
   ```bash
   cd C:\pantau_emas
   ```
   (Or on Mac/Linux: `cd ~/pantau_emas`)

### Option B: Using Git (If you have it)

```bash
git clone https://github.com/endzrem/pantau_emas.git
cd pantau_emas
```

---

## Step 3: Install Required Packages

This installs all the libraries the application needs.

1. Make sure you're in the `pantau_emas` folder (see Step 2)

2. Run this command:
   ```bash
   pip install -r requirements.txt
   ```

3. Wait for installation (may take 5-10 minutes)

4. You should see messages like "Successfully installed tensorflow..." 

**Troubleshooting**: 
- If `pip` doesn't work, try `pip3` instead
- If you get permission errors on Mac/Linux, use `sudo pip install -r requirements.txt`

---

## Step 4: Start the Application

1. In your terminal, make sure you're still in the `pantau_emas` folder

2. Run this command:
   ```bash
   python app.py
   ```

3. You should see messages like:
   ```
   * Serving Flask app 'app'
   * Running on http://127.0.0.1:5000
   ```

4. ✅ **Success!** The application is now running!

5. ⚠️ **Keep this terminal window open** - don't close it while using the app

---

## Step 5: Use the Web Interface

### Access the Application

1. Open your web browser (Chrome, Firefox, Safari, etc.)

2. Go to this address:
   ```
   http://localhost:5000
   ```
   (You can also try `http://127.0.0.1:5000`)

3. You should see the Pantau Emas dashboard! 🎉

### Understanding the Dashboard

The dashboard has 4 main sections:

#### 1️⃣ **Current Gold Price** (Top Left)
   - Shows the current price per ounce
   - Updates automatically every 60 seconds
   - Click "Refresh Price" to update manually

#### 2️⃣ **AI Prediction** (Top Right)
   - Click "Get Prediction" to see if price will go UP 📈 or DOWN 📉
   - Shows predicted price and confidence level
   - Needs at least 60 data points (wait ~60 minutes after first start)

#### 3️⃣ **Price History Chart** (Middle)
   - Interactive chart showing price over time
   - Hover over points to see details
   - Click "Update Chart" to refresh

#### 4️⃣ **Statistics** (Bottom)
   - Data Points: How many prices collected
   - 24h High: Highest price in last 24 hours
   - 24h Low: Lowest price in last 24 hours
   - Average: Average of all collected prices

### Making Your First Prediction

**Important**: You need at least 60 price data points before predictions work.

#### Quick Method (For Testing):

1. Open a **new** terminal window (keep the app running in the first one!)

2. Navigate to the pantau_emas folder again

3. Run this command to quickly add test data:
   ```bash
   python -c "import requests; [requests.get('http://localhost:5000/api/current-price') for _ in range(70)]"
   ```

4. Go back to your browser and refresh the page

5. Click "Get Prediction" - you should now see a prediction!

#### Normal Method (Real Usage):

1. Just leave the application running
2. It automatically collects a new price every 60 seconds
3. After 60 minutes (60 data points), predictions will work
4. The more data collected, the better the predictions!

### Using the API (Advanced)

If you want to use the application programmatically:

#### Get Current Price
```bash
curl http://localhost:5000/api/current-price
```

#### Get Prediction
```bash
curl http://localhost:5000/api/predict
```

#### Get Price History
```bash
curl http://localhost:5000/api/price-history?limit=50
```

---

## Troubleshooting

### Problem: "pip: command not found"
**Solution**: Try `pip3` instead of `pip`, or reinstall Python with "Add to PATH" checked.

### Problem: "Port 5000 already in use"
**Solution**: 
1. Close any other applications using port 5000
2. Or edit `app.py` and change `port=5000` to `port=5001`

### Problem: "Module not found" errors
**Solution**: Make sure you ran `pip install -r requirements.txt` successfully

### Problem: "Not enough data for prediction"
**Solution**: 
- Wait longer (need 60+ data points)
- Or use the quick method above to add test data

### Problem: Price shows as "Loading..." forever
**Solution**: 
1. Check your internet connection
2. The app is using mock data (this is normal if real websites are blocked)
3. Check the terminal for error messages

### Problem: Application crashes
**Solution**:
1. Look at the error message in the terminal
2. Make sure all dependencies installed correctly
3. Try restarting: Press `Ctrl+C` in terminal, then run `python app.py` again

### Problem: Can't access http://localhost:5000
**Solution**:
1. Make sure the app is running (check terminal)
2. Try `http://127.0.0.1:5000` instead
3. Check if firewall is blocking the connection

---

## What's Next?

### Learn More
- Read `README.md` for detailed documentation
- Read `PRODUCTION.md` to deploy this online
- Explore `model.py` to understand the AI model

### Customize the Application
- Change update frequency: Edit `app.py`, line ~40, change `time.sleep(60)` to different seconds
- Modify the model: Edit `model.py` to adjust the neural network
- Change the design: Edit `static/css/style.css` for different colors

### Share Your Application
Want to share your gold price predictor online? Read `PRODUCTION.md` for:
- How to deploy on a server
- Security best practices
- Using a custom domain name

---

## 🎓 Understanding How It Works

### The Process:
1. **Web Scraping**: App visits gold price websites and extracts prices
2. **Data Storage**: Prices are saved in memory (or database in production)
3. **Machine Learning**: LSTM neural network learns patterns from historical data
4. **Prediction**: Model predicts if next price will be higher or lower
5. **Visualization**: Web interface displays everything beautifully

### Key Files:
- `app.py` - Web server that handles everything
- `model.py` - AI/machine learning code
- `scraper.py` - Gets prices from websites
- `templates/index.html` - The web page you see
- `static/` - Styling and JavaScript

---

## 📞 Need More Help?

1. Check existing issues on GitHub
2. Read the full documentation in `README.md`
3. Look at `QUICKSTART.md` for quick reference
4. Open a new issue on GitHub with your question

---

## ✨ Congratulations!

You now know how to:
- ✅ Install and run the gold price prediction system
- ✅ Use the web interface
- ✅ Get AI predictions
- ✅ Troubleshoot common problems

**Happy price predicting!** 🎉📊📈
