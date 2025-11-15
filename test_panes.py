import pandas as pd
import numpy as np
from lightweight_charts import Chart

def create_sample_data(periods=100):
    """Create sample OHLCV data"""
    df = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=periods),
        'open': 100 + np.cumsum(np.random.randn(periods) * 0.5),
        'high': 100 + np.cumsum(np.random.randn(periods) * 0.5) + 2,
        'low': 100 + np.cumsum(np.random.randn(periods) * 0.5) - 2,
        'close': 100 + np.cumsum(np.random.randn(periods) * 0.5),
        'volume': np.random.randint(1000000, 5000000, periods)
    })
    return df

def test_basic_panes():
    """Test creating series in different panes using paneIndex"""
    print("Testing paneIndex-based multi-pane layout...")
    print("="*60)
    
    df = create_sample_data(100)
    
    with Chart(width=1800, height=1000) as chart:
        # Main chart - pane 0
        chart.set(df)
        print("✅ Main chart (pane 0)")
        
        # Create volume in pane 1
        print("Creating volume line in pane 1...")
        vol_line = chart.create_line('Volume', pane_index=1)
        vol_data = df[['time', 'volume']].rename(columns={'volume': 'Volume'})
        vol_line.set(vol_data)
        print("✅ Volume (pane 1)")
        
        # Create RSI in pane 2
        print("Creating RSI line in pane 2...")
        rsi_line = chart.create_line('RSI', color='rgba(255, 100, 100, 0.8)', pane_index=2)
        rsi = df[['time']].copy()
        rsi['RSI'] = 50 + np.random.randn(len(df)) * 10
        rsi_line.set(rsi)
        print("✅ RSI (pane 2)")
        
        # Create MACD in pane 3
        print("Creating MACD line in pane 3...")
        macd_line = chart.create_line('MACD', color='rgba(100, 255, 100, 0.8)', pane_index=3)
        macd = df[['time']].copy()
        macd['MACD'] = np.random.randn(len(df)) * 2
        macd_line.set(macd)
        print("✅ MACD (pane 3)")
        
        print(f"\nShowing chart with 4 panes...")
        
        chart.show(block=True)
    
    print("\n✅ Test complete!")

if __name__ == '__main__':
    print("\n🎨 TESTING V5 PANE SYSTEM\n")
    test_basic_panes()