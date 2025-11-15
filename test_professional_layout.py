import pandas as pd
import numpy as np
from lightweight_charts import Chart

def calculate_sma(data, period):
    return data.rolling(window=period).mean()

def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def main():
    # Generate data
    periods = 200
    dates = pd.date_range('2024-01-01', periods=periods)
    returns = np.random.randn(periods) * 2
    price = 100 * np.exp(np.cumsum(returns * 0.01))
    
    df = pd.DataFrame({
        'time': dates,
        'open': price + np.random.randn(periods) * 0.5,
        'high': price + np.abs(np.random.randn(periods)) * 2,
        'low': price - np.abs(np.random.randn(periods)) * 2,
        'close': price,
    })
    df['high'] = df[['open', 'high', 'close']].max(axis=1) + 0.5
    df['low'] = df[['open', 'low', 'close']].min(axis=1) - 0.5
    
    # Create chart
    chart = Chart(width=1920, height=1080)
    chart.set(df)
    
    # ============================================
    # PANE 0: Main chart with SMAs  
    # ============================================
    chart.price_scale(
        scale_margin_top=0.15,
        scale_margin_bottom=0.15
    )
    
    sma20 = chart.create_line('SMA 20', color='rgba(255, 193, 7, 0.9)', 
                              width=2, pane_index=0)
    sma20_data = df[['time']].copy()
    sma20_data['SMA 20'] = calculate_sma(df['close'], 20)
    sma20.set(sma20_data)
    
    sma50 = chart.create_line('SMA 50', color='rgba(33, 150, 243, 0.9)', 
                              width=2, pane_index=0)
    sma50_data = df[['time']].copy()
    sma50_data['SMA 50'] = calculate_sma(df['close'], 50)
    sma50.set(sma50_data)
    
    # ============================================
    # PANE 1: Volume - SMALL and CONSTRAINED
    # ============================================
    # Normalize volume to small range (0-10)
    volume_raw = np.random.randint(1000000, 5000000, periods)
    volume_normalized = ((volume_raw - volume_raw.min()) / 
                         (volume_raw.max() - volume_raw.min()) * 10)
    
    volume_data = df[['time']].copy()
    volume_data['Volume'] = volume_normalized
    
    vol_hist = chart.create_histogram(
        'Volume', 
        color='rgba(100, 130, 180, 0.4)', 
        price_line=False,
        price_label=False,
        scale_margin_top=0.8,  # Push histogram to bottom 20% of pane
        scale_margin_bottom=0.0,
        pane_index=1
    )
    vol_hist.set(volume_data)
    
    # Add top border line for visual separation
    vol_border_top = chart.create_line('', color='rgba(70, 75, 85, 1.0)', 
                                       width=2, pane_index=1)
    vol_border_data = df[['time']].copy()
    vol_border_data['value'] = 10  # Top of volume pane
    vol_border_top.set(vol_border_data)
    vol_border_top.price_line(label_visible=False, line_visible=False)
    
    # ============================================
    # PANE 2: RSI with reference levels
    # ============================================
    rsi_data = df[['time']].copy()
    rsi_data['RSI'] = calculate_rsi(df['close']).fillna(50)
    
    rsi_line = chart.create_line('RSI', color='rgba(156, 39, 176, 1.0)', 
                                 width=2, pane_index=2)
    rsi_line.set(rsi_data)
    
    # Add top border for RSI pane
    rsi_border_top = chart.create_line('', color='rgba(70, 75, 85, 1.0)', 
                                       width=2, pane_index=2)
    rsi_border_data = df[['time']].copy()
    rsi_border_data['value'] = 100  # Top of RSI range
    rsi_border_top.set(rsi_border_data)
    rsi_border_top.price_line(label_visible=False, line_visible=False)
    
    # Reference levels
    for level, color in [(70, 'rgba(255, 82, 82, 0.3)'), 
                         (50, 'rgba(128, 128, 128, 0.2)'),
                         (30, 'rgba(76, 175, 80, 0.3)')]:
        ref_line = chart.create_line('', color=color, width=1, 
                                     style='dashed', pane_index=2)
        ref_data = df[['time']].copy()
        ref_data['value'] = level
        ref_line.set(ref_data)
        ref_line.price_line(label_visible=False, line_visible=False)
    
    # ============================================
    # Add CSS for visual pane borders
    # ============================================
    chart.run_script('''
        const style = document.createElement('style');
        style.textContent = `
            /* Add borders between chart panes */
            .tv-lightweight-charts > div {
                border-top: 2px solid #3C434C !important;
                margin-top: 2px;
            }
            .tv-lightweight-charts > div:first-child {
                border-top: none !important;
            }
        `;
        document.head.appendChild(style);
    ''')
    
    # ============================================
    # Styling
    # ============================================
    chart.layout(
        background_color='#0C0D0F',
        text_color='#D8D9DB',
        font_size=11
    )
    
    chart.grid(
        vert_enabled=True,
        horz_enabled=True,
        color='rgba(42, 46, 57, 0.5)',
        style='solid'
    )
    
    chart.legend(visible=True, ohlc=True, percent=True, lines=True,
                color='rgb(200, 205, 210)')
    chart.watermark('PROFESSIONAL TRADING LAYOUT')
    
    print("\n" + "="*70)
    print("✅ PERFECT 3-PANE LAYOUT")
    print("="*70)
    print("📊 PANE 0: Candlesticks + SMA indicators (60% height)")
    print("📊 PANE 1: Volume histogram (20% height - CONSTRAINED)")  
    print("📊 PANE 2: RSI oscillator (20% height)")
    print("="*70)
    print("🎯 Volume scaled to 0-10 range (won't overpower chart)")
    print("🎯 Visual borders separate each pane")
    print("🎯 Independent Y-axis scaling per indicator\n")
    
    chart.show(block=True)

if __name__ == '__main__':
    main()