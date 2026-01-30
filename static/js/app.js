// Gold Price Monitor Application - Multi-Source Support
let priceHistoryBySources = {
    goldprice: [],
    emasku: []
};
let chartInitialized = {
    goldprice: false,
    emasku: false
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Pantau Emas initialized - Multi-source mode');
    
    // Load initial data
    loadAllPrices();
    loadAllHistory();
    
    // Set up event listeners
    document.getElementById('predict-btn').addEventListener('click', getPrediction);
    document.getElementById('update-chart-btn').addEventListener('click', loadAllHistory);
    
    // Auto-refresh every 60 seconds
    setInterval(function() {
        loadAllPrices();
        loadAllHistory();
    }, 60000);
});

// Load current prices from all sources
async function loadAllPrices() {
    try {
        const response = await fetch('/api/current-prices-all');
        const data = await response.json();
        
        // Update goldprice.org display
        if (data.goldprice) {
            document.getElementById('current-price-goldprice').textContent = data.goldprice.price.toFixed(2);
            const timestamp1 = new Date(data.goldprice.timestamp);
            document.getElementById('price-timestamp-goldprice').textContent = 
                `Last updated: ${timestamp1.toLocaleTimeString()}`;
            console.log('GoldPrice updated:', data.goldprice.price);
        }
        
        // Update emasku.co.id display
        if (data.emasku) {
            document.getElementById('current-price-emasku').textContent = formatNumber(Math.round(data.emasku.price));
            const timestamp2 = new Date(data.emasku.timestamp);
            document.getElementById('price-timestamp-emasku').textContent = 
                `Last updated: ${timestamp2.toLocaleTimeString()}`;
            console.log('Emasku updated:', data.emasku.price);
        }
        
    } catch (error) {
        console.error('Error loading prices:', error);
        document.getElementById('current-price-goldprice').textContent = 'Error';
        document.getElementById('current-price-emasku').textContent = 'Error';
    }
}

// Load price history for all sources
async function loadAllHistory() {
    try {
        const response = await fetch('/api/price-history-all?limit=10000');
        const data = await response.json();
        
        // Update goldprice history
        if (data.goldprice) {
            priceHistoryBySources.goldprice = data.goldprice;
            console.log(`Loaded ${priceHistoryBySources.goldprice.length} goldprice points`);
            updateChart('goldprice');
            updateStatistics('goldprice');
        }
        
        // Update emasku history
        if (data.emasku) {
            priceHistoryBySources.emasku = data.emasku;
            console.log(`Loaded ${priceHistoryBySources.emasku.length} emasku points`);
            updateChart('emasku');
            updateStatistics('emasku');
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Update the price chart for a specific source
function updateChart(source) {
    const history = priceHistoryBySources[source];
    if (history.length === 0) {
        return;
    }
    
    // Prepare data for Plotly
    const timestamps = history.map(p => new Date(p.timestamp));
    const prices = history.map(p => p.price);
    
    const trace = {
        x: timestamps,
        y: prices,
        type: 'scatter',
        mode: 'lines+markers',
        name: source === 'goldprice' ? 'GoldPrice.org' : 'Emasku.co.id',
        line: {
            color: source === 'goldprice' ? '#d4af37' : '#10b981',
            width: 3
        },
        marker: {
            size: 4,
            color: source === 'goldprice' ? '#d4af37' : '#10b981'
        }
    };
    
    const currencyUnit = source === 'goldprice' ? 'USD/oz' : 'IDR/gram';
    
    const layout = {
        title: source === 'goldprice' ? 'GoldPrice.org - Price Over Time' : 'Emasku.co.id - Price Over Time',
        xaxis: {
            title: 'Time',
            showgrid: true,
            gridcolor: '#e0e0e0'
        },
        yaxis: {
            title: `Price (${currencyUnit})`,
            showgrid: true,
            gridcolor: '#e0e0e0'
        },
        plot_bgcolor: '#f9fafb',
        paper_bgcolor: '#f9fafb',
        font: {
            family: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif'
        },
        margin: {
            l: 80,
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
    
    const chartId = `price-chart-${source}`;
    Plotly.newPlot(chartId, [trace], layout, config);
    chartInitialized[source] = true;
}

// Update statistics for a specific source
function updateStatistics(source) {
    const history = priceHistoryBySources[source];
    if (history.length === 0) {
        return;
    }
    
    const prices = history.map(p => p.price);
    
    // Calculate stats
    const high24h = Math.max(...prices);
    const low24h = Math.min(...prices);
    const average = prices.reduce((a, b) => a + b, 0) / prices.length;
    
    // Format based on source
    const formatter = source === 'goldprice' 
        ? (val) => `$${val.toFixed(2)}`
        : (val) => `Rp${formatNumber(Math.round(val))}`;
    
    // Update display
    document.getElementById(`data-points-${source}`).textContent = history.length;
    document.getElementById(`high-24h-${source}`).textContent = formatter(high24h);
    document.getElementById(`low-24h-${source}`).textContent = formatter(low24h);
    document.getElementById(`average-price-${source}`).textContent = formatter(average);
}

// Get AI prediction (uses goldprice data)
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
