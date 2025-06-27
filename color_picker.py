from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, 
    QListWidget, QListWidgetItem, QColorDialog, QSpinBox, QLineEdit, 
    QGridLayout, QGroupBox, QSlider, QTabWidget, QWidget, QScrollArea, 
    QSizePolicy
)
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt, Signal
import colorsys


class ColorPickerArea(QWidget):
    """Main color selection area for saturation and value adjustment"""
    color_changed = Signal(float, float)  # sat, val
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(256, 128)
        self.current_hue = 0.5
        self.current_sat = 1.0
        self.current_val = 1.0
        
    def set_hue(self, hue):
        """Set hue value"""
        self.current_hue = hue
        self.update()
        
    def set_position(self, sat, val):
        """Set saturation and value position"""
        self.current_sat = sat
        self.current_val = val
        self.update()
        
    def paintEvent(self, event):
        """Paint the color area with saturation-value gradient"""
        painter = QPainter(self)
        
        # Draw saturation-value gradient
        for x in range(256):
            for y in range(128):
                sat = x / 255.0
                val = 1.0 - (y / 127.0)
                
                r, g, b = colorsys.hsv_to_rgb(self.current_hue, sat, val)
                color = QColor(int(r * 255), int(g * 255), int(b * 255))
                painter.setPen(color)
                painter.drawPoint(x, y)
        
        # Draw current position marker
        x = int(self.current_sat * 255)
        y = int((1.0 - self.current_val) * 127)
        
        painter.setPen(QColor(255, 255, 255))
        painter.drawEllipse(x - 3, y - 3, 6, 6)
        painter.setPen(QColor(0, 0, 0))
        painter.drawEllipse(x - 2, y - 2, 4, 4)
        
    def mousePressEvent(self, event):
        """Handle mouse press events"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.update_color_from_position(event.position().toPoint())
            
    def mouseMoveEvent(self, event):
        """Handle mouse move events"""
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.update_color_from_position(event.position().toPoint())
            
    def update_color_from_position(self, pos):
        """Update color based on mouse position"""
        x = max(0, min(255, pos.x()))
        y = max(0, min(127, pos.y()))
        
        sat = x / 255.0
        val = 1.0 - (y / 127.0)
        
        self.current_sat = sat
        self.current_val = val
        
        # Emit signal
        self.color_changed.emit(sat, val)
            
        self.update()


class HueBar(QWidget):
    """Hue selection bar widget"""
    
    # Define signals
    hue_changed = Signal(float)  # hue
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(256, 20)
        self.current_hue = 0.5
        
    def set_hue(self, hue):
        """Set hue value"""
        self.current_hue = hue
        self.update()
        
    def paintEvent(self, event):
        """Paint the hue bar with hue gradient"""
        painter = QPainter(self)
        
        # Draw hue gradient
        for x in range(256):
            hue = x / 255.0
            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            color = QColor(int(r * 255), int(g * 255), int(b * 255))
            painter.setPen(color)
            painter.drawLine(x, 0, x, 20)
        
        # Draw current position marker
        x = int(self.current_hue * 255)
        painter.setPen(QColor(255, 255, 255))
        painter.drawLine(x, 0, x, 20)
        painter.setPen(QColor(0, 0, 0))
        painter.drawLine(x - 1, 0, x - 1, 20)
        painter.drawLine(x + 1, 0, x + 1, 20)
        
    def mousePressEvent(self, event):
        """Handle mouse press events"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.update_hue_from_position(event.position().toPoint())
            
    def mouseMoveEvent(self, event):
        """Handle mouse move events"""
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.update_hue_from_position(event.position().toPoint())
            
    def update_hue_from_position(self, pos):
        """Update hue based on mouse position"""
        x = max(0, min(255, pos.x()))
        hue = x / 255.0
        
        self.current_hue = hue
        
        # Emit signal
        self.hue_changed.emit(hue)
            
        self.update()


