"""Data validation for chart inputs"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class ValidationError(ValueError):
    """Raised when data validation fails"""
    pass


class OHLCValidator:
    """Validator for OHLC/candlestick data"""
    
    REQUIRED_COLUMNS = ['time', 'open', 'high', 'low', 'close']
    
    @classmethod
    def validate(cls, df: pd.DataFrame, fix_issues: bool = True) -> pd.DataFrame:
        """
        Validate OHLC DataFrame.
        
        Args:
            df: DataFrame to validate
            fix_issues: Attempt to fix common issues automatically
            
        Returns:
            Validated (and possibly corrected) DataFrame
            
        Raises:
            ValidationError: If validation fails
        """
        if df is None or df.empty:
            raise ValidationError("DataFrame is empty")
        
        # Check required columns
        df = cls._check_columns(df, fix_issues)
        
        # Validate data types
        df = cls._validate_types(df, fix_issues)
        
        # Validate OHLC relationships
        df = cls._validate_ohlc_rules(df, fix_issues)
        
        # Check for data quality issues
        df = cls._check_data_quality(df, fix_issues)
        
        # Sort by time
        df = df.sort_values('time').reset_index(drop=True)
        
        return df
    
    @classmethod
    def _check_columns(cls, df: pd.DataFrame, fix: bool) -> pd.DataFrame:
        """Check for required columns"""
        df = df.copy()
        
        # Case-insensitive column mapping
        column_map = {}
        for col in df.columns:
            lower = col.lower().strip()
            if lower in ['date', 'datetime', 'timestamp']:
                column_map[col] = 'time'
            elif lower in cls.REQUIRED_COLUMNS:
                column_map[col] = lower
        
        if column_map:
            df = df.rename(columns=column_map)
            logger.info(f"Renamed columns: {column_map}")
        
        # Check for missing required columns
        missing = set(cls.REQUIRED_COLUMNS) - set(df.columns)
        if missing:
            raise ValidationError(
                f"Missing required columns: {missing}. "
                f"Available columns: {list(df.columns)}"
            )
        
        return df
    
    @staticmethod
    def _validate_types(df: pd.DataFrame, fix: bool) -> pd.DataFrame:
        """Validate and fix data types"""
        df = df.copy()
        
        # Time column
        if not pd.api.types.is_datetime64_any_dtype(df['time']):
            if fix:
                df['time'] = pd.to_datetime(df['time'])
                logger.info("Converted 'time' column to datetime")
            else:
                raise ValidationError("'time' column must be datetime type")
        
        # Numeric columns
        for col in ['open', 'high', 'low', 'close']:
            if not pd.api.types.is_numeric_dtype(df[col]):
                if fix:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    logger.info(f"Converted '{col}' to numeric")
                else:
                    raise ValidationError(f"'{col}' must be numeric type")
        
        return df
    
    @staticmethod
    def _validate_ohlc_rules(df: pd.DataFrame, fix: bool) -> pd.DataFrame:
        """Validate OHLC relationships (high >= low, etc.)"""
        df = df.copy()
        
        # Check high >= low
        invalid_hl = df['high'] < df['low']
        if invalid_hl.any():
            count = invalid_hl.sum()
            if fix:
                # Swap high and low
                df.loc[invalid_hl, ['high', 'low']] = df.loc[
                    invalid_hl, ['low', 'high']
                ].values
                logger.warning(f"Fixed {count} bars where high < low (swapped values)")
            else:
                raise ValidationError(
                    f"{count} bars have high < low at rows: "
                    f"{df[invalid_hl].index.tolist()[:5]}"
                )
        
        # Check high >= open, close
        invalid_h = (df['high'] < df['open']) | (df['high'] < df['close'])
        if invalid_h.any():
            count = invalid_h.sum()
            if fix:
                df.loc[invalid_h, 'high'] = df.loc[
                    invalid_h, ['open', 'high', 'low', 'close']
                ].max(axis=1)
                logger.warning(f"Fixed {count} bars where high < open/close")
            else:
                raise ValidationError(f"{count} bars have invalid high values")
        
        # Check low <= open, close
        invalid_l = (df['low'] > df['open']) | (df['low'] > df['close'])
        if invalid_l.any():
            count = invalid_l.sum()
            if fix:
                df.loc[invalid_l, 'low'] = df.loc[
                    invalid_l, ['open', 'high', 'low', 'close']
                ].min(axis=1)
                logger.warning(f"Fixed {count} bars where low > open/close")
            else:
                raise ValidationError(f"{count} bars have invalid low values")
        
        return df
    
    @staticmethod
    def _check_data_quality(df: pd.DataFrame, fix: bool) -> pd.DataFrame:
        """Check for NaN and other quality issues"""
        df = df.copy()
        
        # Check for NaN values
        required_cols = ['time', 'open', 'high', 'low', 'close']
        nan_counts = df[required_cols].isna().sum()
        if nan_counts.any():
            if fix:
                df = df.ffill().bfill()
                logger.warning(f"Filled NaN values: {nan_counts.to_dict()}")
            else:
                raise ValidationError(
                    f"DataFrame contains NaN values: {nan_counts.to_dict()}"
                )
        
        return df