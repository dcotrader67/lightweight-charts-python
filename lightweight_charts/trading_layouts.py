"""
Easy-to-use multi-pane trading layouts
Provides high-level abstractions for common chart configurations
"""
import pandas as pd
from typing import Optional, Dict, List, Tuple
import numpy as np

class TradingLayout:
    """
    Simplified multi-pane chart creator for common trading layouts
    Uses subcharts under the hood for true pane separation
    """
    
    @staticmethod
    def create_standard(
        df: pd.DataFrame,
        indicators: Optional[Dict[str, pd.DataFrame]] = None,
        width: int = 1920,
        height: int = 1080,
        volume_pane: bool = True,
        volume_color: str = 'rgba(100, 130, 180, 0.6)',
        sync_crosshairs: bool = True,
        show_legend: bool = True,
        watermark: Optional[str] = None
    ) -> Tuple:
        """
        Create a standard multi-pane trading layout with TRUE separate panes
        
        Layout structure:
        - Main pane (60%): Candlesticks + overlays
        - Volume pane (optional, 15%): Volume histogram  
        - Indicator panes (25% / num_indicators): RSI, MACD, etc.
        
        Args:
            df: OHLC DataFrame with columns: time, open, high, low, close
                Optional: volume (if volume_pane=True)
            indicators: Dict of {name: DataFrame} for indicator panes
                       Each DataFrame must have 'time' and indicator name as columns
            width: Chart width in pixels
            height: Chart height in pixels
            volume_pane: Create separate pane for volume
            volume_color: Color for volume histogram
            sync_crosshairs: Synchronize crosshairs across panes
            show_legend: Show legend on main chart
            watermark: Optional watermark text
            
        Returns:
            (main_chart, list_of_subcharts)
            
        Example:
            >>> from lightweight_charts.trading_layouts import TradingLayout, IndicatorBuilder
            >>> 
            >>> df = pd.DataFrame({...})  # Your OHLC data
            >>> rsi_data = IndicatorBuilder.rsi(df)
            >>> 
            >>> chart, subcharts = TradingLayout.create_standard(
            ...     df,
            ...     indicators={'RSI': rsi_data},
            ...     volume_pane=True
            ... )
            >>> chart.show(block=True)
        """
        from lightweight_charts import Chart
        
        # Calculate pane heights
        num_indicators = len(indicators) if indicators else 0
        has_volume = volume_pane and 'volume' in df.columns
        
        main_height = 0.60
        remaining = 0.40
        
        if has_volume:
            volume_height = 0.15
            remaining -= volume_height
        
        indicator_height = remaining / max(num_indicators, 1) if num_indicators > 0 else 0
        
        # Create main chart
        chart = Chart(width=width, height=height, inner_height=main_height)
        
        # Remove volume from df if it exists (we'll add it separately)
        df_no_vol = df.drop(columns=['volume']) if 'volume' in df.columns else df
        chart.set(df_no_vol)
        
        # Configure main chart styling
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
        
        chart.crosshair(
            mode='normal',
            vert_visible=True,
            vert_color='rgba(150, 150, 150, 0.5)',
            vert_style='dashed',
            horz_visible=True,
            horz_color='rgba(150, 150, 150, 0.5)',
            horz_style='dashed'
        )
        
        if show_legend:
            chart.legend(visible=True, ohlc=True, percent=True, lines=True)
        
        if watermark:
            chart.watermark(watermark)
        
        subcharts = []
        
        # Add volume subchart (TRULY SEPARATE WINDOW)
        if has_volume:
            vol_chart = chart.create_subchart(
                position='bottom',
                width=1.0,
                height=volume_height,
                sync_crosshairs_only=sync_crosshairs
            )
            
            vol_line = vol_chart.create_line('Volume', color=volume_color, width=1)
            vol_data = df[['time', 'volume']].rename(columns={'volume': 'Volume'})
            vol_line.set(vol_data)
            
            vol_chart.legend(visible=True, lines=True)
            vol_chart.layout(background_color='#0C0D0F')
            subcharts.append(vol_chart)
        
        # Add indicator subcharts (TRULY SEPARATE WINDOWS)
        if indicators:
            for ind_name, ind_data in indicators.items():
                subchart = chart.create_subchart(
                    position='bottom',
                    width=1.0,
                    height=indicator_height,
                    sync_crosshairs_only=sync_crosshairs
                )
                
                # Determine color based on indicator name
                color = TradingLayout._get_indicator_color(ind_name)
                
                line = subchart.create_line(ind_name, color=color, width=2)
                line.set(ind_data)
                
                # Add reference lines for known indicators
                TradingLayout._add_reference_lines(subchart, ind_name, ind_data)
                
                subchart.legend(visible=True, lines=True)
                subchart.layout(background_color='#0C0D0F')
                subcharts.append(subchart)
        
        return chart, subcharts
    
    @staticmethod
    def create_with_overlays(
        df: pd.DataFrame,
        overlays: Optional[Dict[str, pd.DataFrame]] = None,
        indicators: Optional[Dict[str, pd.DataFrame]] = None,
        width: int = 1920,
        height: int = 1080,
        **kwargs
    ) -> Tuple:
        """
        Create layout with overlay indicators (SMAs, Bollinger Bands) on main chart
        
        Args:
            df: OHLC DataFrame
            overlays: Dict of {name: DataFrame} for lines on main chart
                     Example: {'SMA 20': sma20_df, 'SMA 50': sma50_df}
            indicators: Dict of {name: DataFrame} for separate panes
            width: Chart width
            height: Chart height
            **kwargs: Additional arguments passed to create_standard()
            
        Returns:
            (main_chart, list_of_subcharts)
            
        Example:
            >>> sma20 = IndicatorBuilder.sma(df, 20)
            >>> sma50 = IndicatorBuilder.sma(df, 50)
            >>> rsi = IndicatorBuilder.rsi(df)
            >>> 
            >>> chart, subcharts = TradingLayout.create_with_overlays(
            ...     df,
            ...     overlays={'SMA 20': sma20, 'SMA 50': sma50},
            ...     indicators={'RSI': rsi}
            ... )
        """
        # Create standard layout
        chart, subcharts = TradingLayout.create_standard(
            df, indicators, width, height, **kwargs
        )
        
        # Add overlay lines to main chart
        if overlays:
            for i, (overlay_name, overlay_data) in enumerate(overlays.items()):
                color = TradingLayout._get_overlay_color(overlay_name, i)
                line = chart.create_line(overlay_name, color=color, width=2)
                line.set(overlay_data)
        
        return chart, subcharts
    
    @staticmethod
    def create_grid_2x2(
        width: int = 1920,
        height: int = 1080,
        sync_crosshairs: bool = True,
        title: str = ''
    ) -> Tuple:
        """
        Create a 2x2 grid layout with 4 synchronized charts.
        
        Perfect for:
        - Multi-timeframe analysis
        - Comparing multiple symbols
        - Technical analysis dashboards
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
            sync_crosshairs: Synchronize crosshairs across all charts
            title: Window title
            
        Returns:
            (main_chart, top_left, top_right, bottom_left, bottom_right)
            
        Example:
            >>> from lightweight_charts.trading_layouts import TradingLayout
            >>> 
            >>> # Create grid
            >>> main, tl, tr, bl, br = TradingLayout.create_grid_2x2(
            ...     width=1920, 
            ...     height=1080,
            ...     sync_crosshairs=True,
            ...     title="Multi-Timeframe Analysis"
            ... )
            >>> 
            >>> # Set data for each chart
            >>> tl.set(df_1h)
            >>> tl.watermark('1H')
            >>> 
            >>> tr.set(df_4h)
            >>> tr.watermark('4H')
            >>> 
            >>> bl.set(df_1d)
            >>> bl.watermark('1D')
            >>> 
            >>> br.set(df_1w)
            >>> br.watermark('1W')
            >>> 
            >>> # Show the grid
            >>> main.show(block=True)
        """
        from lightweight_charts import Chart
        
        # Create main container chart
        chart = Chart(width=width, height=height, title=title)
        
        # Create 2x2 grid
        tl, tr, bl, br = chart.create_grid_2x2(
            sync_id=chart.id if sync_crosshairs else None,
            sync_crosshairs_only=True
        )
        
        # Apply consistent styling to all charts
        for c in [tl, tr, bl, br]:
            c.layout(
                background_color='#0C0D0F',
                text_color='#D8D9DB',
                font_size=11
            )
            
            c.grid(
                vert_enabled=True,
                horz_enabled=True,
                color='rgba(42, 46, 57, 0.5)',
                style='solid'
            )
            
            c.crosshair(
                mode='normal',
                vert_visible=True,
                vert_color='rgba(150, 150, 150, 0.5)',
                vert_style='dashed',
                horz_visible=True,
                horz_color='rgba(150, 150, 150, 0.5)',
                horz_style='dashed'
            )
            
            c.legend(visible=True, ohlc=True, percent=True, lines=True)
        
        return chart, tl, tr, bl, br
    
    @staticmethod
    def _get_indicator_color(name: str) -> str:
        """Get appropriate color based on indicator name"""
        name_lower = name.lower()
        
        color_map = {
            'rsi': 'rgba(156, 39, 176, 1.0)',
            'macd': 'rgba(33, 150, 243, 1.0)',
            'stoch': 'rgba(255, 152, 0, 1.0)',
            'cci': 'rgba(76, 175, 80, 1.0)',
            'momentum': 'rgba(244, 67, 54, 1.0)',
            'volume': 'rgba(100, 130, 180, 0.6)',
        }
        
        for key, color in color_map.items():
            if key in name_lower:
                return color
        
        return 'rgba(156, 39, 176, 0.9)'
    
    @staticmethod
    def _get_overlay_color(name: str, index: int) -> str:
        """Get color for overlay indicators"""
        name_lower = name.lower()
        
        # Special colors for specific indicators
        if 'vwap' in name_lower:
            if 'upper' in name_lower:
                return 'rgba(255, 82, 82, 0.4)'  # Red for upper band
            elif 'lower' in name_lower:
                return 'rgba(76, 175, 80, 0.4)'  # Green for lower band
            else:
                return 'rgba(255, 193, 7, 0.9)'  # Yellow for VWAP
        
        colors = [
            'rgba(255, 193, 7, 0.9)',   # Yellow
            'rgba(33, 150, 243, 0.9)',  # Blue  
            'rgba(76, 175, 80, 0.9)',   # Green
            'rgba(244, 67, 54, 0.9)',   # Red
            'rgba(156, 39, 176, 0.9)',  # Purple
            'rgba(255, 152, 0, 0.9)',   # Orange
        ]
        return colors[index % len(colors)]
    
    @staticmethod
    def _add_reference_lines(chart, indicator_name: str, data: pd.DataFrame):
        """Add reference lines for known indicators"""
        name_lower = indicator_name.lower()
        
        # RSI reference lines
        if 'rsi' in name_lower:
            for level, color in [(70, 'rgba(255, 82, 82, 0.3)'), 
                                 (50, 'rgba(128, 128, 128, 0.2)'),
                                 (30, 'rgba(76, 175, 80, 0.3)')]:
                ref_line = chart.create_line('', color=color, width=1, style='dashed')
                ref_data = data[['time']].copy()
                ref_data['value'] = level
                ref_line.set(ref_data)
                ref_line.price_line(label_visible=False, line_visible=False)
        
        # Stochastic reference lines
        elif 'stoch' in name_lower:
            for level, color in [(80, 'rgba(255, 82, 82, 0.3)'),
                                 (20, 'rgba(76, 175, 80, 0.3)')]:
                ref_line = chart.create_line('', color=color, width=1, style='dashed')
                ref_data = data[['time']].copy()
                ref_data['value'] = level
                ref_line.set(ref_data)
                ref_line.price_line(label_visible=False, line_visible=False)
        
        # MACD zero line
        elif 'macd' in name_lower:
            zero_line = chart.create_line('', color='rgba(128, 128, 128, 0.3)', width=1)
            zero_data = data[['time']].copy()
            zero_data['value'] = 0
            zero_line.set(zero_data)
            zero_line.price_line(label_visible=False, line_visible=False)


