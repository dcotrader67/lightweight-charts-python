import pandas as pd
import numpy as np
from lightweight_charts import Chart
from lightweight_charts.layouts import LayoutPreset

def generate_ohlcv(periods, freq, base_price=150):
    """Generate OHLCV data"""
    if freq == '4h':
        dates = pd.date_range('2024-06-01', periods=periods, freq='4h')
    elif freq == '1h':
        dates = pd.date_range('2024-06-01 09:30:00', periods=periods, freq='1h')
    elif freq == '15min':
        dates = pd.date_range('2024-06-01 09:30:00', periods=periods, freq='15min')
    elif freq == '2min':
        dates = pd.date_range('2024-06-01 09:30:00', periods=periods, freq='2min')
    
    price = base_price + np.cumsum(np.random.randn(periods) * 0.5)
    
    df = pd.DataFrame({
        'time': dates,
        'open': price + np.random.randn(periods) * 0.3,
        'high': price + np.abs(np.random.randn(periods)) * 1.5,
        'low': price - np.abs(np.random.randn(periods)) * 1.5,
        'close': price,
        'volume': np.random.randint(100000, 500000, periods)
    })
    df['high'] = df[['open', 'high', 'close']].max(axis=1) + 0.3
    df['low'] = df[['open', 'low', 'close']].min(axis=1) - 0.3
    
    return df

def calculate_simple_vwap(df):
    """Simple VWAP"""
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    vwap_values = []
    for i in range(len(df)):
        cum_tp_volume = (typical_price.iloc[:i+1] * df['volume'].iloc[:i+1]).sum()
        cum_volume = df['volume'].iloc[:i+1].sum()
        vwap_values.append(cum_tp_volume / cum_volume if cum_volume > 0 else typical_price.iloc[i])
    
    result = df[['time']].copy()
    result['VWAP'] = vwap_values
    return result

if __name__ == '__main__':
    print("\n" + "="*70)
    print("2x2 MULTI-TIMEFRAME GRID WITH VWAP")
    print("="*70)
    
    # Generate data
    df_4h = generate_ohlcv(20, '4h', base_price=150)
    df_1h = generate_ohlcv(48, '1h', base_price=150)
    df_15min = generate_ohlcv(100, '15min', base_price=150)
    df_2min = generate_ohlcv(300, '2min', base_price=150)
    
    # Calculate VWAPs
    vwap_4h = calculate_simple_vwap(df_4h)
    vwap_1h = calculate_simple_vwap(df_1h)
    vwap_15min = calculate_simple_vwap(df_15min)
    vwap_2min = calculate_simple_vwap(df_2min)
    
    # ============================================
    # TOP-LEFT: 4H Chart
    # ============================================
    chart = Chart(width=1920, height=1080)
    chart.set(df_4h)
    
    # Add VWAP to 4H
    vwap_line_4h = chart.create_line('VWAP', color='rgba(255, 193, 7, 0.9)', width=2)
    vwap_line_4h.set(vwap_4h)
    
    chart.watermark('4H', font_size=36)
    chart.legend(visible=True, ohlc=True, lines=True)
    chart.layout(background_color='#0C0D0F', text_color='#D8D9DB')
    chart.grid(vert_enabled=True, horz_enabled=True, color='rgba(42, 46, 57, 0.5)')
    
    print("✅ Top-Left: 4H with VWAP")
    
    # ============================================
    # Create 2x2 Grid
    # ============================================
    top_right, bottom_left, bottom_right = LayoutPreset.grid_2x2(chart)
    
    # ============================================
    # TOP-RIGHT: 1H Chart
    # ============================================
    top_right.set(df_1h)
    
    # Add VWAP to 1H
    vwap_line_1h = top_right.create_line('VWAP', color='rgba(255, 193, 7, 0.9)', width=2)
    vwap_line_1h.set(vwap_1h)
    
    top_right.watermark('1H', font_size=36)
    top_right.legend(visible=True, ohlc=True, lines=True)
    top_right.layout(background_color='#0C0D0F', text_color='#D8D9DB')
    top_right.grid(vert_enabled=True, horz_enabled=True, color='rgba(42, 46, 57, 0.5)')
    
    print("✅ Top-Right: 1H with VWAP")
    
    # ============================================
    # BOTTOM-LEFT: 15-min Chart
    # ============================================
    bottom_left.set(df_15min)
    
    # Add VWAP to 15-min
    vwap_line_15m = bottom_left.create_line('VWAP', color='rgba(255, 193, 7, 0.9)', width=2)
    vwap_line_15m.set(vwap_15min)
    
    bottom_left.watermark('15-MIN', font_size=36)
    bottom_left.legend(visible=True, ohlc=True, lines=True)
    bottom_left.layout(background_color='#0C0D0F', text_color='#D8D9DB')
    bottom_left.grid(vert_enabled=True, horz_enabled=True, color='rgba(42, 46, 57, 0.5)')
    
    print("✅ Bottom-Left: 15-min with VWAP")
    
    # ============================================
    # BOTTOM-RIGHT: 2-min Chart
    # ============================================
    bottom_right.set(df_2min)
    
    # Add VWAP to 2-min
    vwap_line_2m = bottom_right.create_line('VWAP', color='rgba(255, 193, 7, 0.9)', width=2)
    vwap_line_2m.set(vwap_2min)
    
    bottom_right.watermark('2-MIN', font_size=36)
    bottom_right.legend(visible=True, ohlc=True, lines=True)
    bottom_right.layout(background_color='#0C0D0F', text_color='#D8D9DB')
    bottom_right.grid(vert_enabled=True, horz_enabled=True, color='rgba(42, 46, 57, 0.5)')
    
    print("✅ Bottom-Right: 2-min with VWAP")
    
    print("="*70)
    print("\n🎉 SUCCESS! 2x2 GRID WITH ALL TIMEFRAMES:")
    print("   Top-Left:     4H + VWAP + Volume")
    print("   Top-Right:    1H + VWAP + Volume")
    print("   Bottom-Left:  15-min + VWAP + Volume")
    print("   Bottom-Right: 2-min + VWAP + Volume")
    print("\n📊 Each chart has:")
    print("   • Candlesticks with volume")
    print("   • VWAP overlay")
    print("   • Independent scaling")
    print("   • Professional styling\n")
    
    chart.show(block=True)

if __name__ == '__main__':
    main()