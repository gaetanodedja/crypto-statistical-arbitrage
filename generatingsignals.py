import ccxt
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint
from statsmodels.tools.tools import add_constant
from statsmodels.regression.linear_model import OLS
import time

# Set up Binance API connection
binance = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
    'enableRateLimit': True,
})

def fetch_all_pairs():
    """Fetch all USDT pairs from Binance."""
    markets = binance.load_markets()
    usdt_pairs = [symbol for symbol in markets if symbol.endswith('/USDT')]
    return usdt_pairs

def fetch_data(symbol, timeframe='1m', limit=28000):
    """Fetch historical data from Binance."""
    ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df.set_index('timestamp')['close']

def fetch_data_for_pairs(tickers, timeframe='1m'):
    """Fetch data for all tickers."""
    data = {}
    for ticker in tickers:
        data[ticker] = fetch_data(ticker, timeframe)
    return pd.DataFrame(data)

def calculate_hedge_ratio(asset1, asset2):
    """Calculate hedge ratio between two assets."""
    X = add_constant(asset1.values)
    model = OLS(asset2.values, X).fit()
    return model.params[1]

def cointegration_checker(crypto_dataframe):
    """Check for cointegration and return cointegrated pairs."""
    cointegrated_pairs = []
    k = crypto_dataframe.shape[1]
    p_values = np.ones((k, k))
    keys = crypto_dataframe.keys()
    
    for i in range(k):
        for j in range(i + 1, k):
            asset1 = crypto_dataframe[keys[i]]
            asset2 = crypto_dataframe[keys[j]]
            coint_test = coint(asset1, asset2)
            pvalue = coint_test[1]
            p_values[i, j] = pvalue
            if pvalue < 0.02:
                cointegrated_pairs.append((keys[i], keys[j]))
                
    return p_values, cointegrated_pairs

def generate_signals(price_ratio, z_score, hedge_ratio):
    """Generate trading signals based on Z-score."""
    if z_score.iloc[-1] > 1.25:
        return "Enter SHORT"
    elif z_score.iloc[-1] < -1.25:
        return "Enter LONG"
    elif abs(z_score.iloc[-1]) < 0.5:
        return "EXIT Position"
    return "Hold"

def main():
    while True:
        try:
            # Fetch all USDT pairs
            usdt_pairs = fetch_all_pairs()
            print(f"Fetched {len(usdt_pairs)} USDT pairs.")
            
            # Fetch live data for all pairs
            df = fetch_data_for_pairs(usdt_pairs)
            
            # Check for cointegrated pairs
            _, pairs = cointegration_checker(df)
            
            if pairs:
                for pair in pairs:
                    asset1, asset2 = pair
                    hedge_ratio = calculate_hedge_ratio(df[asset1], df[asset2])
                    
                    # Calculate Z-score
                    price_ratio = df[asset1] / df[asset2]
                    rolling_mean = price_ratio.rolling(window=20).mean()
                    rolling_std = price_ratio.rolling(window=20).std()
                    z_score = (price_ratio - rolling_mean) / rolling_std
                    
                    # Generate trading signals
                    signal = generate_signals(price_ratio, z_score, hedge_ratio)
                    print(f"Signal for {asset1}/{asset2}: {signal}")
                    
            # Sleep for a specific period before checking again
            time.sleep(3600)  # Wait for 1 hour before the next iteration
        
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)  # Wait for 1 minute before retrying

if __name__ == "__main__":
    main()