class GradientColorPicker(QWidget):
    """Adobe-style gradient color picker widget"""
    
    def __init__(self, initial_color='blue'):
        super().__init__()
        self.current_color = initial_color
        self.current_hue = 0.5  # Current hue (0-1)
        self.current_sat = 1.0  # Current saturation (0-1)
        self.current_val = 1.0  # Current value (0-1)
        self.color_changed_callback = None
        self.setFixedSize(300, 280)
        self.create_ui()
        
    def create_ui(self):
        """Create the user interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        # Main color selection area
        self.color_area = ColorPickerArea(self)
        self.color_area.color_changed.connect(self.on_color_area_changed)
        layout.addWidget(self.color_area)
        
        # Hue bar
        self.hue_bar = HueBar(self)
        self.hue_bar.hue_changed.connect(self.on_hue_changed)
        layout.addWidget(self.hue_bar)
        
        # Add some spacing
        layout.addSpacing(10)
        
        # Color code input area
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Color:"))
        
        self.color_input = QLineEdit(self.current_color)
        self.color_input.textChanged.connect(self.on_color_input_changed)
        input_layout.addWidget(self.color_input)
        
        self.color_preview = QPushButton()
        self.color_preview.setFixedSize(30, 25)
        self.color_preview.clicked.connect(self.open_color_dialog)
        input_layout.addWidget(self.color_preview)
        
        layout.addLayout(input_layout)
        
        # RGB input controls
        rgb_layout = QHBoxLayout()
        rgb_layout.addWidget(QLabel("R:"))
        self.r_spin = QSpinBox()
        self.r_spin.setRange(0, 255)
        self.r_spin.valueChanged.connect(self.on_rgb_changed)
        rgb_layout.addWidget(self.r_spin)
        
        rgb_layout.addWidget(QLabel("G:"))
        self.g_spin = QSpinBox()
        self.g_spin.setRange(0, 255)
        self.g_spin.valueChanged.connect(self.on_rgb_changed)
        rgb_layout.addWidget(self.g_spin)
        
        rgb_layout.addWidget(QLabel("B:"))
        self.b_spin = QSpinBox()
        self.b_spin.setRange(0, 255)
        self.b_spin.valueChanged.connect(self.on_rgb_changed)
        rgb_layout.addWidget(self.b_spin)
        
        layout.addLayout(rgb_layout)
        
        self.update_color_preview()
        
    def on_color_area_changed(self, sat, val):
        """Handle color area changes"""
        self.current_sat = sat
        self.current_val = val
        self.update_from_hsv()
        
    def on_hue_changed(self, hue):
        """Handle hue changes"""
        self.current_hue = hue
        self.color_area.set_hue(hue)
        self.update_from_hsv()
        
    def update_from_hsv(self):
        """Update color display from HSV values"""
        r, g, b = colorsys.hsv_to_rgb(self.current_hue, self.current_sat, self.current_val)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        
        self.r_spin.blockSignals(True)
        self.g_spin.blockSignals(True)
        self.b_spin.blockSignals(True)
        
        self.r_spin.setValue(r)
        self.g_spin.setValue(g)
        self.b_spin.setValue(b)
        
        self.r_spin.blockSignals(False)
        self.g_spin.blockSignals(False)
        self.b_spin.blockSignals(False)
        
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.current_color = hex_color
        
        self.color_input.blockSignals(True)
        self.color_input.setText(hex_color)
        self.color_input.blockSignals(False)
        
        self.update_color_preview()
        
        if self.color_changed_callback:
            self.color_changed_callback(hex_color)
            
    def on_rgb_changed(self):
        """Handle RGB value changes"""
        r = self.r_spin.value() / 255.0
        g = self.g_spin.value() / 255.0
        b = self.b_spin.value() / 255.0
        
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        
        self.current_hue = h
        self.current_sat = s
        self.current_val = v
        
        self.hue_bar.set_hue(h)
        self.color_area.set_hue(h)
        self.color_area.set_position(s, v)
        
        hex_color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
        self.current_color = hex_color
        
        self.color_input.blockSignals(True)
        self.color_input.setText(hex_color)
        self.color_input.blockSignals(False)
        
        self.update_color_preview()
        
        if self.color_changed_callback:
            self.color_changed_callback(hex_color)
            
    def on_color_input_changed(self, text):
        """Handle color input text changes"""
        try:
            if text.startswith('#') and len(text) == 7:
                r = int(text[1:3], 16) / 255.0
                g = int(text[3:5], 16) / 255.0
                b = int(text[5:7], 16) / 255.0
                
                h, s, v = colorsys.rgb_to_hsv(r, g, b)
                
                self.current_hue = h
                self.current_sat = s
                self.current_val = v
                self.current_color = text
                
                self.hue_bar.set_hue(h)
                self.color_area.set_hue(h)
                self.color_area.set_position(s, v)
                
                self.r_spin.blockSignals(True)
                self.g_spin.blockSignals(True)
                self.b_spin.blockSignals(True)
                
                self.r_spin.setValue(int(r * 255))
                self.g_spin.setValue(int(g * 255))
                self.b_spin.setValue(int(b * 255))
                
                self.r_spin.blockSignals(False)
                self.g_spin.blockSignals(False)
                self.b_spin.blockSignals(False)
                
                self.update_color_preview()
                
                if self.color_changed_callback:
                    self.color_changed_callback(text)
        except:
            pass
            
    def update_color_preview(self):
        """Update the color preview button"""
        from config import LayoutConfig
        
        preview_style = LayoutConfig.COLOR_PICKER_STYLES['color_preview']
        self.color_preview.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.current_color};
                border: {preview_style['border']};
                border-radius: {preview_style['border_radius']};
            }}
        """)
        
    def open_color_dialog(self):
        """Open system color dialog"""
        color = QColorDialog.getColor()
        if color.isValid():
            hex_color = color.name()
            self.color_input.setText(hex_color)
            
    def get_color(self):
        """Get current selected color"""
        return self.current_color


