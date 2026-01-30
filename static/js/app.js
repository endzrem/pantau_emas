// Gold Price Monitor Application
let priceHistory = [];
let chartInitialized = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Pantau Emas initialized');
    
    // Load initial data
    loadCurrentPrice();
    loadPriceHistory();
    
    // Set up event listeners
    document.getElementById('refresh-btn').addEventListener('click', loadCurrentPrice);
    document.getElementById('predict-btn').addEventListener('click', getPrediction);
    document.getElementById('update-chart-btn').addEventListener('click', loadPriceHistory);
    
    // Auto-refresh every 60 seconds
    setInterval(function() {
        loadCurrentPrice();
        loadPriceHistory();
    }, 60000);
});

// Load current gold price
async function loadCurrentPrice() {
    try {
        const response = await fetch('/api/current-price');
        const data = await response.json();
        
        // Update display
        document.getElementById('current-price').textContent = data.price.toFixed(2);
        document.getElementById('price-source').textContent = `Source: ${data.source}`;
        
        const timestamp = new Date(data.timestamp);
        document.getElementById('price-timestamp').textContent = 
            `Last updated: ${timestamp.toLocaleTimeString()}`;
        
        console.log('Price updated:', data.price);
    } catch (error) {
        console.error('Error loading price:', error);
        document.getElementById('current-price').textContent = 'Error';
    }
}

// Load price history and update chart
async function loadPriceHistory() {
    try {
        const response = await fetch('/api/price-history?limit=100');
        priceHistory = await response.json();
        
        console.log(`Loaded ${priceHistory.length} price points`);
        
        // Update chart
        updateChart();
        
        // Update statistics
        updateStatistics();
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Update the price chart
function updateChart() {
    if (priceHistory.length === 0) {
        return;
    }
    
    // Prepare data for Plotly
    const timestamps = priceHistory.map(p => new Date(p.timestamp));
    const prices = priceHistory.map(p => p.price);
    
    const trace = {
        x: timestamps,
        y: prices,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Gold Price',
        line: {
            color: '#d4af37',
            width: 3
        },
        marker: {
            size: 6,
            color: '#d4af37'
        }
    };
    
    const layout = {
        title: 'Gold Price Over Time',
        xaxis: {
            title: 'Time',
            showgrid: true,
            gridcolor: '#e0e0e0'
        },
        yaxis: {
            title: 'Price (USD/oz)',
            showgrid: true,
            gridcolor: '#e0e0e0'
        },
        plot_bgcolor: '#f9fafb',
        paper_bgcolor: '#f9fafb',
        font: {
            family: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif'
        },
        margin: {
            l: 60,
            r: 40,
            t: 60,
            b: 60
        }
    };
    
    const config = {
        responsive: true,
        displayModeBar: true,
        displaylogo: false
    };
    
    Plotly.newPlot('price-chart', [trace], layout, config);
    chartInitialized = true;
}

// Update statistics
function updateStatistics() {
    if (priceHistory.length === 0) {
        return;
    }
    
    const prices = priceHistory.map(p => p.price);
    
    // Calculate stats
    const high24h = Math.max(...prices);
    const low24h = Math.min(...prices);
    const average = prices.reduce((a, b) => a + b, 0) / prices.length;
    
    // Update display
    document.getElementById('data-points').textContent = priceHistory.length;
    document.getElementById('high-24h').textContent = `$${high24h.toFixed(2)}`;
    document.getElementById('low-24h').textContent = `$${low24h.toFixed(2)}`;
    document.getElementById('average-price').textContent = `$${average.toFixed(2)}`;
}

// Get AI prediction
async function getPrediction() {
    try {
        document.getElementById('direction-text').textContent = 'Calculating...';
        document.getElementById('predict-btn').disabled = true;
        
        const response = await fetch('/api/predict');
        
        if (!response.ok) {
            const error = await response.json();
            alert(error.message || 'Not enough data for prediction');
            document.getElementById('predict-btn').disabled = false;
            return;
        }
        
        const prediction = await response.json();
        
        // Update prediction display
        const directionText = document.getElementById('direction-text');
        const directionIcon = document.getElementById('direction-icon');
        
        directionText.textContent = prediction.direction;
        directionText.className = `direction-text ${prediction.direction.toLowerCase()}`;
        
        if (prediction.direction === 'UP') {
            directionIcon.textContent = '📈';
        } else {
            directionIcon.textContent = '📉';
        }
        
        // Update details
        document.getElementById('predicted-price').textContent = 
            `$${prediction.predicted_price.toFixed(2)}`;
        
        const changeColor = prediction.change >= 0 ? '#10b981' : '#ef4444';
        const changeSign = prediction.change >= 0 ? '+' : '';
        const changeElement = document.getElementById('price-change');
        changeElement.textContent = `${changeSign}$${prediction.change.toFixed(2)}`;
        changeElement.style.color = changeColor;
        
        document.getElementById('confidence').textContent = 
            `${prediction.confidence.toFixed(2)}%`;
        
        console.log('Prediction:', prediction);
        
    } catch (error) {
        console.error('Error getting prediction:', error);
        alert('Error getting prediction. Please try again.');
    } finally {
        document.getElementById('predict-btn').disabled = false;
    }
}

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
