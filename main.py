import pandas as pd
from lightweight_charts import Chart


def main():
    path = r"C:\Users\jegge\Desktop\best_data_futures\nq_intraday\nq_combined_minute_data.csv"

    # 1. Load & normalize columns
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower()

    # Ensure datetime and rename to 'time'
    df['date'] = pd.to_datetime(df['date'])
    df = df.rename(columns={'date': 'time'})

    # Keep only the columns we care about (adjust names if your CSV differs)
    df = df[['time', 'open', 'high', 'low', 'close', 'volume']]

    # 2. Set DatetimeIndex for resampling
    df = df.set_index('time')

    agg = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }

    # 3. Resample and bring 'time' back as a column
    df_1 = df.reset_index()  # original 1-min with 'time' column
    df_2 = (
        df.resample('2min', origin='start_day', offset='-7h')
          .agg(agg)
          .dropna()
          .reset_index()      # gives 'time' column back
    )
    df_60 = (
        df.resample('1h', origin='start_day', offset='-7h')
          .agg(agg)
          .dropna()
          .reset_index()
    )
    df_4h = (
        df.resample('4h', origin='start_day', offset='-7h')
          .agg(agg)
          .dropna()
          .reset_index()
    )

    # 4. Take last 250 rows from each (still with 'time' column)
    filt    = df_1.iloc[-250:]
    filt_2  = df_2.iloc[-250:]
    filt_60 = df_60.iloc[-250:]
    filt_4h = df_4h.iloc[-250:]

    # 5. Build chart layout
    chart = Chart(width=1920, height=1080, title="NQ Intraday Data", toolbox=True)
    charts = chart.create_layout('main_right_3', toolbox=True)
    
    main_chart = charts[0]
    ind1, ind2, ind3 = charts[1], charts[2], charts[3]

    # 6. Set data on each pane
    main_chart.set(filt)
    main_chart.watermark("MAIN (1m)")

    ind1.set(filt_2)
    ind1.watermark("2min")

    ind2.set(filt_60)
    ind2.watermark("1h")

    ind3.set(filt_4h)
    ind3.watermark("4h")

    chart.show(block=True)


if __name__ == '__main__':
    main()
