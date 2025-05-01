import yfinance as yf
from ta.momentum import StochasticOscillator
from ta.trend import SMAIndicator
from tradingview_ta import TA_Handler, Interval, Exchange
import winsound
import time
import datetime

# Global variable to store the initial recommendation
initial_recommendation = None
# Global variable to store the previous recommendation
prev_recommendation = None

def fetch_crypto_data_yahoo(symbol='BTC-USD', start_date=None, end_date=None, interval='1d'):
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
    return data[['Open', 'High', 'Low', 'Close', 'Volume']]

def calculate_stochastic(prices):
    stochastic = StochasticOscillator(high=prices['High'], low=prices['Low'], close=prices['Close'], window=14, smooth_window=3)
    K = stochastic.stoch()
    D = stochastic.stoch_signal()
    return K, D

def check_stochastic_indicator(prices):
    global prev_recommendation, initial_recommendation
    K, D = calculate_stochastic(prices)
    # Use .iloc to access elements by position
    if D.iloc[-1] < D.iloc[-2]:
        print("🔻 Stochastic %D inverted down.")
    elif D.iloc[-1] > D.iloc[-2]:
        print("🔺 Stochastic %D inverted up.")
        if prev_recommendation is not None and prev_recommendation != initial_recommendation:
            winsound.Beep(1000, 500)  # Play alert sound if recommendation changes
        prev_recommendation = "Stochastic %D inverted up."

def calculate_sma(prices):
    sma_indicator = SMAIndicator(close=prices['Close'], window=20)
    sma = sma_indicator.sma_indicator()
    return sma

def check_sma_indicator(prices):
    global prev_recommendation, initial_recommendation
    sma = calculate_sma(prices)
    # Use .iloc to access elements by position
    if prices['Close'].iloc[-1] > sma.iloc[-1]:
        print("🔺 Price is above the 20-day Simple Moving Average.")
    elif prices['Close'].iloc[-1] < sma.iloc[-1]:
        print("🔻 Price is below the 20-day Simple Moving Average.")
        if prev_recommendation is not None and prev_recommendation != initial_recommendation:
            winsound.Beep(1000, 500)  # Play alert sound if recommendation changes
        prev_recommendation = "Price is below the 20-day Simple Moving Average."

def get_tradingview_ta(symbol="BTCUSDT", exchange="BINANCE", screener="crypto", interval=Interval.INTERVAL_1_DAY):
    handler = TA_Handler(
        symbol=symbol,
        exchange=exchange,
        screener=screener,
        interval=interval
    )
    analysis = handler.get_analysis()
    return analysis.summary

def display_tradingview_summary():
    # Display summary for 1-day interval
    summary_1d = get_tradingview_ta(interval=Interval.INTERVAL_1_DAY)
    print("TradingView TA Summary (1 Day Interval):", summary_1d)

    # Display summary for hourly interval
    summary_1h = get_tradingview_ta(interval=Interval.INTERVAL_1_HOUR)
    print("TradingView TA Summary (1 Hour Interval):", summary_1h)

    # Display summary for 15-minute interval
    summary_15m = get_tradingview_ta(interval=Interval.INTERVAL_15_MINUTES)
    print("TradingView TA Summary (15 Min Interval):", summary_15m)

# Example usage
symbol = 'BTC-USD'
start_date = (datetime.datetime.now() - datetime.timedelta(days=60)).strftime('%Y-%m-%d')  # 60 days ago
end_date = datetime.datetime.now().strftime('%Y-%m-%d')
interval = '1d'

# Get the initial recommendation
crypto_data = fetch_crypto_data_yahoo(symbol=symbol, start_date=start_date, end_date=end_date, interval=interval)
check_stochastic_indicator(crypto_data)
check_sma_indicator(crypto_data)
initial_recommendation = prev_recommendation

while True:
    # Get the current time and print it
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Current time: {current_time}")

    crypto_data = fetch_crypto_data_yahoo(symbol=symbol, start_date=start_date, end_date=end_date, interval=interval)
    check_stochastic_indicator(crypto_data)
    check_sma_indicator(crypto_data)
    
    display_tradingview_summary()
    
    time.sleep(15 * 60)  # Delay for 15 minutes before checking again
