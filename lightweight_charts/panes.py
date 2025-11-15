"""
Proper pane implementation using TradingView Lightweight Charts v5 paneIndex API
"""
from typing import Optional, List, TYPE_CHECKING
from .util import jbool

if TYPE_CHECKING:
    from .abstract import AbstractChart, Line, Histogram


class PaneManager:
    """Manages panes using the official TradingView paneIndex system"""
    
    def __init__(self, chart: 'AbstractChart'):
        self.chart = chart
        self._panes: List[int] = [0]  # Main pane is always index 0
        self._series_by_pane = {0: []}  # Track which series are in which pane
        
    def create_pane(self, height: Optional[int] = None) -> int:
        """
        Create a new pane and return its index.
        
        Args:
            height: Height in pixels (optional)
            
        Returns:
            The pane index
        """
        pane_index = len(self._panes)
        self._panes.append(pane_index)
        self._series_by_pane[pane_index] = []
        
        if height:
            self.chart.run_script(f'''
                // Pane will be created automatically when series is added with paneIndex
                // Store height preference for when series is added
                if (!{self.chart.id}._paneHeights) {{
                    {self.chart.id}._paneHeights = {{}};
                }}
                {self.chart.id}._paneHeights[{pane_index}] = {height};
            ''', run_last=True)
        
        return pane_index
    
    def set_pane_height(self, pane_index: int, height: int):
        """Set the height of a specific pane in pixels"""
        self.chart.run_script(f'''
            const panes = {self.chart.id}.chart.panes();
            if (panes[{pane_index}]) {{
                panes[{pane_index}].setHeight({height});
            }}
        ''')
    
    def move_pane(self, pane_index: int, target_index: int):
        """Move a pane to a different position"""
        self.chart.run_script(f'''
            const panes = {self.chart.id}.chart.panes();
            if (panes[{pane_index}]) {{
                panes[{pane_index}].moveTo({target_index});
            }}
        ''')
    
    def remove_pane(self, pane_index: int):
        """Remove a pane (and all its series)"""
        if pane_index == 0:
            raise ValueError("Cannot remove the main pane (index 0)")
        
        self.chart.run_script(f'{self.chart.id}.chart.removePane({pane_index});')
        
        if pane_index in self._panes:
            self._panes.remove(pane_index)
        if pane_index in self._series_by_pane:
            del self._series_by_pane[pane_index]
    
    def configure_panes(
        self,
        separator_color: str = '#2B2B43',
        separator_hover_color: str = 'rgba(255, 0, 0, 0.1)',
        enable_resize: bool = True
    ):
        """Configure visual options for all panes"""
        self.chart.run_script(f'''
            {self.chart.id}.chart.applyOptions({{
                layout: {{
                    panes: {{
                        separatorColor: '{separator_color}',
                        separatorHoverColor: '{separator_hover_color}',
                        enableResize: {jbool(enable_resize)}
                    }}
                }}
            }});
        ''')
    
    def get_pane_count(self) -> int:
        """Get the number of panes"""
        return len(self._panes)
    
    def track_series(self, series, pane_index: int):
        """Internal method to track which series are in which pane"""
        if pane_index not in self._series_by_pane:
            self._series_by_pane[pane_index] = []
        self._series_by_pane[pane_index].append(series)