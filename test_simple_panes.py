import pandas as pd
import numpy as np
from lightweight_charts import Chart

def main():
    # Very simple test
    df = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=50),
        'open': 100 + np.random.randn(50),
        'high': 102 + np.random.randn(50),
        'low': 98 + np.random.randn(50),
        'close': 100 + np.random.randn(50),
        'volume': np.random.randint(1000000, 5000000, 50)
    })

    chart = Chart(width=1800, height=1000)
    chart.set(df)

    # Add line to pane 1
    line1 = chart.create_line('Test Line 1', color='red', pane_index=1)
    line1_data = df[['time']].copy()
    line1_data['Test Line 1'] = 50 + np.random.randn(len(df)) * 10
    line1.set(line1_data)

    # Add line to pane 2
    line2 = chart.create_line('Test Line 2', color='green', pane_index=2)
    line2_data = df[['time']].copy()
    line2_data['Test Line 2'] = np.random.randn(len(df)) * 5
    line2.set(line2_data)

    print("Chart should show 3 panes:")
    print("  Pane 0: Candlesticks + Volume")
    print("  Pane 1: Red line")
    print("  Pane 2: Green line")

    chart.show(block=True)

if __name__ == '__main__':
    main()