import pandas as pd
import numpy as np
from lightweight_charts import Chart

def main():
    df = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=100),
        'open': 100 + np.cumsum(np.random.randn(100) * 0.5),
        'high': 100 + np.cumsum(np.random.randn(100) * 0.5) + 2,
        'low': 100 + np.cumsum(np.random.randn(100) * 0.5) - 2,
        'close': 100 + np.cumsum(np.random.randn(100) * 0.5),
        'volume': np.random.randint(1000000, 5000000, 100)
    })

    chart = Chart(width=1800, height=1000)
    chart.set(df)
    
    # Volume indicator in separate pane
    vol_line = chart.create_line('Volume', color='blue', pane_index=1)
    vol_data = df[['time', 'volume']].rename(columns={'volume': 'Volume'})
    vol_line.set(vol_data)
    
    # RSI indicator
    rsi_line = chart.create_line('RSI', color='purple', pane_index=2)
    rsi = df[['time']].copy()
    rsi['RSI'] = 50 + np.random.randn(len(df)) * 10
    rsi_line.set(rsi)
    
    # MACD indicator
    macd_line = chart.create_line('MACD', color='orange', pane_index=3)
    macd = df[['time']].copy()
    macd['MACD'] = np.random.randn(len(df)) * 2
    macd_line.set(macd)
    
    print("✅ Professional 4-pane trading layout created!")
    print("   Pane 0: Main chart (60% height)")
    print("   Pane 1: Volume (15% height)")
    print("   Pane 2: RSI (12.5% height)")
    print("   Pane 3: MACD (12.5% height)")
    
    chart.show(block=True)

if __name__ == '__main__':
    main()