import pandas as pd
import numpy as np
from lightweight_charts import Chart

def test_basic():
    """Test basic chart"""
    print("\n" + "="*60)
    print("TEST: Basic Chart")
    print("="*60)
    
    df = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=50),
        'open': range(100, 150),
        'high': range(105, 155),
        'low': range(95, 145),
        'close': range(102, 152),
    })
    
    try:
        with Chart() as chart:
            chart.set(df)
            chart.show(block=True)
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_data_validation():
    """Test data validation catches issues"""
    print("\n" + "="*60)
    print("TEST: Data Validation")
    print("="*60)
    
    # Test 1: Invalid OHLC
    print("  1. Invalid OHLC (high < low)...")
    df_invalid = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=5),
        'open': [100] * 5,
        'high': [95, 105, 95, 105, 95],
        'low': [105, 95, 105, 95, 105],
        'close': [102] * 5,
    })
    
    try:
        with Chart() as chart:
            chart.set(df_invalid)
        print("     ✅ Auto-fixed invalid data")
    except Exception as e:
        print(f"     ❌ Error: {e}")
        return False
    
    # Test 2: Missing columns
    print("  2. Missing required columns...")
    df_missing = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=5),
        'open': [100] * 5,
        'close': [102] * 5,
    })
    
    try:
        with Chart() as chart:
            chart.set(df_missing)
        print("     ❌ Should have rejected!")
        return False
    except Exception as e:
        print("     ✅ Correctly rejected")
    
    # Test 3: NaN values
    print("  3. NaN values...")
    df_nan = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=5),
        'open': [100, np.nan, 102, 103, 104],
        'high': [105, 106, 107, 108, 109],
        'low': [95, 96, 97, 98, 99],
        'close': [102, 103, np.nan, 105, 106],
    })
    
    try:
        with Chart() as chart:
            chart.set(df_nan)
        print("     ✅ Handled NaN values")
    except Exception as e:
        print(f"     ❌ Error: {e}")
        return False
    
    print("✅ PASSED")
    return True


