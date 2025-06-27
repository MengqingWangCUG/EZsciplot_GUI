import matplotlib.pyplot as plt
# Fix: Use the correct backend for PySide6
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtCore import QSize


class MplCanvas(FigureCanvas):
    """
    Matplotlib Canvas Wrapper Class
    
    A custom FigureCanvas wrapper that provides standardized plotting interface
    for Qt widgets with support for:
    - Automatic canvas size adjustment
    - Fixed aspect ratio options
    - Expandable size policy
    - Tight layout management
    """
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """
        Initialize matplotlib canvas
        
        Args:
            parent: Parent widget
            width (float): Figure width in inches
            height (float): Figure height in inches  
            dpi (int): Dots per inch for figure resolution
        """
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        
        super().__init__(self.fig)
        self.setParent(parent)
        
        # Set size policy for expanding behavior
        FigureCanvas.setSizePolicy(self, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        # Fixed aspect ratio flag
        self._fixed_aspect_ratio = False
        
        # Set tight layout for the figure
        self.fig.tight_layout()

    def setFixedAspectRatio(self, fixed=True):
        """
        Set whether to maintain fixed aspect ratio
        
        Args:
            fixed (bool): True to maintain fixed aspect ratio, False otherwise
        """
        self._fixed_aspect_ratio = fixed
        if fixed:
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def sizeHint(self):
        """
        Return recommended size for the widget
        
        Returns:
            QSize: Recommended size, square if fixed aspect ratio is enabled
        """
        if self._fixed_aspect_ratio:
            # Return square dimensions
            size = min(self.parent().width() - 40, self.parent().height() - 80) if self.parent() else 300
            return QSize(size, size)
        return super().sizeHint()

    def heightForWidth(self, width):
        """
        Return corresponding height for given width (maintains square shape)
        
        Args:
            width (int): Widget width
            
        Returns:
            int: Corresponding height (equal to width for square shape)
        """
        if self._fixed_aspect_ratio:
            return width
        return super().heightForWidth(width)

    def hasHeightForWidth(self):
        """
        Indicate whether widget supports width-based height calculation
        
        Returns:
            bool: True if fixed aspect ratio is enabled
        """
        return self._fixed_aspect_ratio

    def resizeEvent(self, event):
        """
        Override resize event to maintain square proportions when needed
        
        Args:
            event: Qt resize event object
        """
        if self._fixed_aspect_ratio:
            # Calculate square dimensions
            size = min(event.size().width(), event.size().height())
            # Set to square shape
            if event.size().width() != size or event.size().height() != size:
                self.resize(size, size)
        super().resizeEvent(event)

    def clear_plot(self):
        """Clear the current plot and reset axes"""
        self.ax.clear()
        self.draw()

    def update_plot(self):
        """Update the plot display"""
        self.fig.tight_layout()
        self.draw()

    def save_plot(self, filename, **kwargs):
        """
        Save the current plot to file
        
        Args:
            filename (str): Output filename with extension
            **kwargs: Additional arguments passed to savefig()
        """
        default_kwargs = {
            'dpi': 300,
            'bbox_inches': 'tight',
            'facecolor': 'white',
            'edgecolor': 'none'
        }
        default_kwargs.update(kwargs)
        self.fig.savefig(filename, **default_kwargs)

    def set_background_color(self, color='white'):
        """
        Set the background color of the figure
        
        Args:
            color (str): Color specification (name, hex, etc.)
        """
        self.fig.patch.set_facecolor(color)
        self.ax.set_facecolor(color)
        self.draw()

    def get_figure(self):
        """
        Get the matplotlib figure object
        
        Returns:
            Figure: The matplotlib figure object
        """
        return self.fig

    def get_axes(self):
        """
        Get the matplotlib axes object
        
        Returns:
            Axes: The matplotlib axes object
        """
        return self.ax