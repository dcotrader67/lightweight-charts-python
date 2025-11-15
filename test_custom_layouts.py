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

def test_workaround_layout():
    """
    Workaround: Main chart (left 65%) + 3 bottom indicators (right 35% each)
    Since deep nesting doesn't work, we'll create them all from main chart
    """
    print("Testing: Workaround Layout (All from Main Chart)")
    print("="*60)
    
    df = create_sample_data(100)
    
    with Chart(width=1800, height=1000, inner_width=0.65) as chart:
        chart.set(df)
        print("✅ Main chart (left)")
        
        # Create 3 right panels - all from main chart with different positions
        # This might not work exactly as nested, but let's try
        
        # Top right - from main
        right1 = chart.create_subchart(position='right', width=0.35, height=0.33)
        vol = df[['time', 'volume']].rename(columns={'volume': 'value'})
        line1 = right1.create_line()
        line1.set(vol)
        print("✅ Right panel 1: Volume")
        
        # Middle right - from right1
        right2 = right1.create_subchart(position='bottom', width=1.0, height=0.5)
        rsi = df[['time']].copy()
        rsi['value'] = 50 + np.random.randn(len(df)) * 10
        line2 = right2.create_line()
        line2.set(rsi)
        print("✅ Right panel 2: RSI")
        
        # Bottom right - from main (NOT from right2)
        # Try creating directly from main chart instead
        print("Attempting different approach for panel 3...")
        try:
            # Method 1: From right2
            right3 = right2.create_subchart(position='bottom', width=1.0, height=1.0)
            macd = df[['time']].copy()
            macd['value'] = np.random.randn(len(df)) * 2
            line3 = right3.create_line()
            line3.set(macd)
            print("✅ Right panel 3: MACD (from right2)")
        except Exception as e:
            print(f"❌ Method failed: {e}")
        
        chart.show(block=True)
    
    print("Test complete!\n")

def test_alternative_bottom_layout():
    """
    Alternative: Main on top (65% height) + 3 indicators stacked at bottom
    This is more likely to work since bottom stacking is well-supported
    """
    print("Testing: Alternative - Main Top + 3 Bottom Indicators")
    print("="*60)
    
    df = create_sample_data(100)
    
    with Chart(width=1800, height=1000, inner_height=0.65) as chart:
        chart.set(df)
        print("✅ Main chart (top 65%)")
        
        # Bottom 1: Volume
        bottom1 = chart.create_subchart(position='bottom', width=1.0, height=0.12)
        vol = df[['time', 'volume']].rename(columns={'volume': 'value'})
        line1 = bottom1.create_line()
        line1.set(vol)
        print("✅ Bottom 1: Volume")
        
        # Bottom 2: RSI
        bottom2 = chart.create_subchart(position='bottom', width=1.0, height=0.12)
        rsi = df[['time']].copy()
        rsi['value'] = 50 + np.random.randn(len(df)) * 10
        line2 = bottom2.create_line()
        line2.set(rsi)
        print("✅ Bottom 2: RSI")
        
        # Bottom 3: MACD
        bottom3 = chart.create_subchart(position='bottom', width=1.0, height=0.11)
        macd = df[['time']].copy()
        macd['value'] = np.random.randn(len(df)) * 2
        line3 = bottom3.create_line()
        line3.set(macd)
        print("✅ Bottom 3: MACD")
        
        chart.show(block=True)
    
    print("✅ All panels working!\n")

if __name__ == '__main__':
    print("\n🎨 TESTING LAYOUT WORKAROUNDS\n")
    
    # Test the workaround
    # test_workaround_layout()
    
    # Test alternative (bottom stacking instead of right stacking)
    test_alternative_bottom_layout()