class IndicatorBuilder:
    """Helper methods to calculate common technical indicators"""
    
    @staticmethod
    def sma(df: pd.DataFrame, period: int, column: str = 'close') -> pd.DataFrame:
        """Simple Moving Average"""
        result = df[['time']].copy()
        result[f'SMA {period}'] = df[column].rolling(window=period).mean()
        return result
    
    @staticmethod
    def ema(df: pd.DataFrame, period: int, column: str = 'close') -> pd.DataFrame:
        """Exponential Moving Average"""
        result = df[['time']].copy()
        result[f'EMA {period}'] = df[column].ewm(span=period, adjust=False).mean()
        return result
    
    @staticmethod
    def rsi(df: pd.DataFrame, period: int = 14, column: str = 'close') -> pd.DataFrame:
        """Relative Strength Index"""
        delta = df[column].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        result = df[['time']].copy()
        result['RSI'] = rsi.fillna(50)
        return result
    
    @staticmethod
    def macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, 
             signal: int = 9, column: str = 'close') -> pd.DataFrame:
        """MACD Indicator"""
        exp1 = df[column].ewm(span=fast, adjust=False).mean()
        exp2 = df[column].ewm(span=slow, adjust=False).mean()
        macd_line = exp1 - exp2
        
        result = df[['time']].copy()
        result['MACD'] = macd_line
        return result
    
    @staticmethod
    def bollinger_bands(df: pd.DataFrame, period: int = 20, 
                       std_dev: float = 2.0, column: str = 'close') -> Dict[str, pd.DataFrame]:
        """Bollinger Bands - returns dict of upper, middle, lower"""
        sma = df[column].rolling(window=period).mean()
        std = df[column].rolling(window=period).std()
        
        upper = df[['time']].copy()
        upper['BB Upper'] = sma + (std * std_dev)
        
        middle = df[['time']].copy()
        middle['BB Middle'] = sma
        
        lower = df[['time']].copy()
        lower['BB Lower'] = sma - (std * std_dev)
        
        return {
            'BB Upper': upper,
            'BB Middle': middle,
            'BB Lower': lower
        }
    
    @staticmethod
    def vwap(
        df: pd.DataFrame, 
        anchor_datetime: Optional[str] = None,
        anchor_price: Optional[float] = None,
        session_open: str = '09:30:00'
    ) -> pd.DataFrame:
        """
        Volume Weighted Average Price (VWAP)
        
        Standard VWAP calculation: sum(price * volume) / sum(volume)
        where price = (high + low + close) / 3
        
        Args:
            df: DataFrame with columns: time, high, low, close, volume
            anchor_datetime: Optional anchor datetime (YYYY-MM-DD HH:MM:SS or YYYY-MM-DD)
                            If time not specified, defaults to session_open
                            If None, calculates from beginning of data
            anchor_price: Optional price anchor for intraday VWAP
                        Can be 'open', 'high', 'low', 'close', or specific float
            session_open: Default session open time if time not specified (HH:MM:SS)
                        Default is '09:30:00' (US market open)
                            
        Returns:
            DataFrame with time and VWAP columns
            
        Example:
            >>> # Rolling VWAP from start
            >>> vwap = IndicatorBuilder.vwap(df)
            >>> 
            >>> # Anchored VWAP from date (uses session open time)
            >>> vwap = IndicatorBuilder.vwap(df, anchor_datetime='2024-06-01')
            >>> 
            >>> # Anchored VWAP from specific datetime
            >>> vwap = IndicatorBuilder.vwap(df, anchor_datetime='2024-06-01 14:30:00')
            >>> 
            >>> # Anchored VWAP at high of specific candle
            >>> vwap = IndicatorBuilder.vwap(df, anchor_datetime='2024-06-01 10:00:00', anchor_price='high')
        """
        if 'volume' not in df.columns:
            raise ValueError("DataFrame must contain 'volume' column for VWAP calculation")
        
        # Calculate typical price (default price calculation)
        typical_price = (df['high'] + df['low'] + df['close']) / 3
        
        # Find anchor index
        if anchor_datetime is not None:
            # Parse the datetime
            anchor_dt = pd.to_datetime(anchor_datetime)
            
            # If no time component provided, add session open time
            if anchor_dt.hour == 0 and anchor_dt.minute == 0 and anchor_dt.second == 0:
                # Check if original string had time component
                if ':' not in str(anchor_datetime):
                    # No time provided, use session open
                    time_parts = session_open.split(':')
                    anchor_dt = anchor_dt.replace(
                        hour=int(time_parts[0]),
                        minute=int(time_parts[1]) if len(time_parts) > 1 else 0,
                        second=int(time_parts[2]) if len(time_parts) > 2 else 0
                    )
            
            # Find the closest timestamp >= anchor
            anchor_idx = df[df['time'] >= anchor_dt].index[0] if any(df['time'] >= anchor_dt) else 0
            
            # If exact match not found, find nearest
            if anchor_idx == 0 and len(df) > 0:
                time_diffs = abs(df['time'] - anchor_dt)
                anchor_idx = time_diffs.idxmin()
        else:
            anchor_idx = 0
        
        # Handle price anchor
        anchor_price_value = None
        if anchor_price is not None and anchor_idx < len(df):
            if isinstance(anchor_price, str):
                # Use OHLC value
                price_col = anchor_price.lower()
                if price_col in ['open', 'high', 'low', 'close']:
                    anchor_price_value = df.iloc[anchor_idx][price_col]
                else:
                    raise ValueError(f"Invalid anchor_price: {anchor_price}. Use 'open', 'high', 'low', 'close', or float")
            else:
                # Use specific price value
                anchor_price_value = float(anchor_price)
        
        # Calculate VWAP from anchor point
        vwap_values = []
        for i in range(len(df)):
            if i < anchor_idx:
                vwap_values.append(np.nan)
            else:
                # Calculate cumulative values from anchor
                subset = df.iloc[anchor_idx:i+1]
                tp_subset = typical_price.iloc[anchor_idx:i+1]
                
                cum_tp_volume = (tp_subset * subset['volume']).sum()
                cum_volume = subset['volume'].sum()
                
                if cum_volume > 0:
                    vwap_val = cum_tp_volume / cum_volume
                    
                    # Adjust for price anchor if specified
                    if anchor_price_value is not None and i == anchor_idx:
                        # For the anchor bar, use the specified price
                        vwap_val = anchor_price_value
                    
                    vwap_values.append(vwap_val)
                else:
                    vwap_values.append(np.nan)
        
        result = df[['time']].copy()
        
        # Create descriptive column name
        if anchor_datetime:
            anchor_dt_parsed = pd.to_datetime(anchor_datetime)
            
            # Format based on whether time is significant
            if anchor_dt_parsed.hour == 0 and anchor_dt_parsed.minute == 0:
                anchor_str = anchor_dt_parsed.strftime('%Y-%m-%d')
            else:
                anchor_str = anchor_dt_parsed.strftime('%Y-%m-%d %H:%M')
            
            col_name = f'VWAP ({anchor_str}'
            
            if anchor_price:
                col_name += f' @ {anchor_price}' if isinstance(anchor_price, str) else f' @ ${anchor_price:.2f}'
            col_name += ')'
            
            result[col_name] = vwap_values
        else:
            result['VWAP'] = vwap_values
        
        return result

    @staticmethod
    def anchored_vwap(
        df: pd.DataFrame, 
        anchor_datetime: str,
        anchor_price: Optional[str] = None,
        session_open: str = '09:30:00'
    ) -> pd.DataFrame:
        """
        Anchored VWAP - VWAP calculation from a specific datetime and/or price
        
        Commonly anchored to:
        - Earnings dates (with session open time)
        - Significant news events (with specific time)
        - Market opens (specific time)
        - Swing highs/lows (with specific price)
        - Key levels breaks (specific price and time)
        
        Args:
            df: DataFrame with OHLCV data
            anchor_datetime: Date/time to anchor from
                            Formats: 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'
                            If time omitted, uses session_open time
            anchor_price: Optional price anchor point
                        'open', 'high', 'low', 'close', or specific float value
                        Useful for anchoring to specific candle features
            session_open: Default session open time (default: '09:30:00' for US)
            
        Returns:
            DataFrame with time and Anchored VWAP
            
        Example:
            >>> # Anchor to earnings date (uses session open)
            >>> vwap1 = IndicatorBuilder.anchored_vwap(df, '2024-05-15')
            >>> 
            >>> # Anchor to specific time (Fed announcement)
            >>> vwap2 = IndicatorBuilder.anchored_vwap(df, '2024-03-20 14:00:00')
            >>> 
            >>> # Anchor to swing high
            >>> vwap3 = IndicatorBuilder.anchored_vwap(
            ...     df, 
            ...     '2024-06-01 10:30:00', 
            ...     anchor_price='high'
            ... )
            >>> 
            >>> # Anchor to specific price level
            >>> vwap4 = IndicatorBuilder.anchored_vwap(
            ...     df,
            ...     '2024-04-15 09:30:00',
            ...     anchor_price=150.50
            ... )
        """
        return IndicatorBuilder.vwap(
            df, 
            anchor_datetime=anchor_datetime,
            anchor_price=anchor_price,
            session_open=session_open
        )

    @staticmethod
    def multiple_anchored_vwaps(
        df: pd.DataFrame, 
        anchors: List[dict],
        session_open: str = '09:30:00'
    ) -> Dict[str, pd.DataFrame]:
        """
        Calculate multiple anchored VWAPs at once
        
        Args:
            df: DataFrame with OHLCV data
            anchors: List of anchor dicts, each containing:
                    - 'datetime': anchor datetime (required)
                    - 'price': anchor price (optional) - 'open'/'high'/'low'/'close' or float
                    - 'label': custom label (optional)
            session_open: Default session open time
            
        Returns:
            Dict of {label: vwap_dataframe}
            
        Example:
            >>> anchors = [
            ...     {'datetime': '2024-03-01', 'price': 'high', 'label': 'Q1 High'},
            ...     {'datetime': '2024-04-15 14:00:00', 'label': 'Fed Meeting'},
            ...     {'datetime': '2024-06-01', 'price': 150.50, 'label': 'Key Level'},
            ... ]
            >>> vwaps = IndicatorBuilder.multiple_anchored_vwaps(df, anchors)
            >>> 
            >>> # Use in layout
            >>> chart, subs = TradingLayout.create_with_overlays(
            ...     df,
            ...     overlays=vwaps
            ... )
        """
        result = {}
        
        for anchor in anchors:
            datetime = anchor.get('datetime')
            price = anchor.get('price', None)
            label = anchor.get('label', None)
            
            if not datetime:
                raise ValueError("Each anchor must have a 'datetime' key")
            
            vwap_df = IndicatorBuilder.anchored_vwap(
                df, 
                datetime, 
                anchor_price=price,
                session_open=session_open
            )
            
            # Get the column name
            col_name = [c for c in vwap_df.columns if c != 'time'][0]
            
            # Use custom label if provided
            if label:
                vwap_df_renamed = vwap_df.copy()
                vwap_df_renamed.rename(columns={col_name: label}, inplace=True)
                result[label] = vwap_df_renamed
            else:
                result[col_name] = vwap_df
        
        return result

    @staticmethod
    def vwap_bands(
        df: pd.DataFrame, 
        anchor_datetime: Optional[str] = None,
        anchor_price: Optional[str] = None,
        num_std: float = 1.0,
        session_open: str = '09:30:00'
    ) -> Dict[str, pd.DataFrame]:
        """
        VWAP with standard deviation bands
        
        Args:
            df: DataFrame with OHLCV data
            anchor_datetime: Optional anchor datetime
            anchor_price: Optional price anchor
            num_std: Number of standard deviations for bands (default 1.0)
            session_open: Default session open time
            
        Returns:
            Dict with 'VWAP...', 'VWAP Upper', 'VWAP Lower'
        """
        if 'volume' not in df.columns:
            raise ValueError("DataFrame must contain 'volume' column")
        
        # Calculate typical price and VWAP
        typical_price = (df['high'] + df['low'] + df['close']) / 3
        vwap_df = IndicatorBuilder.vwap(
            df, 
            anchor_datetime=anchor_datetime,
            anchor_price=anchor_price,
            session_open=session_open
        )
        vwap_col = [c for c in vwap_df.columns if c != 'time'][0]
        vwap_values = vwap_df[vwap_col].values
        
        # Find anchor index
        if anchor_datetime is not None:
            anchor_dt = pd.to_datetime(anchor_datetime)
            if anchor_dt.hour == 0 and anchor_dt.minute == 0 and ':' not in str(anchor_datetime):
                time_parts = session_open.split(':')
                anchor_dt = anchor_dt.replace(
                    hour=int(time_parts[0]),
                    minute=int(time_parts[1]) if len(time_parts) > 1 else 0
                )
            anchor_idx = df[df['time'] >= anchor_dt].index[0] if any(df['time'] >= anchor_dt) else 0
        else:
            anchor_idx = 0
        
        # Calculate standard deviation
        std_values = []
        for i in range(len(df)):
            if i < anchor_idx or pd.isna(vwap_values[i]):
                std_values.append(np.nan)
            else:
                subset = typical_price.iloc[anchor_idx:i+1]
                variance = ((subset - vwap_values[i]) ** 2).mean()
                std_values.append(np.sqrt(variance))
        
        std_series = pd.Series(std_values)
        
        # Create bands
        upper = df[['time']].copy()
        upper[f'{vwap_col} Upper'] = vwap_values + (num_std * std_series)
        
        middle = vwap_df.copy()
        
        lower = df[['time']].copy()
        lower[f'{vwap_col} Lower'] = vwap_values - (num_std * std_series)
        
        return {
            vwap_col: middle,
            f'{vwap_col} Upper': upper,
            f'{vwap_col} Lower': lower
        }