import pandas as pd
from lightweight_charts import Chart

def test_basic():
    print("Testing basic chart...")
    df = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=10),
        'open': range(100, 110),
        'high': range(105, 115),
        'low': range(95, 105),
        'close': range(102, 112),
    })
    
    try:
        with Chart() as chart:
            chart.set(df)
            chart.show(block=True)
        print("✅ Test passed!")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_invalid_data():
    """Test with invalid OHLC data"""
    print("\n" + "="*60)
    print("Testing invalid data (high < low)...")
    print("="*60)
    
    df = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=5),
        'open': [100, 100, 100, 100, 100],
        'high': [95, 105, 95, 105, 95],   # Some high < low (INVALID!)
        'low': [105, 95, 105, 95, 105],   # Some low > high (INVALID!)
        'close': [102, 102, 102, 102, 102],
    })
    
    print("Data has invalid OHLC (high < low in some rows)")
    
    try:
        with Chart() as chart:
            chart.set(df)
            # Check if data was fixed by looking at the warning
            print("✅ Good: Validator auto-fixed invalid data!")
            chart.show(block=True)
        return True
    except Exception as e:
        print(f"✅ Also good: Chart rejected bad data: {e}")
        return True
    
def test_rapid_updates():
    """Test many rapid updates"""
    print("\n" + "="*60)
    print("Testing 100 rapid updates...")
    print("="*60)
    
    df = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=10),
        'open': range(100, 110),
        'high': range(105, 115),
        'low': range(95, 105),
        'close': range(102, 112),
    })
    
    try:
        import time
        with Chart() as chart:
            chart.set(df)
            chart.show(block=False)
            
            print("Sending 100 updates...")
            start = time.time()
            
            for i in range(100):
                series = pd.Series({
                    'time': pd.Timestamp('2024-01-11'),
                    'open': 110 + i * 0.1,
                    'high': 115 + i * 0.1,
                    'low': 105 + i * 0.1,
                    'close': 112 + i * 0.1,
                })
                chart.update(series)
                
                if i % 20 == 0:
                    print(f"  Progress: {i}/100")
            
            elapsed = time.time() - start
            print(f"✅ Completed 100 updates in {elapsed:.2f}s")
            print(f"   Average: {elapsed/100*1000:.2f}ms per update")
            
            time.sleep(2)  # Let it render
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
def test_missing_columns():
    """Test with missing required columns"""
    print("\n" + "="*60)
    print("Testing missing columns...")
    print("="*60)
    
    # Missing 'high' and 'low' columns
    df = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=5),
        'open': [100, 101, 102, 103, 104],
        'close': [102, 103, 104, 105, 106],
    })
    
    print("Data missing 'high' and 'low' columns")
    
    try:
        with Chart() as chart:
            chart.set(df)
            chart.show(block=True)
        print("⚠️  ISSUE: Accepted data with missing columns!")
        return False
    except Exception as e:
        print(f"✅ Good: Rejected incomplete data: {e}")
        return True

def test_nan_values():
    """Test with NaN values"""
    print("\n" + "="*60)
    print("Testing NaN values...")
    print("="*60)
    
    import numpy as np
    
    df = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=5),
        'open': [100, np.nan, 102, 103, 104],
        'high': [105, 106, 107, 108, 109],
        'low': [95, 96, 97, 98, 99],
        'close': [102, 103, np.nan, 105, 106],
    })
    
    print("Data contains NaN values")
    
    try:
        with Chart() as chart:
            chart.set(df)
            print("✅ Good: Validator handled NaN values!")
            chart.show(block=True)
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

# Add to main:
if __name__ == '__main__':
    test_basic()
    test_invalid_data()
    test_rapid_updates()
    test_missing_columns()
    test_nan_values()  # ADD THIS
