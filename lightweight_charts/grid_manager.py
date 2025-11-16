"""
Grid Layout Manager for TradingView Lightweight Charts
Handles proper positioning of multiple subcharts in grid layouts
"""
from typing import List, Tuple, Dict, Literal, Optional
from dataclasses import dataclass

@dataclass
class GridCell:
    """Represents a cell in the grid"""
    row: int
    col: int
    width: float
    height: float
    x_offset: float
    y_offset: float
    chart: Optional['AbstractChart'] = None


class GridLayoutManager:
    """
    Manages grid layouts for charts
    
    Handles positioning logic for 2x2, 3x3, and custom grid configurations
    """
    
    def __init__(self, rows: int, cols: int, total_width: float = 1.0, total_height: float = 1.0):
        """
        Initialize grid layout
        
        Args:
            rows: Number of rows
            cols: Number of columns
            total_width: Total width (0.0 to 1.0)
            total_height: Total height (0.0 to 1.0)
        """
        self.rows = rows
        self.cols = cols
        self.total_width = total_width
        self.total_height = total_height
        self.cells: Dict[Tuple[int, int], GridCell] = {}
        self._calculate_cells()
    
    def _calculate_cells(self):
        """Calculate position and size for each cell"""
        cell_width = self.total_width / self.cols
        cell_height = self.total_height / self.rows
        
        for row in range(self.rows):
            for col in range(self.cols):
                x_offset = col * cell_width
                y_offset = row * cell_height
                
                cell = GridCell(
                    row=row,
                    col=col,
                    width=cell_width,
                    height=cell_height,
                    x_offset=x_offset,
                    y_offset=y_offset
                )
                self.cells[(row, col)] = cell
    
    def get_cell(self, row: int, col: int) -> GridCell:
        """Get cell at specific position"""
        return self.cells.get((row, col))
    
    def get_cell_config(self, row: int, col: int) -> Dict:
        """Get configuration dict for creating a subchart in this cell"""
        cell = self.get_cell(row, col)
        if not cell:
            raise ValueError(f"Invalid cell position: ({row}, {col})")
        
        return {
            'width': cell.width,
            'height': cell.height,
            'x_offset': cell.x_offset,
            'y_offset': cell.y_offset
        }
    
    def assign_chart(self, row: int, col: int, chart: 'AbstractChart'):
        """Assign a chart to a specific cell"""
        cell = self.get_cell(row, col)
        if cell:
            cell.chart = chart
    
    @staticmethod
    def create_2x2(main_chart: 'AbstractChart') -> Tuple['AbstractChart', 'AbstractChart', 'AbstractChart']:
        """
        Create 2x2 grid layout
        
        Args:
            main_chart: The main chart (will become top-left)
            
        Returns:
            Tuple of (top_right, bottom_left, bottom_right) subcharts
        """
        # Resize main chart to top-left (50% x 50%)
        main_chart.resize(width=0.5, height=0.5)
        
        # Create top-right subchart
        top_right = main_chart.create_subchart(
            position='right',
            width=0.5,
            height=0.5,
            sync_crosshairs_only=False
        )
        
        # Create bottom-left subchart
        bottom_left = main_chart.create_subchart(
            position='bottom',
            width=0.5,
            height=0.5,
            sync_crosshairs_only=False
        )
        
        # Create bottom-right subchart from bottom-left
        bottom_right = bottom_left.create_subchart(
            position='right',
            width=1.0,  # Takes remaining width
            height=1.0,  # Takes full height of its row
            sync_crosshairs_only=False
        )
        
        return top_right, bottom_left, bottom_right
    
    @staticmethod
    def create_3x3(main_chart: 'AbstractChart') -> List['AbstractChart']:
        """
        Create 3x3 grid layout
        
        Args:
            main_chart: The main chart (will become top-left)
            
        Returns:
            List of 8 subcharts (9 total including main)
        """
        # Resize main to top-left corner (33% x 33%)
        main_chart.resize(width=0.33, height=0.33)
        
        subcharts = []
        
        # Row 1: Top middle and top right
        top_middle = main_chart.create_subchart(
            position='right',
            width=0.33,
            height=0.33,
            sync_crosshairs_only=False
        )
        top_right = top_middle.create_subchart(
            position='right',
            width=0.34,  # Slightly larger for rounding
            height=1.0,
            sync_crosshairs_only=False
        )
        subcharts.extend([top_middle, top_right])
        
        # Row 2: Create from main chart going down
        mid_left = main_chart.create_subchart(
            position='bottom',
            width=0.33,
            height=0.33,
            sync_crosshairs_only=False
        )
        mid_middle = mid_left.create_subchart(
            position='right',
            width=0.33,
            height=1.0,
            sync_crosshairs_only=False
        )
        mid_right = mid_middle.create_subchart(
            position='right',
            width=0.34,
            height=1.0,
            sync_crosshairs_only=False
        )
        subcharts.extend([mid_left, mid_middle, mid_right])
        
        # Row 3: Create from mid_left going down
        bottom_left = mid_left.create_subchart(
            position='bottom',
            width=0.33,
            height=1.0,
            sync_crosshairs_only=False
        )
        bottom_middle = bottom_left.create_subchart(
            position='right',
            width=0.33,
            height=1.0,
            sync_crosshairs_only=False
        )
        bottom_right = bottom_middle.create_subchart(
            position='right',
            width=0.34,
            height=1.0,
            sync_crosshairs_only=False
        )
        subcharts.extend([bottom_left, bottom_middle, bottom_right])
        
        return subcharts
    
    @staticmethod
    def create_1x4_vertical(main_chart: 'AbstractChart') -> Tuple['AbstractChart', 'AbstractChart', 'AbstractChart']:
        """
        Create 1x4 vertical stack (4 charts stacked vertically)
        
        Args:
            main_chart: The main chart (will become top chart)
            
        Returns:
            Tuple of (chart2, chart3, chart4)
        """
        main_chart.resize(width=1.0, height=0.25)
        
        chart2 = main_chart.create_subchart(
            position='bottom',
            width=1.0,
            height=0.25,
            sync_crosshairs_only=False
        )
        
        chart3 = chart2.create_subchart(
            position='bottom',
            width=1.0,
            height=0.33,  # 1/3 of remaining space
            sync_crosshairs_only=False
        )
        
        chart4 = chart3.create_subchart(
            position='bottom',
            width=1.0,
            height=0.5,  # 1/2 of remaining space (fills rest)
            sync_crosshairs_only=False
        )
        
        return chart2, chart3, chart4