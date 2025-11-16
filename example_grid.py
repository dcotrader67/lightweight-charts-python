"""
2x2 Grid - Clean Example (No Extra Window)
"""
import pandas as pd
import numpy as np
from lightweight_charts import Chart

def generate_sample_data(periods=200, timeframe='1H', base_price=150):
    """Generate realistic OHLCV data"""
    freq_map = {'1H': '1h', '4H': '4h', '1D': '1D', '1W': '1W'}
    dates = pd.date_range('2024-01-01', periods=periods, freq=freq_map.get(timeframe, '1h'))
    
    returns = np.random.randn(periods) * 0.02
    price = base_price * np.exp(np.cumsum(returns))
    
    df = pd.DataFrame({
        'time': dates,
        'open': price * (1 + np.random.randn(periods) * 0.005),
        'high': price * (1 + np.abs(np.random.randn(periods)) * 0.015),
        'low': price * (1 - np.abs(np.random.randn(periods)) * 0.015),
        'close': price,
        'volume': np.random.randint(100000, 5000000, periods)
    })
    
    df['high'] = df[['open', 'high', 'close']].max(axis=1)
    df['low'] = df[['low', 'open', 'close']].min(axis=1)
    
    return df

def main():
    print("\nGenerating data...")
    df_1h = generate_sample_data(periods=200, timeframe='1H')
    df_4h = generate_sample_data(periods=150, timeframe='4H')
    df_1d = generate_sample_data(periods=100, timeframe='1D')
    df_1w = generate_sample_data(periods=52, timeframe='1W')

    print("Creating 2x2 grid...")
    chart = Chart(width=1920, height=1080, title="Multi-Timeframe Analysis", toolbox=True)
    tl, tr, bl, br = chart.create_grid_2x2()
    
    print("Setting data...")
    tl.set(df_1h)
    tl.watermark('1H Chart')
    
    tr.set(df_4h)
    tr.watermark('4H Chart')
    
    bl.set(df_1d)
    bl.watermark('Daily Chart')
    
    br.set(df_1w)
    br.watermark('Weekly Chart')
    
    print("\n✅ Opening chart...\n")
    chart.show(block=True)

if __name__ == '__main__':
    main()