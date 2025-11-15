"""
Visual pane dividers for multi-pane layouts
"""

class PaneDivider:
    """Adds visual separator between panes"""
    
    def __init__(self, chart, pane_index: int, color: str = '#3C434C', width: int = 2):
        """
        Add a visual divider above a pane
        
        Args:
            chart: The chart object
            pane_index: Which pane to add divider above (1, 2, 3...)
            color: Divider color
            width: Divider width in pixels
        """
        self.chart = chart
        self.pane_index = pane_index
        
        # Add CSS for the divider
        chart.run_script(f'''
            // Add divider CSS if not already added
            if (!document.getElementById('pane-divider-style')) {{
                const style = document.createElement('style');
                style.id = 'pane-divider-style';
                style.textContent = `
                    .pane-divider {{
                        position: absolute;
                        left: 0;
                        right: 0;
                        height: {width}px;
                        background: {color};
                        z-index: 1000;
                        pointer-events: none;
                    }}
                    .pane-divider:hover {{
                        background: rgba(100, 150, 255, 0.5);
                    }}
                `;
                document.head.appendChild(style);
            }}
        ''')