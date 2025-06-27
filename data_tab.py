from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QComboBox, QTextEdit, QSizePolicy, QPushButton, QLineEdit, QScrollArea,
    QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence
from mpl_canvas import MplCanvas
from entrance import TestData
from config import LayoutConfig
import numpy as np


class DataTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.config = LayoutConfig()
        
        # 初始化列表属性
        self.data_boxes = []
        self.plot_canvases = []  # 确保这个属性被初始化
        self.canvases = []  # 兼容性属性
        
        self.init_test_data()
        self.create_ui()
        self.setup_keyboard_shortcuts()
        self.setup_connections()

    def init_test_data(self):
        """Initialize test data from entrance.py"""
        self.test_data_generator = TestData()
        self.sample_data = self.test_data_generator.sites
        range_config = self.config.RANGE_VALUES
        self.range_up_values = list(range(range_config['min'], range_config['max'] + 1))
        self.range_down_values = list(range(range_config['min'], range_config['max'] + 1))

        self.parameter_labels = self.test_data_generator.parameter_labels
        self.data_display_labels = self.test_data_generator.data_display_labels
        self.plot_titles = self.test_data_generator.plot_titles

    def create_ui(self):
        """Create user interface"""
        config = self.config.DATA_TAB
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*self.config.MAIN_WINDOW['margins'])
        layout.setSpacing(self.config.MAIN_WINDOW['spacing'])
        
        # Top layout: Current Specimen, Range Tab and Data Filter side by side
        top_layout = QHBoxLayout()
        top_layout.setSpacing(config['top_layout_spacing'])
        specimen_group = self.create_status_group()
        range_group = self.create_range_group()
        filter_group = self.create_filter_group()
        top_layout.addWidget(specimen_group, 0)  
        top_layout.addWidget(range_group, 0)     
        top_layout.addWidget(filter_group, 1)   
        
        layout.addLayout(top_layout, 0)

        # Middle layout: Plot area and data display area side by side
        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(config['top_layout_spacing'])
        plots_container = self.create_plots_container()
        data_group = self.create_data_group()
        middle_layout.addWidget(plots_container, 3)
        middle_layout.addWidget(data_group, 1)
        
        layout.addLayout(middle_layout, 1)

        # After creating filter inputs, setup their callbacks
        self.setup_filter_input_callbacks()

    def _create_adaptive_label(self, text, max_width=None, base_font_size=9):
        """Create adaptive label with optimized font size"""
        label = QLabel(text)
        
        if max_width and hasattr(self.config, 'ADAPTIVE_FONT') and self.config.ADAPTIVE_FONT.get('enable_auto_scale', False):
            # Calculate adaptive font size
            font_size = self.config.get_adaptive_font_size(text, max_width, base_font_size)
            
            label.setStyleSheet(f"""
                font-weight: {self.config.STYLES['label']['font_weight']};
                color: {self.config.STYLES['label']['color']};
                font-size: {font_size}pt;
                text-align: right;
            """)
        else:
            font_size = max(6, base_font_size - 1)  # At least 6pt, 1pt smaller than base
            label.setStyleSheet(f"""
                font-weight: {self.config.STYLES['label']['font_weight']};
                color: {self.config.STYLES['label']['color']};
                font-size: {font_size}pt;
            """)
        label.setWordWrap(False)
        label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        if max_width:
            label.setMaximumWidth(max_width)
        
        return label

    def create_status_group(self):
        """Create status display group with adaptive labels"""
        config = self.config.DATA_TAB['specimen_group']
        status_group = QGroupBox(config['title'])
        status_group.setStyleSheet(self._get_groupbox_style('specimen_group'))
        status_group.setMaximumWidth(config['max_width'])
        status_group.setMinimumWidth(config['min_width'])
        
        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(*config['margins'])
        status_layout.setSpacing(config['spacing'])
        
        # Site selection with adaptive label
        site_layout = QHBoxLayout()
        site_label = self._create_adaptive_label("Site:", config['label_width'])
        site_label.setMaximumWidth(config['label_width'])
        
        self.site_combo = QComboBox()
        self.site_combo.setMinimumWidth(config['combo_min_width'])
        self.site_combo.setMaximumHeight(config['combo_max_height'])
        self.site_combo.setStyleSheet(self._get_combobox_style())
        
        site_layout.addWidget(site_label)
        site_layout.addWidget(self.site_combo)
        status_layout.addLayout(site_layout)
        
        # Specimen selection with adaptive label
        specimen_layout = QHBoxLayout()
        specimen_label = self._create_adaptive_label("Sample:", config['label_width'])
        specimen_label.setMaximumWidth(config['label_width'])
        
        self.specimen_combo = QComboBox()
        self.specimen_combo.setMinimumWidth(config['combo_min_width'])
        self.specimen_combo.setMaximumHeight(config['combo_max_height'])
        self.specimen_combo.setStyleSheet(self._get_combobox_style())
        
        specimen_layout.addWidget(specimen_label)
        specimen_layout.addWidget(self.specimen_combo)
        status_layout.addLayout(specimen_layout)
        status_layout.addLayout(site_layout)
        status_layout.addLayout(specimen_layout)
        
        status_group.setLayout(status_layout)
        return status_group

    def create_range_group(self):
        """Create range control group with adaptive labels"""
        config = self.config.DATA_TAB['range_group']
        range_group = QGroupBox(config['title'])
        range_group.setStyleSheet(self._get_groupbox_style('range_group'))
        range_group.setMaximumWidth(config['max_width'])
        range_group.setMinimumWidth(config['min_width'])
        
        range_layout = QVBoxLayout()
        range_layout.setContentsMargins(*config['margins'])
        range_layout.setSpacing(config['spacing'])
        
        # Range Up with adaptive label
        up_layout = QHBoxLayout()
        up_label = self._create_adaptive_label("Up:", config['label_width'])
        up_label.setMaximumWidth(config['label_width'])
        
        self.range_up_combo = QComboBox()
        self.range_up_combo.setMinimumWidth(config['combo_min_width'])
        self.range_up_combo.setMaximumHeight(config['combo_max_height'])
        self.range_up_combo.setStyleSheet(self._get_combobox_style())
        
        up_layout.addWidget(up_label)
        up_layout.addWidget(self.range_up_combo)
        range_layout.addLayout(up_layout) 
        down_layout = QHBoxLayout()
        down_label = self._create_adaptive_label("Down:", config['label_width'])
        down_label.setMaximumWidth(config['label_width'])
        
        self.range_down_combo = QComboBox()
        self.range_down_combo.setMinimumWidth(config['combo_min_width'])
        self.range_down_combo.setMaximumHeight(config['combo_max_height'])
        self.range_down_combo.setStyleSheet(self._get_combobox_style())
        
        down_layout.addWidget(down_label)
        down_layout.addWidget(self.range_down_combo)
        range_layout.addLayout(down_layout)
        
        # Add two rows to vertical layout
        range_layout.addLayout(up_layout)
        range_layout.addLayout(down_layout)
        
        range_group.setLayout(range_layout)
        return range_group

    def create_filter_group(self):
        """Create data filter conditions group using parameter labels from entrance.py"""
        config = self.config.DATA_TAB['filter_group']
        filter_group = QGroupBox(config['title'])
        filter_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        filter_layout = QGridLayout()
        filter_layout.setContentsMargins(*config['margins'])
        filter_layout.setSpacing(config['spacing'])
        
        # Create filter condition input boxes using parameter labels from entrance.py
        self.filter_inputs = []
        
        for i, label_text in enumerate(self.parameter_labels):
            # Label
            label = QLabel(f"{label_text}:")
            label.setStyleSheet(f"""
                font-weight: {self.config.STYLES['label']['font_weight']};
                color: {self.config.STYLES['label']['color']};
                font-size: {self.config.STYLES['label']['font_size']['medium']};
            """)
            label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            input_field = QLineEdit()
            input_field.setPlaceholderText("Enter")
            input_field.setFixedWidth(config['input_width'])
            input_field.setStyleSheet(self._get_lineedit_style())
            
            self.filter_inputs.append(input_field)
            row = i // 2
            col = (i % 2) * 2
            
            filter_layout.addWidget(label, row, col)
            filter_layout.addWidget(input_field, row, col + 1)
        for col in range(4):
            filter_layout.setColumnStretch(col, 0)
        
        filter_group.setLayout(filter_layout)
        return filter_group

    def create_plots_container(self):
        """Create container with plot groups using plot titles from entrance.py"""
        config = self.config.DATA_TAB['plots_container']
        plots_container = QGroupBox(config['title'])
        plots_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        plots_container.setStyleSheet(self._get_groupbox_style('plots_container'))
        
        plots_layout = QVBoxLayout()
        plots_layout.setContentsMargins(*config['margins'])
        plots_layout.setSpacing(config['spacing'])
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scroll_area.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        scroll_area.wheelEvent = self.scroll_area_wheel_event
        scroll_content = QWidget()
        scroll_content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scroll_content.wheelEvent = self.scroll_area_wheel_event
        main_grid_layout = QGridLayout(scroll_content)
        main_grid_layout.setSpacing(config['grid_spacing'])
        main_grid_layout.setContentsMargins(*config['scroll_margins'])
        self.plot_groups = []
        self.canvases = []
        
        for i in range(len(self.plot_titles)):
            plot_group = self.create_individual_plot_group(i, self.plot_titles[i])
            self.plot_groups.append(plot_group)
            row = i // 2
            col = i % 2
            
            main_grid_layout.addWidget(plot_group, row, col)
            main_grid_layout.setRowStretch(row, 1)
            main_grid_layout.setColumnStretch(col, 1)
        scroll_area.setWidget(scroll_content)
        self.scroll_area = scroll_area
        
        plots_layout.addWidget(scroll_area)
        plots_container.setLayout(plots_layout)
        return plots_container

    def create_individual_plot_group(self, index, title):
        """Create single independent plot group using config"""
        config = self.config.DATA_TAB['plots_container']
        plot_group = QGroupBox(title)
        plot_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        plot_group.setMinimumSize(*config['plot_min_size'])
        
        plot_layout = QVBoxLayout()
        plot_layout.setContentsMargins(*config['plot_margins'])
        plot_layout.setSpacing(config['plot_spacing'])
        
        # Create top control button area
        control_layout = QHBoxLayout()
        control_layout.setSpacing(config['control_spacing'])
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(lambda checked, idx=index: self.refresh_plot(idx))
        refresh_btn.setMaximumWidth(config['button_max_width'])
        refresh_btn.setStyleSheet(self._get_button_style())
        
        # Export button
        export_btn = QPushButton("Export")
        export_btn.clicked.connect(lambda checked, idx=index: self.export_plot(idx))
        export_btn.setMaximumWidth(config['button_max_width'])
        export_btn.setStyleSheet(self._get_button_style())
        
        control_layout.addWidget(refresh_btn)
        control_layout.addWidget(export_btn)
        control_layout.addStretch()
        
        # Create matplotlib canvas
        canvas = MplCanvas()
        canvas.setMinimumSize(*config['canvas_min_size'])
        canvas.setMaximumSize(16777215, 16777215)
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        canvas.wheelEvent = self.canvas_wheel_event
        
        # Set fixed aspect ratio to 1:1 (square)
        canvas.setFixedAspectRatio(True)
        
        # Initialize axes
        canvas.ax.set_title(title)
        canvas.ax.text(0.5, 0.5, f'{title}\n(No Data)', 
                      ha='center', va='center', transform=canvas.ax.transAxes)
        canvas.ax.grid(True, alpha=0.3)
        canvas.ax.set_aspect('equal', adjustable='box')
        canvas.draw()
        
        self.canvases.append(canvas)
        
        # Add to plot group layout
        plot_layout.addLayout(control_layout)
        plot_layout.addWidget(canvas, 1)
        
        plot_group.setLayout(plot_layout)
        return plot_group

    def create_data_group(self):
        """Create data display group using data labels from entrance.py"""
        config = self.config.DATA_TAB['data_group']
        data_group = QGroupBox(config['title'])
        data_group.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        data_group.setMinimumWidth(config['min_width'])
        data_group.setMaximumWidth(config['max_width'])
        
        data_layout = QVBoxLayout()
        data_layout.setContentsMargins(*config['margins'])
        data_layout.setSpacing(config['spacing'])
        
        self.data_boxes = []
        
        for i, label_text in enumerate(self.data_display_labels):
            data_container = QVBoxLayout()
            data_container.setSpacing(config['container_spacing'])
            
            # Create label
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(f"""
                font-weight: {self.config.STYLES['label']['font_weight']};
                color: {self.config.STYLES['label']['color']};
                font-size: {self.config.STYLES['label']['font_size']['small']};
            """)
            label.setWordWrap(True)
            
            # Create data display box
            data_display = QLineEdit()
            data_display.setPlaceholderText("--")
            data_display.setMinimumHeight(config['display_min_height'])
            data_display.setMaximumHeight(config['display_max_height'])
            data_display.setReadOnly(True)
            data_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
            data_display.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            data_display.setStyleSheet(self._get_data_display_style())
            data_container.addWidget(label)
            data_container.addWidget(data_display)
            container_widget = QWidget()
            container_widget.setLayout(data_container)
            container_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            
            self.data_boxes.append(data_display)
            data_layout.addWidget(container_widget)
        
        # Add flexible space at bottom
        data_layout.addStretch()
        
        data_group.setLayout(data_layout)
        return data_group

    def _get_label_style(self):
        """Get label style from config"""
        style = self.config.STYLES['label']
        return f"""
            font-weight: {style['font_weight']};
            color: {style['color']};
            font-size: {style['font_size']['normal']};
        """

    def _get_combobox_style(self):
        """Get combobox style from config"""
        style = self.config.STYLES['combobox']
        return f"""
            QComboBox {{
                padding: {style['padding']};
                border: {style['border']};
                border-radius: {style['border_radius']};
                font-size: {style['font_size']};
                background-color: {style['background_color']};
            }}
            QComboBox:focus {{
                border: {style['focus_border']};
            }}
        """

    def _get_button_style(self):
        """Get button style from config"""
        style = self.config.STYLES['button']
        return f"""
            QPushButton {{
                background-color: {style['background_color']};
                border: {style['border']};
                border-radius: {style['border_radius']};
                padding: {style['padding']};
                font-size: {style['font_size']};
                font-weight: {style['font_weight']};
                color: {style['color']};
            }}
            QPushButton:hover {{
                background-color: {style['hover_bg']};
            }}
            QPushButton:pressed {{
                background-color: {style['pressed_bg']};
            }}
            QPushButton:disabled {{
                background-color: {style.get('disabled_bg', '#f8f8f8')};
                color: {style.get('disabled_color', '#999999')};
            }}
        """

    def _get_lineedit_style(self):
        """Get line edit style from config"""
        style = self.config.STYLES['lineedit']
        return f"""
            QLineEdit {{
                padding: {style['padding']};
                border: {style['border']};
                border-radius: {style['border_radius']};
                font-size: {style['font_size']};
            }}
            QLineEdit:focus {{
                border: {style['focus_border']};
            }}
        """

    def _get_data_display_style(self):
        """Get data display style from config"""
        style = self.config.STYLES['data_display']
        return f"""
            QLineEdit {{
                background-color: {style['background_color']};
                border: {style['border']};
                border-radius: {style['border_radius']};
                padding: {style['padding']};
                font-family: {style['font_family']};
                font-size: {style['font_size']};
                font-weight: {style['font_weight']};
                color: {style['color']};
            }}
            QLineEdit:read-only {{
                background-color: {style['readonly_bg']};
            }}
        """

    def _get_groupbox_style(self, style_name='default'):
        """Get group box style from config"""
        if not hasattr(self.config, 'GROUPBOX_STYLES'):
            # If no GROUPBOX_STYLES in config, return default style
            return """
                QGroupBox {
                    border: 2px solid #666666;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                    background-color: #ffffff;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                    color: #333333;
                    font-weight: bold;
                }
            """
        
        style = self.config.GROUPBOX_STYLES.get(style_name, self.config.GROUPBOX_STYLES['default'])
        return f"""
            QGroupBox {{
                border: {style['border']};
                border-radius: {style['border_radius']};
                margin-top: {style['margin_top']};
                padding-top: {style['padding_top']};
                background-color: {style['background_color']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: {style['title_color']};
                font-weight: {style['title_font_weight']};
            }}
        """

    def plot_dynamic_data(self, canvas, data, plot_index):
        """Plot data dynamically based on data structure from entrance.py"""
        canvas.ax.clear()
        
        # Check data type and plot accordingly
        if 'y1' in data and 'y2' in data:
            # Multi-line data
            canvas.ax.plot(data['x'], data['y1'], 'b-o', linewidth=2, markersize=4, label='Line 1')
            canvas.ax.plot(data['x'], data['y2'], 'r-s', linewidth=2, markersize=4, label='Line 2')
            canvas.ax.legend()
        else:
            # Single line data - use different colors and styles for different plots
            colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']
            markers = ['o', 's', '^', 'v', 'D', 'p', '*', 'h', '+', 'x']
            
            color = colors[plot_index % len(colors)]
            marker = markers[plot_index % len(markers)]
            
            if plot_index % 3 == 0:  # Line only
                canvas.ax.plot(data['x'], data['y'], color=color, linewidth=2)
            elif plot_index % 3 == 1:  # Line + markers
                canvas.ax.plot(data['x'], data['y'], color=color, marker=marker, 
                              linewidth=2, markersize=4)
            else:  # Markers only
                canvas.ax.scatter(data['x'], data['y'], color=color, marker=marker, s=30)
        
        canvas.ax.set_title(data['title'])
        canvas.ax.set_xlabel(data['xlabel'])
        canvas.ax.set_ylabel(data['ylabel'])
        canvas.ax.grid(True, alpha=0.3)
        canvas.ax.set_aspect('auto')
        canvas.draw()

    def update_all_plots(self, site, specimen):
        """Update all plots using data from entrance.py"""
        # Generate specimen data using test data generator
        specimen_data = self.test_data_generator.generate_specimen_data(site, specimen)
        
        # Use plot data keys generated from entrance.py
        for i in range(min(len(self.canvases), self.test_data_generator.num_plots)):
            canvas = self.canvases[i]
            plot_key = f'plot{i+1}'  # Use key format from entrance.py
            
            if plot_key in specimen_data:
                data = specimen_data[plot_key]
                self.plot_dynamic_data(canvas, data, i)

    def load_specimen_data(self, site, specimen):
        """Load specimen data using test data generator from entrance.py"""
        try:
            range_up = int(self.range_up_combo.currentText())
            range_down = int(self.range_down_combo.currentText())
        except ValueError:
            range_up = 100
            range_down = 1
        specimen_summary = self.test_data_generator.get_range_based_specimen_summary(
            site, specimen, range_up, range_down)
        for i, (key, value) in enumerate(specimen_summary.items()):
            if i < len(self.data_boxes):
                self.data_boxes[i].setText(value)
        self.update_all_plots(site, specimen)

    def load_specimen_plots(self, site, specimen):
        """Load specimen plots using full range data (not affected by range selection)"""
        if not hasattr(self, 'test_data_generator'):
            return
        
        try:
            specimen_data = self.test_data_generator.generate_specimen_data_full_range(site, specimen)
            
            for canvas in self.canvases:
                canvas.ax.clear()
            
            # Generate plots for each canvas
            for i, canvas in enumerate(self.canvases):
                if i >= self.test_data_generator.num_plots:
                    # Clear extra canvases
                    canvas.ax.clear()
                    canvas.ax.set_title(f'Plot {i+1} - No Data')
                    canvas.draw()
                    continue
                
                plot_key = f'plot{i+1}'
                if plot_key in specimen_data:
                    plot_data = specimen_data[plot_key]
                    
                    self.plot_dynamic_data(canvas, plot_data, i)
                else:
                    canvas.ax.clear()
                    canvas.ax.set_title(f'Plot {i+1} - No Data')
                    canvas.draw()
                
        except Exception as e:
            for canvas in self.canvases:
                canvas.ax.clear()
                canvas.ax.set_title('Error Loading Plot')
                canvas.ax.text(0.5, 0.5, f'Error: {str(e)}', 
                              ha='center', va='center', transform=canvas.ax.transAxes)
                canvas.draw()

    def load_specimen_data_boxes(self, site, specimen):
        """Load specimen data boxes using range-affected data"""
        if not hasattr(self, 'test_data_generator'):
            return
    
        try:
            # Get current range settings
            range_up = int(self.range_up_combo.currentText())
            range_down = int(self.range_down_combo.currentText())
        except (ValueError, AttributeError):
            range_up = 100
            range_down = 1
    
        try:
            # Use range-affected data to fill data boxes
            specimen_summary = self.test_data_generator.get_range_based_specimen_summary(
                site, specimen, range_up, range_down)
            
            # Update data boxes with range-affected values
            for i, data_box in enumerate(self.data_boxes):
                if i < len(self.test_data_generator.data_display_labels):
                    label = self.test_data_generator.data_display_labels[i]
                    value = specimen_summary.get(label, 'N/A')
                    data_box.setText(str(value))
                else:
                    data_box.setText('N/A')
                
        except Exception as e:
            # Handle errors gracefully
            for data_box in self.data_boxes:
                data_box.setText('Error')

    def get_axes(self, index):
        """Get axes object of specified index"""
        if 0 <= index < len(self.canvases):
            return self.canvases[index].ax
        else:
            raise IndexError(f"Plot index {index} out of range. Available plots: 0-{len(self.canvases)-1}")

    def export_plot(self, index):
        """Export specified plot"""
        if 0 <= index < len(self.canvases):
            from PySide6.QtWidgets import QFileDialog
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                f"Export Plot {index + 1}",
                f"plot_{index + 1}.png",
                "PNG Files (*.png);;PDF Files (*.pdf);;SVG Files (*.svg);;All Files (*)"
            )
            
            if file_path:
                try:
                    canvas = self.canvases[index]
                    canvas.fig.savefig(file_path, dpi=300, bbox_inches='tight')
                except Exception as e:
                    print(f"Error exporting plot {index + 1}: {e}")

    def refresh_plot(self, index):
        """Refresh specified plot"""
        if 0 <= index < len(self.canvases):
            current_site = self.site_combo.currentText()
            current_specimen = self.specimen_combo.currentText()
            
            if (current_site != "Select a site..." and 
                current_specimen != "Select a specimen..."):
                # Regenerate data and update single plot
                specimen_data = self.test_data_generator.generate_specimen_data(current_site, current_specimen)
                canvas = self.canvases[index]
                plot_key = f'plot{index+1}'
                
                if plot_key in specimen_data:
                    data = specimen_data[plot_key]
                    self.plot_dynamic_data(canvas, data, index)

    def clear_plot(self, index):
        """Clear specified plot"""
        if 0 <= index < len(self.canvases):
            canvas = self.canvases[index]
            canvas.ax.clear()
            canvas.ax.grid(True, alpha=0.3)
            canvas.ax.set_title(self.plot_titles[index])
            canvas.ax.text(0.5, 0.5, f'{self.plot_titles[index]}\n(No Data)', 
                          ha='center', va='center', transform=canvas.ax.transAxes)
            canvas.draw()

    def scroll_area_wheel_event(self, event):
        """Handle scroll area mouse wheel event"""
        self.handle_wheel_event(event)

    def canvas_wheel_event(self, event):
        """Handle canvas mouse wheel event"""
        self.handle_wheel_event(event)

    def handle_wheel_event(self, event):
        """Unified wheel event handling"""
        v_scrollbar = self.scroll_area.verticalScrollBar()
        h_scrollbar = self.scroll_area.horizontalScrollBar()
        
        modifiers = event.modifiers()
        
        if modifiers == Qt.KeyboardModifier.ShiftModifier:
            delta = event.angleDelta().y()
            h_scrollbar.setValue(h_scrollbar.value() - delta // 8)
        elif modifiers == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            v_scrollbar.setValue(v_scrollbar.value() - delta // 2)
        else:
            delta = event.angleDelta().y()
            v_scrollbar.setValue(v_scrollbar.value() - delta // 8)
        
        event.accept()

    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Previous - left arrow and up arrow
        self.prev_shortcut_left = QShortcut(QKeySequence(Qt.Key.Key_Left), self)
        self.prev_shortcut_left.activated.connect(self.navigate_previous)
        
        self.prev_shortcut_up = QShortcut(QKeySequence(Qt.Key.Key_Up), self)
        self.prev_shortcut_up.activated.connect(self.navigate_previous)
        
        # Next - right arrow and down arrow
        self.next_shortcut_right = QShortcut(QKeySequence(Qt.Key.Key_Right), self)
        self.next_shortcut_right.activated.connect(self.navigate_next)
        
        self.next_shortcut_down = QShortcut(QKeySequence(Qt.Key.Key_Down), self)
        self.next_shortcut_down.activated.connect(self.navigate_next)

    def setup_connections(self):
        """Setup signal connections with improved error handling"""
        if not hasattr(self, '_connections_established'):
            self._connections_established = False
    
        if self._connections_established:
            return  
        
        import warnings
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning, 
                                  message="Failed to disconnect.*from signal")
            if hasattr(self, 'site_combo') and self.site_combo:
                self.site_combo.currentTextChanged.connect(self.on_site_changed)
            
            if hasattr(self, 'specimen_combo') and self.specimen_combo:
                self.specimen_combo.currentTextChanged.connect(self.on_specimen_changed)
            
            if hasattr(self, 'range_up_combo') and self.range_up_combo:
                self.range_up_combo.currentTextChanged.connect(self.on_range_up_changed)
            
            if hasattr(self, 'range_down_combo') and self.range_down_combo:
                self.range_down_combo.currentTextChanged.connect(self.on_range_down_changed)
        self._connections_established = True

    def on_site_changed(self, site_name):
        """Handle site selection change"""
        # Clear current specimen selection
        self.specimen_combo.clear()
        self.specimen_combo.addItem("Select a specimen...")
        
        if site_name != "Select a site..." and hasattr(self, 'test_data_generator'):
            if site_name in self.test_data_generator.sites:
                # Populate specimens for this site
                specimens = self.test_data_generator.sites[site_name]
                for specimen in specimens:
                    self.specimen_combo.addItem(specimen)
                
                # Enable specimen dropdown
                self.specimen_combo.setEnabled(True)
            else:
                self.specimen_combo.setEnabled(False)
        else:
            self.specimen_combo.setEnabled(False)
        
        # Clear data display and plots - but don't trigger any loading
        self.clear_data_display()
        self.clear_all_plots()
        self.update_navigation_buttons()

    # def on_specimen_changed(self, specimen_name):
    #     """Handle specimen selection change"""
    #     current_site = self.site_combo.currentText()
        
    #     # Only load data when user explicitly selects a valid specimen
    #     if (specimen_name != "Select a specimen..." and 
    #         current_site != "Select a site..." and
    #         specimen_name and current_site):
    #         self.load_specimen_data(current_site, specimen_name)
    #     else:
    #         # Clear data display, but don't trigger traversal
    #         self.clear_data_display()
    #         self.clear_all_plots()
        
    #     self.update_navigation_buttons()

    def reset_controls(self):
        """Reset control states"""
        self.site_combo.clear()
        self.site_combo.addItem("Select a site...")
        for site in self.sample_data.keys():
            self.site_combo.addItem(site)
        self.site_combo.setEnabled(True)
        
        self.specimen_combo.clear()
        self.specimen_combo.addItem("Select a specimen...")
        self.specimen_combo.setEnabled(False)

    def populate_site_list(self):
        """Populate site list"""
        if hasattr(self, 'test_data_generator') and self.test_data_generator:
            sites = list(self.test_data_generator.sites.keys())
            
            # Clear existing items
            self.site_combo.clear()
            
            # Add default option
            self.site_combo.addItem("Select a site...")
            
            # Add sites
            for site in sites:
                self.site_combo.addItem(site)
            
            # Ensure dropdown is available
            self.site_combo.setEnabled(True)

    def populate_specimen_list(self, site):
        """Populate specimen list"""
        if not hasattr(self, 'test_data_generator') or not self.test_data_generator:
            return
            
        # Clear existing items
        self.specimen_combo.clear()
        
        if site == "Select a site..." or site not in self.test_data_generator.sites:
            self.specimen_combo.addItem("Select a specimen...")
            self.specimen_combo.setEnabled(False)
            return
        
        # Add default option
        self.specimen_combo.addItem("Select a specimen...")
        
        # Add all specimens for this site
        specimens = self.test_data_generator.sites[site]
        for specimen in specimens:
            self.specimen_combo.addItem(specimen)
        
        # Enable dropdown
        self.specimen_combo.setEnabled(True)

    def populate_range_lists(self):
        """Populate Range Tab dropdown lists"""
        if not hasattr(self, 'range_up_combo') or not hasattr(self, 'range_down_combo'):
            return
        
        # Clear existing items
        self.range_up_combo.clear()
        self.range_down_combo.clear()
        
        # Populate range values (from config)
        range_config = self.config.RANGE_VALUES
        min_val = range_config['min']
        max_val = range_config['max']
        
        # Populate upper limit dropdown (from high to low)
        for i in range(max_val, min_val - 1, -1):
            self.range_up_combo.addItem(str(i))
        
        # Populate lower limit dropdown (from low to high)
        for i in range(min_val, max_val + 1):
            self.range_down_combo.addItem(str(i))
        
        # Set default values
        self.range_up_combo.setCurrentText(str(range_config['default_up']))
        self.range_down_combo.setCurrentText(str(range_config['default_down']))
        
        # Ensure dropdowns are available
        self.range_up_combo.setEnabled(True)
        self.range_down_combo.setEnabled(True)

    def navigate_previous(self):
        """Navigate to previous specimen"""
        current_site = self.site_combo.currentText()
        current_specimen = self.specimen_combo.currentText()
        
        if not current_site or current_site == "Select a site...":
            return
        
        if current_site in self.sample_data and current_specimen in self.sample_data[current_site]:
            specimens = self.sample_data[current_site]
            current_specimen_index = specimens.index(current_specimen)
            
            if current_specimen_index > 0:
                self.specimen_combo.setCurrentText(specimens[current_specimen_index - 1])
            else:
                sites = list(self.sample_data.keys())
                current_site_index = sites.index(current_site)
                
                if current_site_index > 0:
                    previous_site = sites[current_site_index - 1]
                    self.site_combo.setCurrentText(previous_site)
                    
                    if previous_site in self.sample_data and self.sample_data[previous_site]:
                        last_specimen = self.sample_data[previous_site][-1]
                        self.specimen_combo.setCurrentText(last_specimen)

    def navigate_next(self):
        """Navigate to next specimen"""
        current_site = self.site_combo.currentText()
        current_specimen = self.specimen_combo.currentText()
        
        if not current_site or current_site == "Select a site...":
            return
        
        if current_site in self.sample_data and current_specimen in self.sample_data[current_site]:
            specimens = self.sample_data[current_site]
            current_specimen_index = specimens.index(current_specimen)
            
            if current_specimen_index < len(specimens) - 1:
                self.specimen_combo.setCurrentText(specimens[current_specimen_index + 1])
            else:
                sites = list(self.sample_data.keys())
                current_site_index = sites.index(current_site)
                
                if current_site_index < len(sites) - 1:
                    next_site = sites[current_site_index + 1]
                    self.site_combo.setCurrentText(next_site)
                    
                    if next_site in self.sample_data and self.sample_data[next_site]:
                        first_specimen = self.sample_data[next_site][0]
                        self.specimen_combo.setCurrentText(first_specimen)

    def update_navigation_buttons(self):
        """Update navigation button states"""
        if not hasattr(self, 'prev_btn') or not hasattr(self, 'next_btn'):
            return
        
        current_site = self.site_combo.currentText()
        current_specimen = self.specimen_combo.currentText()
        
        if (current_site == "Select a site..." or 
            current_specimen == "Select a specimen..."):
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
            return
        
        can_go_prev = False
        can_go_next = False
        
        if current_site in self.sample_data:
            specimens = self.sample_data[current_site]
            sites = list(self.sample_data.keys())
            
            try:
                current_specimen_index = specimens.index(current_specimen)
                current_site_index = sites.index(current_site)
                
                if current_specimen_index > 0 or current_site_index > 0:
                    can_go_prev = True
                
                if current_specimen_index < len(specimens) - 1 or current_site_index < len(sites) - 1:
                    can_go_next = True
                    
            except (ValueError, IndexError):
                pass
        
        self.prev_btn.setEnabled(can_go_prev)
        self.next_btn.setEnabled(can_go_next)

    def clear_data_display(self):
        """Clear data display boxes"""
        for data_box in self.data_boxes:
            data_box.setText("")

    def go_to_previous_specimen(self):
        """Jump to previous specimen"""
        self.navigate_previous()

    def go_to_next_specimen(self):
        """Jump to next specimen"""
        self.navigate_next()

    def clear_all_plots(self):
        """Clear all plots"""
        if hasattr(self, 'canvases'):
            for i, canvas in enumerate(self.canvases):
                if i < len(self.plot_titles):
                    canvas.ax.clear()
                    canvas.ax.set_title(self.plot_titles[i])
                    canvas.ax.text(0.5, 0.5, f'{self.plot_titles[i]}\n(No Data)', 
                                  ha='center', va='center', transform=canvas.ax.transAxes)
                    canvas.ax.grid(True, alpha=0.3)
                    canvas.draw()

    def on_range_up_changed(self, value):
        """Handle range up selection change"""
        self.on_range_changed()

    def on_range_down_changed(self, value):
        """Handle range down selection change"""
        self.on_range_changed()

    def on_range_changed(self):
        """Handle range change - only update data boxes, not plots"""
        current_site = self.site_combo.currentText()
        current_specimen = self.specimen_combo.currentText()
        
        # Only update data boxes when both site and specimen are selected
        if (current_site != "Select a site..." and 
            current_specimen != "Select a specimen..." and
            current_site and current_specimen):
            
            # Only update data boxes (affected by range), not the plots
            self.load_specimen_data_boxes(current_site, current_specimen)
            
            # Apply filter colors if callback exists
            if hasattr(self, 'apply_filter_colors_callback'):
                self.apply_filter_colors_callback(current_site, current_specimen)

    def on_specimen_changed(self, specimen):
        """Handle specimen selection change"""
        if not specimen or specimen == "Select a specimen...":
            return
            
        current_site = self.site_combo.currentText()
        if current_site and current_site != "Select a site...":
            self.load_specimen_data_complete(current_site, specimen)

    def on_site_changed(self, site):
        """Handle site selection change"""
        if not site or site == "Select a site...":
            return
            
        # Update specimen combo for the selected site
        self.update_specimen_combo(site)
        
        # If there's a current specimen selection, load its data
        current_specimen = self.specimen_combo.currentText()
        if current_specimen and current_specimen != "Select a specimen...":
            self.load_specimen_data_complete(site, current_specimen)

    def load_specimen_data_complete(self, site, specimen):
        """Load complete specimen data - plots (full range) and data boxes (range-affected)"""
        if not site or not specimen or site == "Select a site..." or specimen == "Select a specimen...":
            return
        
        self.load_specimen_plots(site, specimen)
        
        self.load_specimen_data_boxes(site, specimen)
        
        self.apply_independent_parameter_colors(site, specimen)

    def update_specimen_combo(self, site):
        """Update specimen combo box based on selected site"""
        if not hasattr(self, 'test_data_generator') or not self.test_data_generator:
            return
        
        # Clear existing items
        self.specimen_combo.clear()
        
        if site == "Select a site..." or site not in self.test_data_generator.sites:
            self.specimen_combo.addItem("Select a specimen...")
            self.specimen_combo.setEnabled(False)
            return
        
        # Add default option
        self.specimen_combo.addItem("Select a specimen...")
        
        # Add all specimens for this site
        specimens = self.test_data_generator.sites[site]
        for specimen in specimens:
            self.specimen_combo.addItem(specimen)
        
        # Enable dropdown
        self.specimen_combo.setEnabled(True)

    def setup_filter_input_callbacks(self):
        """Setup independent callbacks for each filter input"""
        if not hasattr(self, 'filter_inputs'):
            return
        
        for i, filter_input in enumerate(self.filter_inputs):
            # Use lambda with default parameter to capture the current index
            filter_input.textChanged.connect(
                lambda text, index=i: self.on_individual_filter_changed(index, text)
            )
            
            # Also connect to editingFinished for when user stops typing
            filter_input.editingFinished.connect(
                lambda index=i: self.on_filter_editing_finished(index)
            )

    def on_individual_filter_changed(self, parameter_index, condition_text):
        """Handle individual filter input changes"""
        # Only update the color for this specific parameter
        current_site = self.site_combo.currentText()
        current_specimen = self.specimen_combo.currentText()
        
        if (current_site != "Select a site..." and 
            current_specimen != "Select a specimen..." and
            current_site and current_specimen):
            
            # Update color for this specific parameter only
            self.update_single_parameter_color(current_site, current_specimen, parameter_index, condition_text)

    def on_filter_editing_finished(self, parameter_index):
        """Handle when user finishes editing a filter input"""
        # Confirm the condition for this parameter
        current_site = self.site_combo.currentText()
        current_specimen = self.specimen_combo.currentText()
        
        if (current_site != "Select a site..." and 
            current_specimen != "Select a specimen..." and
            current_site and current_specimen):
            
            if parameter_index < len(self.filter_inputs):
                filter_input = self.filter_inputs[parameter_index]
                condition_text = filter_input.text().strip()
                
                # Store as confirmed condition
                filter_input._last_confirmed_condition = condition_text
                
                # Update color for this parameter
                self.update_single_parameter_color(current_site, current_specimen, parameter_index, condition_text)

    def update_single_parameter_color(self, site, specimen, parameter_index, condition_str):
        """Update color for a single parameter independently"""
        if not hasattr(self, 'test_data_generator'):
            return
        
        test_data = self.test_data_generator
        
        # Validate parameter index
        if parameter_index >= len(self.data_boxes) or parameter_index >= len(test_data.parameter_labels):
            return
        
        # Get current range settings
        try:
            range_up = int(self.range_up_combo.currentText())
            range_down = int(self.range_down_combo.currentText())
        except (ValueError, AttributeError):
            range_up = 100
            range_down = 1
        
        # Check this specific parameter condition independently
        param_match = test_data.check_parameter_condition_independently(
            site, specimen, parameter_index, condition_str, range_up, range_down
        )
        
        # Get the corresponding data box
        data_box = self.data_boxes[parameter_index]
        
        # Apply color based on this parameter's condition only
        if not condition_str or not condition_str.strip():
            # No condition - default style
            data_box.setStyleSheet("QLineEdit { background-color: white; color: black; }")
        elif param_match:
            # This parameter's condition is met - green
            data_box.setStyleSheet("QLineEdit { background-color: lightgreen; color: black; }")
        else:
            # This parameter's condition is not met - red
            data_box.setStyleSheet("QLineEdit { background-color: lightcoral; color: black; }")

    def apply_independent_parameter_colors(self, site, specimen):
        """Apply colors to data boxes based on independent parameter conditions"""
        if not hasattr(self, 'test_data_generator'):
            return
    
        test_data = self.test_data_generator
    
        # Get current range settings
        try:
            range_up = int(self.range_up_combo.currentText())
            range_down = int(self.range_down_combo.currentText())
        except (ValueError, AttributeError):
            range_up = 100
            range_down = 1
        from config import LayoutConfig
        filter_colors = LayoutConfig.STYLES['filter_colors']
    
        # Apply colors to each data box independently
        for i, data_box in enumerate(self.data_boxes):
            if i < len(test_data.parameter_labels) and i < len(self.filter_inputs):
                condition_str = self.filter_inputs[i].text().strip()
                
                # Check this specific parameter condition independently
                param_match = test_data.check_parameter_condition_independently(
                    site, specimen, i, condition_str, range_up, range_down
                )
                
                if not condition_str or not condition_str.strip():
                    # No condition - 
                    data_box.setStyleSheet(f"""
                        QLineEdit {{
                            background-color: {filter_colors['default_background']};
                            color: {filter_colors['default_text']};
                            border: 1px solid #cccccc;
                            border-radius: 3px;
                            padding: 4px;
                            font-size: 9pt;
                        }}
                    """)
                elif param_match:
                   
                    data_box.setStyleSheet(f"""
                        QLineEdit {{
                            background-color: {filter_colors['match_background']};
                            color: {filter_colors['match_text']};
                            border: {filter_colors['match_border']};
                            border-radius: 3px;
                            padding: 4px;
                            font-size: 9pt;
                            font-weight: bold;
                        }}
                    """)
                else:
                    data_box.setStyleSheet(f"""
                        QLineEdit {{
                            background-color: {filter_colors['no_match_background']};
                            color: {filter_colors['no_match_text']};
                            border: {filter_colors['no_match_border']};
                            border-radius: 3px;
                            padding: 4px;
                            font-size: 9pt;
                            font-weight: bold;
                        }}
                    """)
            else:
                
                data_box.setStyleSheet(f"""
                    QLineEdit {{
                        background-color: {filter_colors['default_background']};
                        color: {filter_colors['default_text']};
                        border: 1px solid #cccccc;
                        border-radius: 3px;
                        padding: 4px;
                        font-size: 9pt;
                    }}
                """)

