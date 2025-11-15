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

def test_subchart_positions():
    """Test all subchart positions"""
    print("\n" + "="*60)
    print("Testing Subchart Positions")
    print("="*60)
    
    df = create_sample_data(50)
    
    try:
        with Chart(width=1400, height=900) as chart:
            chart.set(df)
            
            # Test bottom subchart - DON'T pass name to create_line
            print("Creating bottom subchart...")
            bottom = chart.create_subchart(position='bottom', width=1.0, height=0.2)
            vol_data = df[['time', 'volume']].rename(columns={'volume': 'value'})
            line = bottom.create_line()  # No name here!
            line.set(vol_data)
            print("  ✅ Bottom subchart works!")
            
            # Test right subchart
            print("Creating right subchart...")
            try:
                right = chart.create_subchart(position='right', width=0.25, height=1.0)
                rsi_data = df[['time']].copy()
                rsi_data['value'] = 50
                line2 = right.create_line()
                line2.set(rsi_data)
                print("  ✅ Right subchart works!")
            except Exception as e:
                print(f"  ❌ Right subchart failed: {e}")
            
            # Test left subchart
            print("Creating left subchart...")
            try:
                left = chart.create_subchart(position='left', width=0.25, height=1.0)
                print("  ✅ Left subchart created!")
            except Exception as e:
                print(f"  ❌ Left subchart failed: {e}")
            
            # Test top subchart
            print("Creating top subchart...")
            try:
                top = chart.create_subchart(position='top', width=1.0, height=0.2)
                print("  ✅ Top subchart created!")
            except Exception as e:
                print(f"  ❌ Top subchart failed: {e}")
            
            chart.show(block=True)
        
        print("\n✅ Position test complete")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_subcharts():
    """Test multiple subcharts stacked"""
    print("\n" + "="*60)
    print("Testing Multiple Subcharts (1 main + 3 indicators)")
    print("="*60)
    
    df = create_sample_data(50)
    
    try:
        with Chart(width=1400, height=900, inner_height=0.5) as chart:
            chart.set(df)
            
            # Create 3 subcharts below main
            print("Creating subchart 1: Volume...")
            sub1 = chart.create_subchart(position='bottom', width=1.0, height=0.15)
            vol_data = df[['time', 'volume']].rename(columns={'volume': 'value'})
            line1 = sub1.create_line()
            line1.set(vol_data)
            
            print("Creating subchart 2: RSI...")
            sub2 = chart.create_subchart(position='bottom', width=1.0, height=0.15)
            line2 = sub2.create_line()
            rsi = df[['time']].copy()
            rsi['value'] = 50
            line2.set(rsi)
            
            print("Creating subchart 3: MACD...")
            sub3 = chart.create_subchart(position='bottom', width=1.0, height=0.15)
            line3 = sub3.create_line()
            macd = df[['time']].copy()
            macd['value'] = 0
            line3.set(macd)
            
            print("  ✅ Created 3 subcharts successfully")
            
            chart.show(block=True)
        
        print("\n✅ Multiple subcharts work!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_grid_layouts():
    """Test creating grid-like layouts"""
    print("\n" + "="*60)
    print("Testing Grid Layouts (2x2, 3x3 attempts)")
    print("="*60)
    
    df = create_sample_data(50)
    
    # Test 1: Simple 2-pane vertical split
    print("\n1. Testing 2-pane vertical split...")
    try:
        with Chart(width=1600, height=800, inner_width=0.5) as chart:
            chart.set(df)
            
            # Right pane
            right = chart.create_subchart(position='right', width=0.5, height=1.0)
            line = right.create_line()
            vol = df[['time', 'volume']].rename(columns={'volume': 'value'})
            line.set(vol)
            
            chart.show(block=True)
        print("  ✅ 2-pane vertical works!")
    except Exception as e:
        print(f"  ❌ Failed: {e}")
    
    # Test 2: Try 2x2 grid
    print("\n2. Testing 2x2 grid (main + right + bottom + bottom-right)...")
    try:
        with Chart(width=1600, height=900, inner_width=0.5, inner_height=0.5) as chart:
            chart.set(df)
            
            # Top-right
            top_right = chart.create_subchart(position='right', width=0.5, height=0.5)
            
            # Bottom-left (under main)
            bottom_left = chart.create_subchart(position='bottom', width=0.5, height=0.5)
            
            # Bottom-right
            # Note: This might not work as expected
            try:
                bottom_right = bottom_left.create_subchart(position='right', width=0.5, height=1.0)
                print("  ✅ Nested subchart works!")
            except Exception as e:
                print(f"  ⚠️  Nested subchart failed: {e}")
            
            chart.show(block=True)
        print("  ✅ Basic 2x2 structure created")
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
    
    return True


if __name__ == '__main__':
    print("🎨 CHART LAYOUT TESTING\n")
    
    results = []
    results.append(("Subchart Positions", test_subchart_positions()))
    results.append(("Multiple Subcharts", test_multiple_subcharts()))
    results.append(("Grid Layouts", test_grid_layouts()))
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status}  {name}")
    print("="*60)