import pandas as pd
import numpy as np
from lightweight_charts.trading_layouts import TradingLayout, IndicatorBuilder

def main():
    # Generate intraday-style data
    periods = 200
    start_date = pd.Timestamp('2024-06-01 09:30:00')
    dates = pd.date_range(start=start_date, periods=periods, freq='15min')
    
    price = 150 + np.cumsum(np.random.randn(periods) * 0.5)
    
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
    
    print("\n" + "="*70)
    print("ADVANCED ANCHORED VWAP FEATURES")
    print("="*70)
    
    # 1. Session VWAP (anchored to market open)
    vwap_session = IndicatorBuilder.anchored_vwap(
        df, 
        '2024-06-01',  # Will default to 09:30:00
        session_open='09:30:00'
    )
    print("✅ Session VWAP: Anchored to 2024-06-01 09:30:00 (market open)")
    
    # 2. News Event VWAP (specific time)
    vwap_news = IndicatorBuilder.anchored_vwap(
        df,
        '2024-06-01 14:00:00'  # Fed announcement time
    )
    print("✅ News VWAP: Anchored to 2024-06-01 14:00:00 (Fed announcement)")
    
    # 3. Swing High VWAP (anchored to high of specific candle)
    vwap_swing_high = IndicatorBuilder.anchored_vwap(
        df,
        '2024-06-01 11:30:00',
        anchor_price='high'
    )
    print("✅ Swing High VWAP: Anchored to high at 2024-06-01 11:30:00")
    
    # 4. Key Level VWAP (anchored to specific price)
    vwap_key_level = IndicatorBuilder.anchored_vwap(
        df,
        '2024-06-01 10:00:00',
        anchor_price=152.50
    )
    print("✅ Key Level VWAP: Anchored to $152.50 at 2024-06-01 10:00:00")
    
    # 5. Multiple anchored VWAPs at once
    multiple_vwaps = IndicatorBuilder.multiple_anchored_vwaps(
        df,
        anchors=[
            {
                'datetime': '2024-06-01 09:30:00',
                'label': 'Session Open'
            },
            {
                'datetime': '2024-06-01 12:00:00',
                'price': 'high',
                'label': 'Morning High'
            },
            {
                'datetime': '2024-06-01 14:00:00',
                'price': 151.00,
                'label': 'Key Support'
            }
        ]
    )
    print("✅ Multiple VWAPs: Session Open, Morning High, Key Support")
    
    # 6. VWAP with bands
    vwap_bands = IndicatorBuilder.vwap_bands(
        df,
        anchor_datetime='2024-06-01',
        num_std=2.0
    )
    print("✅ VWAP Bands: 2-sigma deviation bands")
    
    print("="*70)
    
    # Create the chart
    chart, subcharts = TradingLayout.create_with_overlays(
        df,
        overlays={
            **multiple_vwaps,  # All 3 anchored VWAPs
            # **vwap_bands,    # Uncomment to add bands instead
        },
        indicators={
            'RSI': IndicatorBuilder.rsi(df)
        },
        watermark='ADVANCED ANCHORED VWAP',
        volume_pane=True
    )
    
    print("\n💡 ANCHOR OPTIONS:")
    print("   📅 Date only: '2024-06-01' → defaults to session_open time")
    print("   ⏰ Date + Time: '2024-06-01 14:30:00' → exact time")
    print("   📊 Price: 'high'/'low'/'open'/'close' → candle feature")
    print("   💰 Price: 150.50 → specific price level")
    print("\n🎯 USE CASES:")
    print("   • Earnings announcements")
    print("   • Fed meetings / Economic data")
    print("   • Swing highs/lows")
    print("   • Key support/resistance breaks")
    print("   • Session opens/closes\n")
    
    chart.show(block=True)

if __name__ == '__main__':
    main()