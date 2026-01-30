#!/usr/bin/env python3
"""
Quick Demo Script for Pantau Emas
This script helps you quickly populate data and test predictions
"""

import requests
import time
import sys

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_server():
    """Check if the server is running"""
    try:
        response = requests.get("http://localhost:5000/api/current-price", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print_header("🎯 Pantau Emas - Quick Demo Script")
    
    # Check if server is running
    print("⏳ Checking if application is running...")
    if not check_server():
        print("❌ ERROR: The application is not running!")
        print("\nPlease start the application first:")
        print("   1. Open a terminal")
        print("   2. Run: python app.py")
        print("   3. Wait for 'Running on http://127.0.0.1:5000'")
        print("   4. Then run this demo script again\n")
        sys.exit(1)
    
    print("✅ Application is running!\n")
    
    # Step 1: Get current price
    print_header("Step 1: Getting Current Gold Price")
    try:
        response = requests.get("http://localhost:5000/api/current-price", timeout=5)
        data = response.json()
        print(f"💰 Current Price: ${data['price']:.2f} per {data['unit']}")
        print(f"📍 Source: {data['source']}")
        print(f"🕐 Time: {data['timestamp']}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Step 2: Check price history
    print_header("Step 2: Checking Price History")
    try:
        response = requests.get("http://localhost:5000/api/price-history", timeout=5)
        history = response.json()
        print(f"📊 Current data points: {len(history)}")
        
        if len(history) >= 60:
            print("✅ Enough data for predictions!")
        else:
            print(f"⚠️  Need {60 - len(history)} more data points for predictions")
            print("\nWould you like to quickly add test data? (y/n): ", end="")
            
            choice = input().strip().lower()
            if choice == 'y':
                print_header("Step 3: Adding Test Data")
                print("⏳ Adding 70 data points (this may take a minute)...")
                
                for i in range(70):
                    try:
                        requests.get("http://localhost:5000/api/current-price", timeout=5)
                        if (i + 1) % 10 == 0:
                            print(f"  Added {i + 1}/70 data points...")
                        time.sleep(0.5)
                    except:
                        print(f"  Warning: Failed at point {i + 1}")
                
                print("\n✅ Test data added successfully!")
                
                # Refresh history to get accurate count
                time.sleep(1)  # Wait a moment for server to process
                response = requests.get("http://localhost:5000/api/price-history", timeout=5)
                history = response.json()
                print(f"📊 Total data points now: {len(history)}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Step 4: Get prediction
    if len(history) >= 60:
        print_header("Step 4: Getting AI Prediction")
        try:
            response = requests.get("http://localhost:5000/api/predict", timeout=10)
            if response.status_code == 200:
                prediction = response.json()
                
                # Display prediction
                direction_icon = "📈" if prediction['direction'] == "UP" else "📉"
                print(f"{direction_icon} Prediction: Price will go {prediction['direction']}")
                print(f"💵 Current Price: ${prediction['current_price']:.2f}")
                print(f"🔮 Predicted Price: ${prediction['predicted_price']:.2f}")
                print(f"📊 Expected Change: ${prediction['change']:+.2f}")
                print(f"🎯 Confidence: {prediction['confidence']:.2f}%")
            else:
                error = response.json()
                print(f"❌ Error: {error.get('message', 'Unknown error')}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Final instructions
    print_header("🎉 Demo Complete!")
    print("Next steps:")
    print("  1. Open your browser to: http://localhost:5000")
    print("  2. Click 'Get Prediction' button to see the AI prediction")
    print("  3. Explore the interactive charts and statistics")
    print("  4. Read TUTORIAL.md for detailed instructions")
    print("\nTo stop the application:")
    print("  - Go to the terminal running app.py")
    print("  - Press Ctrl+C")
    print("\nHappy price predicting! 🚀\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