class ColorPaletteWidget(QWidget):
    """Color picker widget with Adobe-style gradient color panel and input field"""
    
    def __init__(self, initial_color='blue'):
        super().__init__()
        self.current_color = initial_color
        self.color_changed_callback = None
        self.create_ui()
        
    def create_ui(self):
        """Create the user interface"""
        layout = QVBoxLayout(self)
        
        # Adobe-style gradient color picker
        gradient_group = QGroupBox("Color Picker")
        gradient_layout = QVBoxLayout()
        
        self.gradient_picker = GradientColorPicker(self.current_color)
        self.gradient_picker.color_changed_callback = self.on_gradient_color_changed
        gradient_layout.addWidget(self.gradient_picker)
        
        gradient_group.setLayout(gradient_layout)
        layout.addWidget(gradient_group)
        
        # Preset color quick selection
        preset_group = QGroupBox("Quick Colors")
        preset_layout = QGridLayout()
        preset_layout.setSpacing(2)
        preset_layout.setContentsMargins(5, 5, 5, 5)
        
        # Common colors
        preset_colors = [
            '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF',
            '#800000', '#008000', '#000080', '#808000', '#800080', '#008080',
            '#FFA500', '#FFC0CB', '#A52A2A', '#808080', '#000000', '#FFFFFF'
        ]
        
        row, col = 0, 0
        for color in preset_colors:
            color_btn = QPushButton()
            color_btn.setFixedSize(18, 18)
            color_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    border: 1px solid #666;
                    border-radius: 2px;
                    margin: 0px;
                    padding: 0px;
                }}
                QPushButton:hover {{
                    border: 2px solid #333;
                    border-radius: 2px;
                }}
                QPushButton:pressed {{
                    border: 2px solid #000;
                    border-radius: 1px;
                }}
            """)
            color_btn.clicked.connect(lambda checked, c=color: self.set_color(c))
            preset_layout.addWidget(color_btn, row, col)
            
            col += 1
            if col >= 6:
                col = 0
                row += 1
        
        preset_group.setLayout(preset_layout)
        layout.addWidget(preset_group)
        
    def on_gradient_color_changed(self, color):
        """Handle gradient picker color changes"""
        self.current_color = color
        if self.color_changed_callback:
            self.color_changed_callback(color)
            
    def set_color(self, color):
        """Set the selected color"""
        self.current_color = color
        self.gradient_picker.color_input.setText(color)
        if self.color_changed_callback:
            self.color_changed_callback(color)
            
    def get_color(self):
        """Get current selected color"""
        return self.current_color


class PlotObjectStyleDialog(QDialog):
    """Plot object style adjustment dialog - resizable with scroll bars"""
    
    def __init__(self, parent, object_info, style_changed_callback=None):
        super().__init__(parent)
        self.object_info = object_info
        self.style_changed_callback = style_changed_callback
        self.setWindowTitle(f"Style Settings - {object_info['label']}")
        self.setModal(True)
        
        # Set window resizable
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint | Qt.WindowType.WindowMinimizeButtonHint)
        self.setSizeGripEnabled(True)
        
        # Set initial size and minimum size
        self.resize(500, 500)
        self.setMinimumSize(300, 400)
        
        # Matplotlib style options
        self.line_styles = ['-', '--', '-.', ':', 'None']
        self.line_style_names = ['Solid', 'Dashed', 'Dash-dot', 'Dotted', 'None']
        
        self.markers = ['o', 's', '^', 'v', '<', '>', 'D', 'p', '*', 'h', 'H', '+', 'x', '|', '_', '.', ',', 'None']
        self.marker_names = ['Circle', 'Square', 'Triangle Up', 'Triangle Down', 'Triangle Left', 'Triangle Right', 
                           'Diamond', 'Pentagon', 'Star', 'Hexagon1', 'Hexagon2', 'Plus', 'X', 'Vertical Line', 
                           'Horizontal Line', 'Point', 'Pixel', 'None']
        
        self.create_ui()
        
    def create_ui(self):
        """Create the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Create main scroll area
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        main_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        main_scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Create scroll content widget
        scroll_content = QWidget()
        scroll_content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Scroll content layout
        content_layout = QVBoxLayout(scroll_content)
        content_layout.setContentsMargins(5, 5, 5, 5)
        content_layout.setSpacing(10)
        
        # Create tab widget
        tab_widget = QTabWidget()
        tab_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Line style tab
        line_tab = self.create_line_style_tab()
        tab_widget.addTab(line_tab, "Line Style")
        
        # Marker style tab
        marker_tab = self.create_marker_style_tab()
        tab_widget.addTab(marker_tab, "Marker Style")
        
        # Color tab
        color_tab = self.create_color_tab()
        tab_widget.addTab(color_tab, "Colors")
        
        content_layout.addWidget(tab_widget)
        
        # Set scroll content
        main_scroll.setWidget(scroll_content)
        layout.addWidget(main_scroll)
        
        # Button area (fixed at bottom, no scrolling)
        button_layout = QHBoxLayout()
        
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply_style)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        
        button_layout.addStretch()
        button_layout.addWidget(apply_btn)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
    def create_line_style_tab(self):
        """Create line style settings tab"""
        tab = QWidget()
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create content widget
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # Line style group
        style_group = QGroupBox("Line Style")
        style_layout = QGridLayout()
        style_layout.setSpacing(10)
        
        style_layout.addWidget(QLabel("Style:"), 0, 0)
        self.line_style_combo = QComboBox()
        for i, (style, name) in enumerate(zip(self.line_styles, self.line_style_names)):
            self.line_style_combo.addItem(name, style)
        style_layout.addWidget(self.line_style_combo, 0, 1)
        
        style_layout.addWidget(QLabel("Width:"), 1, 0)
        self.line_width_spin = QSpinBox()
        self.line_width_spin.setRange(1, 20)
        self.line_width_spin.setValue(2)
        style_layout.addWidget(self.line_width_spin, 1, 1)
        
        style_layout.addWidget(QLabel("Alpha:"), 2, 0)
        self.line_alpha_slider = QSlider(Qt.Orientation.Horizontal)
        self.line_alpha_slider.setRange(0, 100)
        self.line_alpha_slider.setValue(100)
        self.line_alpha_label = QLabel("1.0")
        self.line_alpha_slider.valueChanged.connect(
            lambda v: self.line_alpha_label.setText(f"{v/100:.1f}")
        )
        alpha_layout = QHBoxLayout()
        alpha_layout.addWidget(self.line_alpha_slider)
        alpha_layout.addWidget(self.line_alpha_label)
        style_layout.addLayout(alpha_layout, 2, 1)
        
        style_group.setLayout(style_layout)
        layout.addWidget(style_group)
        
        layout.addStretch()
        
        # Set scroll content
        scroll_area.setWidget(content_widget)
        
        # Tab layout
        tab_layout = QVBoxLayout(tab)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll_area)
        
        return tab
        
    def create_marker_style_tab(self):
        """Create marker style settings tab"""
        tab = QWidget()
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create content widget
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # Marker style group
        marker_group = QGroupBox("Marker Style")
        marker_layout = QGridLayout()
        marker_layout.setSpacing(10)
        
        marker_layout.addWidget(QLabel("Marker:"), 0, 0)
        self.marker_combo = QComboBox()
        for i, (marker, name) in enumerate(zip(self.markers, self.marker_names)):
            self.marker_combo.addItem(name, marker)
        marker_layout.addWidget(self.marker_combo, 0, 1)
        
        marker_layout.addWidget(QLabel("Size:"), 1, 0)
        self.marker_size_spin = QSpinBox()
        self.marker_size_spin.setRange(1, 50)
        self.marker_size_spin.setValue(6)
        marker_layout.addWidget(self.marker_size_spin, 1, 1)
        
        marker_layout.addWidget(QLabel("Edge Width:"), 2, 0)
        self.marker_edge_width_spin = QSpinBox()
        self.marker_edge_width_spin.setRange(0, 10)
        self.marker_edge_width_spin.setValue(1)
        marker_layout.addWidget(self.marker_edge_width_spin, 2, 1)
        
        marker_group.setLayout(marker_layout)
        layout.addWidget(marker_group)
        
        layout.addStretch()
        
        # Set scroll content
        scroll_area.setWidget(content_widget)
        
        # Tab layout
        tab_layout = QVBoxLayout(tab)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll_area)
        
        return tab
        
    def create_color_tab(self):
        """Create color settings tab"""
        tab = QWidget()
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create content widget
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # Color type selection area
        color_type_group = QGroupBox("Color Selection")
        color_type_layout = QVBoxLayout()
        
        # Color type dropdown menu
        type_select_layout = QHBoxLayout()
        type_select_layout.addWidget(QLabel("Color Type:"))
        
        self.color_type_combo = QComboBox()
        self.color_type_combo.addItem("Line Color", "line")
        self.color_type_combo.addItem("Marker Face Color", "marker_face")
        self.color_type_combo.addItem("Marker Edge Color", "marker_edge")
        self.color_type_combo.currentIndexChanged.connect(self.on_color_type_changed)
        type_select_layout.addWidget(self.color_type_combo)
        type_select_layout.addStretch()
        
        color_type_layout.addLayout(type_select_layout)
        
        # Color picker container
        self.color_picker_container = QWidget()
        self.color_picker_layout = QVBoxLayout(self.color_picker_container)
        
        # Create three color pickers, but only show one at a time
        self.line_color_palette = ColorPaletteWidget('blue')
        self.marker_face_color_palette = ColorPaletteWidget('blue') 
        self.marker_edge_color_palette = ColorPaletteWidget('black')
        
        # Add all color pickers to layout but hide them initially
        self.color_picker_layout.addWidget(self.line_color_palette)
        self.color_picker_layout.addWidget(self.marker_face_color_palette)
        self.color_picker_layout.addWidget(self.marker_edge_color_palette)
        
        # Initially show line color picker
        self.marker_face_color_palette.hide()
        self.marker_edge_color_palette.hide()
        
        color_type_layout.addWidget(self.color_picker_container)
        color_type_group.setLayout(color_type_layout)
        layout.addWidget(color_type_group)
        
        # Current color selection display
        current_color_group = QGroupBox("Current Selection")
        current_color_layout = QGridLayout()
        current_color_layout.setSpacing(10)
        
        # Display preview of current colors
        current_color_layout.addWidget(QLabel("Line Color:"), 0, 0)
        self.line_color_preview = QPushButton()
        self.line_color_preview.setFixedSize(60, 30)
        self.line_color_preview.setStyleSheet("background-color: blue; border: 1px solid black;")
        current_color_layout.addWidget(self.line_color_preview, 0, 1)
        
        current_color_layout.addWidget(QLabel("Marker Face:"), 1, 0)
        self.marker_face_preview = QPushButton()
        self.marker_face_preview.setFixedSize(60, 30)
        self.marker_face_preview.setStyleSheet("background-color: blue; border: 1px solid black;")
        current_color_layout.addWidget(self.marker_face_preview, 1, 1)
        
        current_color_layout.addWidget(QLabel("Marker Edge:"), 2, 0)
        self.marker_edge_preview = QPushButton()
        self.marker_edge_preview.setFixedSize(60, 30)
        self.marker_edge_preview.setStyleSheet("background-color: black; border: 1px solid black;")
        current_color_layout.addWidget(self.marker_edge_preview, 2, 1)
        
        current_color_group.setLayout(current_color_layout)
        layout.addWidget(current_color_group)
        
        # Connect color change callbacks
        self.line_color_palette.color_changed_callback = self.on_line_color_changed
        self.marker_face_color_palette.color_changed_callback = self.on_marker_face_color_changed
        self.marker_edge_color_palette.color_changed_callback = self.on_marker_edge_color_changed
        
        layout.addStretch()
        
        # Set scroll content
        scroll_area.setWidget(content_widget)
        
        # Tab layout
        tab_layout = QVBoxLayout(tab)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll_area)
        
        return tab
    
    def on_color_type_changed(self, index):
        """Handle color type selection changes"""
        color_type = self.color_type_combo.currentData()
        
        # Hide all color pickers
        self.line_color_palette.hide()
        self.marker_face_color_palette.hide()
        self.marker_edge_color_palette.hide()
        
        # Show selected color picker
        if color_type == "line":
            self.line_color_palette.show()
        elif color_type == "marker_face":
            self.marker_face_color_palette.show()
        elif color_type == "marker_edge":
            self.marker_edge_color_palette.show()
    
    def on_line_color_changed(self, color):
        """Handle line color changes"""
        self.line_color_preview.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
        
    def on_marker_face_color_changed(self, color):
        """Handle marker face color changes"""
        self.marker_face_preview.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
        
    def on_marker_edge_color_changed(self, color):
        """Handle marker edge color changes"""
        self.marker_edge_preview.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
        
    def get_current_style(self):
        """Get current style settings"""
        return {
            'linestyle': self.line_style_combo.currentData(),
            'linewidth': self.line_width_spin.value(),
            'alpha': self.line_alpha_slider.value() / 100.0,
            'marker': self.marker_combo.currentData(),
            'markersize': self.marker_size_spin.value(),
            'markeredgewidth': self.marker_edge_width_spin.value(),
            'color': self.line_color_palette.get_color(),
            'markerfacecolor': self.marker_face_color_palette.get_color(),
            'markeredgecolor': self.marker_edge_color_palette.get_color()
        }
        
    def apply_style(self):
        """Apply the current style settings"""
        style = self.get_current_style()
        if self.style_changed_callback:
            self.style_changed_callback(self.object_info, style)


