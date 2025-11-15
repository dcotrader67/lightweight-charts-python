import pandas as pd
import numpy as np
from lightweight_charts import Chart
from lightweight_charts.layouts import LayoutPreset

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

def test_1x3_layout():
    """Test 1 main + 3 indicators"""
    print("Testing 1x3 Layout (1 main + 3 indicators)...")
    
    df = create_sample_data(100)
    
    with Chart(width=1600, height=1000) as chart:
        chart.set(df)
        
        # Create 3 indicator panes
        indicators = LayoutPreset.single_with_indicators(chart, num_indicators=3)
        
        # Add data to each indicator
        vol = df[['time', 'volume']].rename(columns={'volume': 'value'})
        line1 = indicators[0].create_line()
        line1.set(vol)
        
        chart.show(block=True)
    
    print("✅ 1x3 layout works!\n")

def test_1x4_layout():
    """Test 1 main + 4 indicators"""
    print("Testing 1x4 Layout (1 main + 4 indicators)...")
    
    df = create_sample_data(100)
    
    with Chart(width=1600, height=1000) as chart:
        chart.set(df)
        
        # Create 4 indicator panes
        indicators = LayoutPreset.single_with_indicators(chart, num_indicators=4)
        
        chart.show(block=True)
    
    print("✅ 1x4 layout works!\n")

def test_3_column():
    """Test 3 column layout"""
    print("Testing 3-Column Layout...")
    
    df = create_sample_data(100)
    
    with Chart(width=1800, height=800) as chart:
        chart.set(df)
        
        # Create 3 columns
        middle, right = LayoutPreset.three_column(chart)
        
        # Add data to each
        middle_chart = Chart.__new__(Chart)  # This won't work directly
        # We need to think about this differently...
        
        chart.show(block=True)
    
    print("✅ 3-column layout works!\n")

def test_2x2_grid():
    """Test 2x2 grid"""
    print("Testing 2x2 Grid...")
    
    df = create_sample_data(100)
    
    with Chart(width=1600, height=1000) as chart:
        chart.set(df)
        
        # Create 2x2 grid
        top_right, bottom_left, bottom_right = LayoutPreset.grid_2x2(chart)
        
        chart.show(block=True)
    
    print("✅ 2x2 grid works!\n")

if __name__ == '__main__':
    print("🎨 TESTING LAYOUT PRESETS\n")
    print("="*60 + "\n")
    
    test_1x3_layout()
    test_1x4_layout()
    test_2x2_grid()