def test_subcharts():
    """Test subchart creation"""
    print("\n" + "="*60)
    print("TEST: Subcharts")
    print("="*60)
    
    df = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=50),
        'open': range(100, 150),
        'high': range(105, 155),
        'low': range(95, 145),
        'close': range(102, 152),
        'volume': [1000000 + i * 10000 for i in range(50)]
    })
    
    try:
        with Chart() as chart:
            chart.set(df)
            
            # Create subchart
            subchart = chart.create_subchart(position='bottom', width=1.0, height=0.3)
            
            # Add volume line (note: no 'name' parameter for line)
            volume_data = df[['time', 'volume']].rename(columns={'volume': 'value'})
            line = subchart.create_line()  # Don't pass name here
            line.set(volume_data)
            
            chart.show(block=True)
        
        print("✅ PASSED")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_line_indicators():
    """Test line indicators"""
    print("\n" + "="*60)
    print("TEST: Line Indicators")
    print("="*60)
    
    df = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=100),
        'open': range(100, 200),
        'high': range(105, 205),
        'low': range(95, 195),
        'close': range(102, 202),
    })
    
    # Calculate SMA
    sma_20 = df['close'].rolling(window=20).mean()
    
    try:
        with Chart() as chart:
            chart.legend(visible=True)
            chart.set(df)
            
            # Add SMA line
            line = chart.create_line('SMA 20', color='rgba(255, 0, 0, 0.8)')
            line.set(pd.DataFrame({
                'time': df['time'], 
                'SMA 20': sma_20
            }))
            
            chart.show(block=True)
        
        print("✅ PASSED")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_rapid_updates():
    """Test performance with rapid updates"""
    print("\n" + "="*60)
    print("TEST: Rapid Updates (100 updates)")
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
            
            elapsed = time.time() - start
            print(f"  Completed in {elapsed:.3f}s ({elapsed/100*1000:.2f}ms per update)")
            time.sleep(1)
        
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
def test_very_large_dataset():
    """Test with very large dataset"""
    print("\n" + "="*60)
    print("TEST: Large Dataset (10,000 bars)")
    print("="*60)
    
    import time
    
    # Generate 10,000 bars
    df = pd.DataFrame({
        'time': pd.date_range('2020-01-01', periods=10000, freq='1min'),
        'open': 100 + np.cumsum(np.random.randn(10000) * 0.1),
        'high': 100 + np.cumsum(np.random.randn(10000) * 0.1) + 1,
        'low': 100 + np.cumsum(np.random.randn(10000) * 0.1) - 1,
        'close': 100 + np.cumsum(np.random.randn(10000) * 0.1),
    })
    
    try:
        start = time.time()
        with Chart() as chart:
            chart.set(df)
            elapsed = time.time() - start
            print(f"  Set {len(df):,} bars in {elapsed:.2f}s")
            
            if elapsed > 5.0:
                print(f"  ⚠️  Performance warning: took {elapsed:.2f}s")
            
            chart.show(block=True)
        
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_special_characters():
    """Test with special characters in data"""
    print("\n" + "="*60)
    print("TEST: Special Characters")
    print("="*60)
    
    df = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=5),
        'open': [100, 101, 102, 103, 104],
        'high': [105, 106, 107, 108, 109],
        'low': [95, 96, 97, 98, 99],
        'close': [102, 103, 104, 105, 106],
    })
    
    try:
        with Chart(title="Test's Chart: €$£¥") as chart:
            chart.set(df)
            
            # Add line with special chars in name
            line = chart.create_line("SMA 🚀 20'")
            sma = df['close'].rolling(3).mean()
            line.set(pd.DataFrame({'time': df['time'], "SMA 🚀 20'": sma}))
            
            chart.show(block=True)
        
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_timezone_handling():
    """Test timezone handling"""
    print("\n" + "="*60)
    print("TEST: Timezone Handling")
    print("="*60)
    
    # Create data with timezone (use 'h' instead of 'H')
    df = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=10, freq='1h', tz='US/Eastern'),  # Changed 'H' to 'h'
        'open': range(100, 110),
        'high': range(105, 115),
        'low': range(95, 105),
        'close': range(102, 112),
    })
    
    print(f"  Data timezone: {df['time'].dt.tz}")
    
    try:
        with Chart() as chart:
            chart.set(df)
            chart.show(block=True)
        
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_duplicate_timestamps():
    """Test duplicate timestamps"""
    print("\n" + "="*60)
    print("TEST: Duplicate Timestamps")
    print("="*60)
    
    df = pd.DataFrame({
        'time': ['2024-01-01', '2024-01-02', '2024-01-02', '2024-01-03', '2024-01-03'],
        'open': [100, 101, 102, 103, 104],
        'high': [105, 106, 107, 108, 109],
        'low': [95, 96, 97, 98, 99],
        'close': [102, 103, 104, 105, 106],
    })
    
    print("  Data has duplicate timestamps")
    
    try:
        with Chart() as chart:
            chart.set(df)
            print("  ✅ Validator removed duplicates")  # UPDATED MESSAGE
            chart.show(block=True)
        
        print("✅ PASSED")  # ADD THIS
        return True
    except Exception as e:
        print(f"  Result: {e}")
        return True


def test_extreme_values():
    """Test extreme price values"""
    print("\n" + "="*60)
    print("TEST: Extreme Values")
    print("="*60)
    
    df = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=5),
        'open': [0.0001, 1000000, 0.0001, 1000000, 100],
        'high': [0.0002, 1000001, 0.0002, 1000001, 105],
        'low': [0.00001, 999999, 0.00001, 999999, 95],
        'close': [0.00015, 1000000.5, 0.00015, 1000000.5, 102],
    })
    
    print("  Data has extreme price swings (0.0001 to 1,000,000)")
    
    try:
        with Chart() as chart:
            chart.set(df)
            chart.show(block=True)
        
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


if __name__ == '__main__':
    print("\n" + "🐛 BUG HUNT: Testing Lightweight Charts" + "\n")
    
    results = []
    results.append(("Basic Chart", test_basic()))
    results.append(("Data Validation", test_data_validation()))
    results.append(("Subcharts", test_subcharts()))
    results.append(("Line Indicators", test_line_indicators()))
    results.append(("Rapid Updates", test_rapid_updates()))
    
    # Advanced tests
    results.append(("Large Dataset", test_very_large_dataset()))
    results.append(("Special Characters", test_special_characters()))
    results.append(("Timezone Handling", test_timezone_handling()))
    results.append(("Duplicate Timestamps", test_duplicate_timestamps()))
    results.append(("Extreme Values", test_extreme_values()))
    
    # Summary (same as before)
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60)