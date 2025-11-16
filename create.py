"""
Resizable Layout System - Proof of Concept

This adds:
1. Draggable resize handles between charts
2. Save/restore layout sizes
3. Reset button to defaults
"""

# JavaScript code to inject for resizable handles
RESIZABLE_JS = """
(function() {
    // Resizable handle system
    class ResizableLayout {
        constructor(containerId, direction, chartWrappers, defaultSizes) {
            this.container = document.getElementById(containerId);
            this.direction = direction; // 'horizontal' or 'vertical'
            this.wrappers = chartWrappers;
            this.defaultSizes = defaultSizes;
            this.currentSizes = [...defaultSizes];
            this.isDragging = false;
            this.dragIndex = -1;
            
            this.init();
        }
        
        init() {
            // Load saved sizes
            const saved = this.loadSizes();
            if (saved) {
                this.currentSizes = saved;
            }
            
            // Apply sizes
            this.applySizes();
            
            // Add handles
            this.addHandles();
            
            // Add reset button
            this.addResetButton();
        }
        
        addHandles() {
            for (let i = 0; i < this.wrappers.length - 1; i++) {
                const handle = document.createElement('div');
                handle.className = 'resize-handle';
                handle.style.cssText = this.getHandleStyle();
                handle.dataset.index = i;
                
                // Mouse events
                handle.addEventListener('mousedown', (e) => this.startDrag(e, i));
                
                // Insert after current wrapper
                this.wrappers[i].parentElement.insertBefore(
                    handle, 
                    this.wrappers[i].nextSibling
                );
            }
            
            // Global mouse events
            document.addEventListener('mousemove', (e) => this.drag(e));
            document.addEventListener('mouseup', () => this.stopDrag());
        }
        
        getHandleStyle() {
            if (this.direction === 'horizontal') {
                return `
                    position: relative;
                    width: 4px;
                    cursor: col-resize;
                    background: rgba(100, 100, 100, 0.3);
                    transition: background 0.2s;
                    z-index: 1000;
                `;
            } else {
                return `
                    position: relative;
                    height: 4px;
                    cursor: row-resize;
                    background: rgba(100, 100, 100, 0.3);
                    transition: background 0.2s;
                    z-index: 1000;
                `;
            }
        }
        
        startDrag(e, index) {
            e.preventDefault();
            this.isDragging = true;
            this.dragIndex = index;
            this.startPos = this.direction === 'horizontal' ? e.clientX : e.clientY;
            
            // Highlight handle
            e.target.style.background = 'rgba(100, 150, 255, 0.8)';
        }
        
        drag(e) {
            if (!this.isDragging) return;
            
            const currentPos = this.direction === 'horizontal' ? e.clientX : e.clientY;
            const delta = currentPos - this.startPos;
            
            const containerSize = this.direction === 'horizontal' 
                ? this.container.offsetWidth 
                : this.container.offsetHeight;
            
            const deltaPercent = (delta / containerSize) * 100;
            
            // Update sizes
            const newSizes = [...this.currentSizes];
            newSizes[this.dragIndex] += deltaPercent;
            newSizes[this.dragIndex + 1] -= deltaPercent;
            
            // Prevent negative sizes
            if (newSizes[this.dragIndex] < 10 || newSizes[this.dragIndex + 1] < 10) {
                return;
            }
            
            this.currentSizes = newSizes;
            this.startPos = currentPos;
            
            this.applySizes();
        }
        
        stopDrag() {
            if (!this.isDragging) return;
            
            this.isDragging = false;
            this.dragIndex = -1;
            
            // Reset handle colors
            document.querySelectorAll('.resize-handle').forEach(h => {
                h.style.background = 'rgba(100, 100, 100, 0.3)';
            });
            
            // Save sizes
            this.saveSizes();
        }
        
        applySizes() {
            this.wrappers.forEach((wrapper, i) => {
                if (this.direction === 'horizontal') {
                    wrapper.style.width = this.currentSizes[i] + '%';
                    wrapper.style.flex = 'none';
                } else {
                    wrapper.style.height = this.currentSizes[i] + '%';
                    wrapper.style.flex = 'none';
                }
            });
        }
        
        saveSizes() {
            const key = 'lwc_layout_' + this.direction;
            localStorage.setItem(key, JSON.stringify(this.currentSizes));
        }
        
        loadSizes() {
            const key = 'lwc_layout_' + this.direction;
            const saved = localStorage.getItem(key);
            return saved ? JSON.parse(saved) : null;
        }
        
        reset() {
            this.currentSizes = [...this.defaultSizes];
            this.applySizes();
            this.saveSizes();
        }
        
        addResetButton() {
            const btn = document.createElement('button');
            btn.innerText = '↺ Reset Layout';
            btn.style.cssText = `
                position: fixed;
                top: 10px;
                right: 10px;
                padding: 8px 16px;
                background: rgba(50, 50, 50, 0.9);
                color: #fff;
                border: 1px solid rgba(100, 100, 100, 0.5);
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
                z-index: 10000;
                transition: background 0.2s;
            `;
            
            btn.addEventListener('mouseenter', () => {
                btn.style.background = 'rgba(70, 70, 70, 0.9)';
            });
            
            btn.addEventListener('mouseleave', () => {
                btn.style.background = 'rgba(50, 50, 50, 0.9)';
            });
            
            btn.addEventListener('click', () => {
                this.reset();
            });
            
            document.body.appendChild(btn);
        }
    }
    
    // Export to window
    window.ResizableLayout = ResizableLayout;
})();
"""

def create_resizable_layout_js(chart_ids, direction, default_sizes):
    """Generate JavaScript to make layout resizable"""
    return f"""
        {RESIZABLE_JS}
        
        (function() {{
            const ids = {chart_ids};
            const wrappers = ids.map(id => window[id.replace(/^window\\./,'')].wrapper);
            
            const layout = new ResizableLayout(
                'container',
                '{direction}',
                wrappers,
                {default_sizes}
            );
        }})();
    """