class PlotObjectListDialog(QDialog):
    """Plot object list dialog - resizable with scroll bars"""
    
    def __init__(self, parent, plot_info):
        super().__init__(parent)
        self.plot_info = plot_info
        self.setWindowTitle(f"Plot Objects - {plot_info['title']}")
        self.setModal(True)
        
        # Set window resizable
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint | Qt.WindowType.WindowMinimizeButtonHint)
        self.setSizeGripEnabled(True)
        
        # Set initial size and minimum size
        self.resize(300, 400)
        self.setMinimumSize(200, 200)
        
        self.create_ui()
        self.populate_objects()
        
    def create_ui(self):
        """Create the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Information label
        info_label = QLabel(f"Select an object to modify its style:")
        info_label.setStyleSheet("font-weight: bold; margin: 10px 0;")
        layout.addWidget(info_label)
        
        # Create scroll area containing object list
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Object list
        self.object_list = QListWidget()
        self.object_list.itemDoubleClicked.connect(self.on_object_selected)
        self.object_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Set list styling
        self.object_list.setStyleSheet("""
            QListWidget {
                background-color: #f8f8f8;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
                border-radius: 3px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background-color: #e0e0e0;
                color: #000;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
            }
        """)
        
        # Put list in scroll area
        scroll_area.setWidget(self.object_list)
        layout.addWidget(scroll_area)
        
        # Button area (fixed at bottom)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        close_btn.setMinimumHeight(35)
        
        # Set button styling
        button_style = """
            QPushButton {
                background-color: #e8e8e8;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #d8d8d8;
            }
            QPushButton:pressed {
                background-color: #c8c8c8;
            }
        """
        
        close_btn.setStyleSheet(button_style)
        
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
    def populate_objects(self):
        """Populate the object list with plot elements"""
        self.object_list.clear()
        
        # Get all objects from the plot area
        canvas = self.plot_info['canvas']
        ax = canvas.ax
        
        # Add line objects
        for i, line in enumerate(ax.get_lines()):
            label = line.get_label() if line.get_label() and not line.get_label().startswith('_') else f"Line {i+1}"
            item = QListWidgetItem(f"📈 {label}")
            item.setData(Qt.ItemDataRole.UserRole, {
                'type': 'line',
                'object': line,
                'label': label,
                'index': i
            })
            self.object_list.addItem(item)
        
        # Add scatter plot objects
        for i, collection in enumerate(ax.collections):
            label = f"Scatter {i+1}"
            item = QListWidgetItem(f"🔴 {label}")
            item.setData(Qt.ItemDataRole.UserRole, {
                'type': 'collection',
                'object': collection,
                'label': label,
                'index': i
            })
            self.object_list.addItem(item)
        
        # Add text objects
        for i, text in enumerate(ax.texts):
            label = text.get_text()[:20] + "..." if len(text.get_text()) > 20 else text.get_text()
            if not label.strip():
                label = f"Text {i+1}"
            item = QListWidgetItem(f"📝 {label}")
            item.setData(Qt.ItemDataRole.UserRole, {
                'type': 'text',
                'object': text,
                'label': label,
                'index': i
            })
            self.object_list.addItem(item)
        
    def on_object_selected(self, item):
        """Handle object selection"""
        self.edit_object(item)
            
    def edit_object(self, item):
        """Edit object style properties"""
        object_info = item.data(Qt.ItemDataRole.UserRole)
        
        # Create style editing dialog
        style_dialog = PlotObjectStyleDialog(
            self, 
            object_info, 
            self.on_style_changed
        )
        style_dialog.exec()
        
    def on_style_changed(self, object_info, style):
        """Handle style change events"""
        obj = object_info['object']
        obj_type = object_info['type']
        
        try:
            if obj_type == 'line':
                # Update line style properties
                if 'color' in style:
                    obj.set_color(style['color'])
                if 'linestyle' in style:
                    obj.set_linestyle(style['linestyle'])
                if 'linewidth' in style:
                    obj.set_linewidth(style['linewidth'])
                if 'alpha' in style:
                    obj.set_alpha(style['alpha'])
                if 'marker' in style:
                    obj.set_marker(style['marker'])
                if 'markersize' in style:
                    obj.set_markersize(style['markersize'])
                if 'markerfacecolor' in style:
                    obj.set_markerfacecolor(style['markerfacecolor'])
                if 'markeredgecolor' in style:
                    obj.set_markeredgecolor(style['markeredgecolor'])
                if 'markeredgewidth' in style:
                    obj.set_markeredgewidth(style['markeredgewidth'])
                    
            elif obj_type == 'collection':
                # Update collection object style (scatter plots, etc.)
                if 'color' in style:
                    obj.set_facecolors(style['color'])
                if 'alpha' in style:
                    obj.set_alpha(style['alpha'])
                    
            elif obj_type == 'text':
                # Update text style properties
                if 'color' in style:
                    obj.set_color(style['color'])
                if 'alpha' in style:
                    obj.set_alpha(style['alpha'])
            
            # Refresh the canvas
            self.plot_info['canvas'].draw()
            
        except Exception as e:
            # Handle any errors during style application
            pass