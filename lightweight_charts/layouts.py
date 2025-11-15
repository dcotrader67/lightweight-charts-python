"""Layout presets for easy chart grid creation"""
from typing import List, Tuple
import pandas as pd


class LayoutPreset:
    """Predefined chart layouts"""
    
    @staticmethod
    def single_with_indicators(chart, num_indicators=3):
        """
        Create 1 main chart + N indicator subcharts below
        
        Args:
            chart: Main Chart object
            num_indicators: Number of indicator panes below (1-4)
            
        Returns:
            List of subchart objects [main_chart, sub1, sub2, ...]
        """
        if num_indicators < 1 or num_indicators > 4:
            raise ValueError("num_indicators must be between 1 and 4")
        
        # Calculate heights
        main_height = 0.6
        indicator_height = 0.4 / num_indicators
        
        # Main chart is already created, adjust its height
        chart.resize(width=1.0, height=main_height)
        
        # Create indicator subcharts
        subcharts = []
        for i in range(num_indicators):
            sub = chart.create_subchart(
                position='bottom',
                width=1.0,
                height=indicator_height
            )
            subcharts.append(sub)
        
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
            height=1.0
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
            height=1.0
        )
        
        right = chart.create_subchart(
            position='right',
            width=0.34,  # Slightly larger to account for rounding
            height=1.0
        )
        
        return middle, right
    
    @staticmethod
    def four_column(chart):
        """
        Create 4-column layout (25/25/25/25 split)
        
        Args:
            chart: Main Chart object
            
        Returns:
            Tuple of (col2, col3, col4) subcharts
        """
        chart.resize(width=0.25, height=1.0)
        
        col2 = chart.create_subchart(position='right', width=0.25, height=1.0)
        col3 = chart.create_subchart(position='right', width=0.25, height=1.0)
        col4 = chart.create_subchart(position='right', width=0.25, height=1.0)
        
        return col2, col3, col4
    
    @staticmethod
    def grid_2x2(chart):
        """
        Create 2x2 grid layout
        
        Args:
            chart: Main Chart object
            
        Returns:
            Tuple of (top_right, bottom_left, bottom_right)
        """
        # Top-left (main chart)
        chart.resize(width=0.5, height=0.5)
        
        # Top-right
        top_right = chart.create_subchart(
            position='right',
            width=0.5,
            height=0.5
        )
        
        # Bottom-left
        bottom_left = chart.create_subchart(
            position='bottom',
            width=0.5,
            height=0.5
        )
        
        # Bottom-right (create from bottom-left)
        bottom_right = bottom_left.create_subchart(
            position='right',
            width=1.0,  # Takes full width of remaining space
            height=1.0
        )
        
        return top_right, bottom_left, bottom_right
    
    @staticmethod
    def grid_3x3(chart):
        """
        Create 3x3 grid layout
        
        Args:
            chart: Main Chart object
            
        Returns:
            List of 8 subchart objects (9 total including main)
        """
        # Resize main chart (top-left)
        chart.resize(width=0.33, height=0.33)
        
        subcharts = []
        
        # Top row: add 2 more
        top_middle = chart.create_subchart(position='right', width=0.33, height=0.33)
        top_right = chart.create_subchart(position='right', width=0.34, height=0.33)
        subcharts.extend([top_middle, top_right])
        
        # Middle row: create from main chart
        mid_left = chart.create_subchart(position='bottom', width=0.33, height=0.33)
        mid_middle = mid_left.create_subchart(position='right', width=0.33, height=1.0)
        mid_right = mid_left.create_subchart(position='right', width=0.34, height=1.0)
        subcharts.extend([mid_left, mid_middle, mid_right])
        
        # Bottom row: create from mid_left
        bottom_left = mid_left.create_subchart(position='bottom', width=0.33, height=1.0)
        bottom_middle = bottom_left.create_subchart(position='right', width=0.33, height=1.0)
        bottom_right = bottom_left.create_subchart(position='right', width=0.34, height=1.0)
        subcharts.extend([bottom_left, bottom_middle, bottom_right])
        
        return subcharts
    
    @staticmethod
    def main_with_side_indicators(chart, num_side_indicators=3):
        """
        Create 1 large chart on left + N indicator charts stacked on right
        Perfect for trading with main chart + multiple indicators
        
        Args:
            chart: Main Chart object
            num_side_indicators: Number of indicator panes on right (1-6)
            
        Returns:
            List of right-side subchart objects
        """
        if num_side_indicators < 1 or num_side_indicators > 6:
            raise ValueError("num_side_indicators must be between 1 and 6")
        
        # DON'T resize the main chart - it already has data
        # Just create the right panels with proper sizing
        
        side_width = 0.35  # Right side takes 35% width
        indicator_height = 1.0 / num_side_indicators
        
        # Create right-side indicator subcharts
        subcharts = []
        for i in range(num_side_indicators):
            if i == 0:
                # First panel: create from main chart at 'right' position
                sub = chart.create_subchart(
                    position='right',
                    width=side_width,
                    height=indicator_height
                )
            else:
                # Stack subsequent panels below the first right panel
                # Each takes proportionally more of remaining space
                remaining_height = 1.0 / (num_side_indicators - i)
                sub = subcharts[0].create_subchart(
                    position='bottom',
                    width=1.0,
                    height=remaining_height
                )
            subcharts.append(sub)
        
        return subcharts


    @staticmethod
    def six_panel_grid(chart):
        """
        Create 2x3 grid (6 panels total)
        
        Args:
            chart: Main Chart object
            
        Returns:
            List of 5 subchart objects (6 total including main)
        """
        # Main chart: top-left
        chart.resize(width=0.5, height=0.33)
        
        subcharts = []
        
        # Top row
        top_right = chart.create_subchart(position='right', width=0.5, height=0.33)
        subcharts.append(top_right)
        
        # Middle row
        mid_left = chart.create_subchart(position='bottom', width=0.5, height=0.33)
        mid_right = mid_left.create_subchart(position='right', width=1.0, height=1.0)
        subcharts.extend([mid_left, mid_right])
        
        # Bottom row
        bottom_left = mid_left.create_subchart(position='bottom', width=0.5, height=1.0)
        bottom_right = bottom_left.create_subchart(position='right', width=1.0, height=1.0)
        subcharts.extend([bottom_left, bottom_right])
        
        return subcharts