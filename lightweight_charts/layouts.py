"""Layout presets for easy chart grid creation"""
from typing import List, Tuple
import pandas as pd
from .grid_manager import GridLayoutManager


class LayoutPreset:
    """Predefined chart layouts using GridLayoutManager"""
    
    @staticmethod
    def single_with_indicators(chart, num_indicators=3):
        """
        Create 1 main chart + N indicator subcharts below
        
        Args:
            chart: Main Chart object
            num_indicators: Number of indicator panes below (1-4)
            
        Returns:
            List of subchart objects [sub1, sub2, ...]
        """
        if num_indicators < 1 or num_indicators > 4:
            raise ValueError("num_indicators must be between 1 and 4")
        
        # Calculate heights
        main_height = 0.6
        indicator_height = 0.4 / num_indicators
        
        # Main chart adjusts its height
        chart.resize(width=1.0, height=main_height)
        
        # Create indicator subcharts
        subcharts = []
        prev_chart = chart
        
        for i in range(num_indicators):
            # Calculate remaining space height
            remaining = 1.0 / (num_indicators - i)
            
            sub = prev_chart.create_subchart(
                position='bottom',
                width=1.0,
                height=remaining if i == 0 else remaining,
                sync_crosshairs_only=True
            )
            subcharts.append(sub)
            prev_chart = sub
        
        return subcharts
    
    @staticmethod
    def two_column(chart):
        """
        Create 2-column layout (50/50 split)
        
        Args:
            chart: Main Chart object
            
        Returns:
            Right pane subchart
        """
        chart.resize(width=0.5, height=1.0)
        
        right = chart.create_subchart(
            position='right',
            width=0.5,
            height=1.0,
            sync_crosshairs_only=False
        )
        
        return right
    
    @staticmethod
    def three_column(chart):
        """
        Create 3-column layout (33/33/33 split)
        
        Args:
            chart: Main Chart object
            
        Returns:
            Tuple of (middle, right) subcharts
        """
        chart.resize(width=0.33, height=1.0)
        
        middle = chart.create_subchart(
            position='right',
            width=0.33,
            height=1.0,
            sync_crosshairs_only=False
        )
        
        right = middle.create_subchart(
            position='right',
            width=0.34,  # Slightly larger to account for rounding
            height=1.0,
            sync_crosshairs_only=False
        )
        
        return middle, right
    
    @staticmethod
    def grid_2x2(chart):
        """
        Create 2x2 grid layout using GridLayoutManager
        
        Args:
            chart: Main Chart object
            
        Returns:
            Tuple of (top_right, bottom_left, bottom_right)
        """
        return GridLayoutManager.create_2x2(chart)
    
    @staticmethod
    def grid_3x3(chart):
        """
        Create 3x3 grid layout using GridLayoutManager
        
        Args:
            chart: Main Chart object
            
        Returns:
            List of 8 subchart objects (9 total including main)
        """
        return GridLayoutManager.create_3x3(chart)
    
    @staticmethod
    def grid_1x4_vertical(chart):
        """
        Create 4 charts stacked vertically
        
        Args:
            chart: Main Chart object
            
        Returns:
            Tuple of (chart2, chart3, chart4)
        """
        return GridLayoutManager.create_1x4_vertical(chart)