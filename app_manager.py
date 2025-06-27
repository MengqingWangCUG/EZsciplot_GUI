from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QLabel, QLineEdit, QComboBox, QPushButton, QSizePolicy,
    QScrollArea, QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from entrance import TestData
from mpl_canvas import MplCanvas


class TestAppManager:   
    def create_test_application(self, num_plots=6, num_params=5, custom_param_labels=None):
        """Create test application
        
        Args:
            num_plots (int): Number of plots
            num_params (int): Number of parameters
            custom_param_labels (list): Custom parameter labels
            
        Returns:
            MainWindow: Configured main window instance
        """
        # Import MainWindow here to avoid circular import
        from main_window import MainWindow
        
        # Create main window
        window = MainWindow()
        
        # Create test data
        test_data = TestData(num_plots=num_plots, num_params=num_params, custom_param_labels=custom_param_labels)
        
        # Inject test data into DataTab
        window.data_tab.sample_data = test_data.sites
        window.data_tab.test_data_generator = test_data
        
        # Update DataTab labels to match new quantities
        window.data_tab.plot_titles = test_data.plot_titles
        window.data_tab.parameter_labels = test_data.parameter_labels
        window.data_tab.data_display_labels = test_data.data_display_labels
        
        # Recreate plots container to accommodate new number of plots
        self._recreate_plots_container(window, num_plots)
        
        # Recreate top layout to accommodate new number of parameters
        self._recreate_top_layout(window, num_params)
        
        # Setup test functionality
        self._setup_test_functionality(window, test_data, num_plots)
        
        # Ensure dropdowns are properly initialized
        if hasattr(window.data_tab, 'populate_range_lists'):
            window.data_tab.populate_range_lists()
        
        if hasattr(window.data_tab, 'setup_connections'):
            window.data_tab.setup_connections()
        
        # Enable sample selection
        window.data_tab.populate_site_list()
        
        return window

    # 修复 app_manager.py 中的 _setup_test_functionality 方法
    def _setup_test_functionality(self, window, test_data, num_plots):
        """Setup test functionality"""
        
        # 存储每个参数的最后确认状态
        def initialize_parameter_states():
            """Initialize parameter confirmed states"""
            if not hasattr(window.data_tab, '_parameter_confirmed_states'):
                window.data_tab._parameter_confirmed_states = {}
                for i in range(len(window.data_tab.filter_inputs)):
                    if i < len(test_data.parameter_labels):
                        param_label = test_data.parameter_labels[i]
                        window.data_tab._parameter_confirmed_states[param_label] = ""
        
        def apply_filter_colors_and_text_colors_independent(site, specimen):
            """Apply filter colors independently for each parameter"""
            try:
                from config import LayoutConfig
                
                # Get current Range settings
                try:
                    range_up = int(window.data_tab.range_up_combo.currentText())
                    range_down = int(window.data_tab.range_down_combo.currentText())
                except (ValueError, AttributeError):
                    range_up = 100
                    range_down = 1
                
                # Use filter color styles from config
                filter_colors = LayoutConfig.STYLES['filter_colors']
                
                # Apply colors to each data box independently
                for i, data_box in enumerate(window.data_tab.data_boxes):
                    if i < len(test_data.parameter_labels) and i < len(window.data_tab.filter_inputs):
                        filter_input = window.data_tab.filter_inputs[i]
                        condition_str = filter_input.text().strip()

                        param_match = test_data.check_parameter_condition_independently(
                            site, specimen, i, condition_str, range_up, range_down
                        )

                        if not condition_str or not condition_str.strip():
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
                
                # 强制UI刷新
                for data_box in window.data_tab.data_boxes:
                    data_box.update()
                    data_box.repaint()
                
            except Exception as e:
                print(f"Error applying filter colors: {e}")
        
        def update_single_parameter_color(parameter_index, condition_str):
            """Update color for a single parameter only"""
            try:
                current_site = window.data_tab.site_combo.currentText()
                current_specimen = window.data_tab.specimen_combo.currentText()
                
                if (current_site == "Select a site..." or 
                    current_specimen == "Select a specimen..." or
                    not current_site or not current_specimen):
                    return
                
                if (parameter_index >= len(window.data_tab.data_boxes) or 
                    parameter_index >= len(test_data.parameter_labels)):
                    return
                
                from config import LayoutConfig
                filter_colors = LayoutConfig.STYLES['filter_colors']
                
                # Get current Range settings
                try:
                    range_up = int(window.data_tab.range_up_combo.currentText())
                    range_down = int(window.data_tab.range_down_combo.currentText())
                except (ValueError, AttributeError):
                    range_up = 100
                    range_down = 1
                
                param_match = test_data.check_parameter_condition_independently(
                    current_site, current_specimen, parameter_index, condition_str, range_up, range_down
                )
                
                data_box = window.data_tab.data_boxes[parameter_index]
                
                if not condition_str or not condition_str.strip():
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
                
                data_box.update()
                data_box.repaint()
                
            except Exception as e:
                print(f"Error updating single parameter color: {e}")
        
        # Define load_test_specimen_data that uses apply_filter_colors_and_text_colors
        def load_test_specimen_data(site, specimen):
            """Load test specimen data"""
            print(f"Loading test data for {site} - {specimen}")
            
            # Get current Range settings
            try:
                range_up = int(window.data_tab.range_up_combo.currentText())
                range_down = int(window.data_tab.range_down_combo.currentText())
            except (ValueError, AttributeError):
                range_up = 100
                range_down = 1
    
            # Generate test data
            specimen_data = test_data.generate_specimen_data(site, specimen)
            
            # Use Range-based specimen summary calculation
            specimen_summary = test_data.get_range_based_specimen_summary(site, specimen, range_up, range_down)
            
            # Update data display box content
            for i, (key, value) in enumerate(specimen_summary.items()):
                if i < len(window.data_tab.data_boxes):
                    data_box = window.data_tab.data_boxes[i]
                    data_box.setText(value)
                    # Temporarily use default style, colors will be set later
                    data_box.setStyleSheet("QLineEdit { background-color: white; color: black; }")
    
            # Update plots
            window.data_tab.update_all_plots(site, specimen)
    
            # Apply filter condition color effects immediately after data loading
            apply_filter_colors_and_text_colors_independent(site, specimen)

        # Define on_range_changed function at the top level
        def on_range_changed():
            """Handle range changes"""
            current_site = window.data_tab.site_combo.currentText()
            current_specimen = window.data_tab.specimen_combo.currentText()
            
            if (current_site != "Select a site..." and 
                current_specimen != "Select a specimen..." and
                current_site and current_specimen):
                try:
                    range_up = int(window.data_tab.range_up_combo.currentText())
                    range_down = int(window.data_tab.range_down_combo.currentText())
                except ValueError:
                    range_up = 100
                    range_down = 1
                    
                specimen_summary = test_data.get_range_based_specimen_summary(
                    current_site, current_specimen, range_up, range_down)
                    
                for i, (key, value) in enumerate(specimen_summary.items()):
                    if i < len(window.data_tab.data_boxes):
                        data_box = window.data_tab.data_boxes[i]
                        data_box.setText(value)
            apply_filter_colors_and_text_colors_independent(current_site, current_specimen)
        
        def setup_filter_listeners():
            """Setup filter condition input box listeners with independent parameter handling"""
            initialize_parameter_states()
            
            for i, input_field in enumerate(window.data_tab.filter_inputs):
                if i < len(test_data.parameter_labels):
                    param_label = test_data.parameter_labels[i]
                    
                    def create_parameter_handlers(parameter_index, parameter_label, input_widget):
                        def on_filter_editing_finished():
                            # 输入完成时更新这个参数的颜色
                            try:
                                current_text = input_widget.text().strip()
                                # 存储确认的状态
                                if hasattr(window.data_tab, '_parameter_confirmed_states'):
                                    window.data_tab._parameter_confirmed_states[parameter_label] = current_text
                                # 更新颜色
                                update_single_parameter_color(parameter_index, current_text)
                            except Exception as e:
                                print(f"Error in filter editing finished: {e}")
                        
                        def on_filter_text_changed(text):
                            # 文本变化时实时更新颜色（实现即时反馈）
                            try:
                                update_single_parameter_color(parameter_index, text.strip())
                            except Exception as e:
                                print(f"Error in filter text changed: {e}")
                        
                        return on_filter_editing_finished, on_filter_text_changed
                    
                    editing_finished_handler, text_changed_handler = create_parameter_handlers(i, param_label, input_field)
                    
                    input_field.textChanged.connect(text_changed_handler)
                    input_field.editingFinished.connect(editing_finished_handler)
    
        def setup_range_listeners():
            """Setup Range Tab control listeners"""
            # Use the on_range_changed function defined above
            if hasattr(window.data_tab, 'range_up_combo'):
                window.data_tab.range_up_combo.currentTextChanged.connect(on_range_changed)
            if hasattr(window.data_tab, 'range_down_combo'):
                window.data_tab.range_down_combo.currentTextChanged.connect(on_range_changed)
    
        # 设置回调
        window.data_tab.load_specimen_data = load_test_specimen_data
        window.data_tab.setup_connections()
        setup_filter_listeners()
        setup_range_listeners()

    def _plot_single_line(self, canvas, data, plot_index, colors, alpha):
        """Plot single line graph"""
        canvas.ax.clear()
        
        markers = ['o', 's', '^', 'v', 'D', 'p', '*', 'h', '+', 'x']
        
        color = colors[plot_index % len(colors)]
        marker = markers[plot_index % len(markers)]
        
        if plot_index % 3 == 0:  # Line only
            canvas.ax.plot(data['x'], data['y'], color=color, linewidth=2, alpha=alpha)
        elif plot_index % 3 == 1:  # Line + markers
            canvas.ax.plot(data['x'], data['y'], color=color, marker=marker, 
                          linewidth=2, markersize=4, alpha=alpha)
        else:  # Markers only
            canvas.ax.scatter(data['x'], data['y'], color=color, marker=marker, s=30, alpha=alpha)
        
        canvas.ax.set_title(data['title'])
        canvas.ax.set_xlabel(data['xlabel'])
        canvas.ax.set_ylabel(data['ylabel'])
        canvas.ax.grid(True, alpha=0.3)
        canvas.ax.set_aspect('auto')
        canvas.draw()
    
    def _plot_multi_line(self, canvas, data, colors, alpha):
        """Plot multi-line graph"""
        canvas.ax.clear()
        color1 = colors[0] if len(colors) > 0 else 'blue'
        color2 = colors[1] if len(colors) > 1 else 'red'
        
        canvas.ax.plot(data['x'], data['y1'], color=color1, linestyle='-', marker='o', 
                      linewidth=2, markersize=4, label='Line 1', alpha=alpha)
        canvas.ax.plot(data['x'], data['y2'], color=color2, linestyle='-', marker='s', 
                      linewidth=2, markersize=4, label='Line 2', alpha=alpha)
        canvas.ax.set_title(data['title'])
        canvas.ax.set_xlabel(data['xlabel'])
        canvas.ax.set_ylabel(data['ylabel'])
        canvas.ax.legend()
        canvas.ax.grid(True, alpha=0.3)
        canvas.ax.set_aspect('auto')
        canvas.draw()
    
    def _recreate_top_layout(self, window, num_params):
        """Recreate top layout to accommodate new number of parameters"""
        data_tab = window.data_tab
        new_filter_group = self._create_dynamic_filter_group(data_tab, num_params)
        new_data_group = self._create_dynamic_data_group(data_tab, num_params)
        layout_found = False
        for i in range(data_tab.layout().count()):
            item = data_tab.layout().itemAt(i)
            if item and hasattr(item, 'layout') and isinstance(item.layout(), QHBoxLayout):
                top_layout = item.layout()
                for j in range(top_layout.count()):
                    widget_item = top_layout.itemAt(j)
                    if widget_item and widget_item.widget() and isinstance(widget_item.widget(), QGroupBox):
                        if "Filter" in widget_item.widget().title():
                            old_filter_widget = widget_item.widget()
                            top_layout.removeWidget(old_filter_widget)
                            top_layout.insertWidget(j, new_filter_group)
                            old_filter_widget.setParent(None)
                            old_filter_widget.deleteLater()
                            layout_found = True
                            break
            
            if layout_found:
                break
        data_layout_found = False
        for i in range(data_tab.layout().count()):
            item = data_tab.layout().itemAt(i)
            if item and hasattr(item, 'layout') and isinstance(item.layout(), QHBoxLayout):
                middle_layout = item.layout()
                # Check if this layout contains data group
                for j in range(middle_layout.count()):
                    widget_item = middle_layout.itemAt(j)
                    if widget_item and widget_item.widget() and isinstance(widget_item.widget(), QGroupBox):
                        if "Data" in widget_item.widget().title() and "Specimen" in widget_item.widget().title():
                            old_data_widget = widget_item.widget()
                            middle_layout.removeWidget(old_data_widget)
                            middle_layout.insertWidget(j, new_data_group)
                            old_data_widget.setParent(None)
                            old_data_widget.deleteLater()
                            data_layout_found = True
                            break
            
            if data_layout_found:
                break
        data_tab.updateGeometry()
        data_tab.update()
    
    def _recreate_plots_container(self, window, num_plots):
        """Recreate plots container to accommodate new number of plots"""
        data_tab = window.data_tab
        config = data_tab.config.DATA_TAB['plots_container']
        
        # Find and remove original plots container
        for i in range(data_tab.layout().count()):
            item = data_tab.layout().itemAt(i)
            if item and hasattr(item, 'widget'):
                widget = item.widget()
                if hasattr(widget, 'layout') and widget.layout():
                    for j in range(widget.layout().count()):
                        sub_item = widget.layout().itemAt(j)
                        if sub_item and hasattr(sub_item, 'widget'):
                            sub_widget = sub_item.widget()
                            if isinstance(sub_widget, QGroupBox) and sub_widget.title() == config['title']:
                                # Found plots container, replace it
                                old_plots_container = sub_widget
                                new_plots_container = self._create_new_plots_container(data_tab, num_plots)
                                parent_layout = widget.layout()
                                index = parent_layout.indexOf(old_plots_container)
                                parent_layout.removeWidget(old_plots_container)
                                parent_layout.insertWidget(index, new_plots_container)
                                old_plots_container.setParent(None)
                                old_plots_container.deleteLater()
                                return
    
    def _create_dynamic_filter_group(self, data_tab, num_params):
        """Create dynamic number of filter group - supports adaptive labels"""
        config = data_tab.config.DATA_TAB['filter_group']
        
        filter_group = QGroupBox(config['title'])
        filter_group.setStyleSheet(data_tab._get_groupbox_style('filter_group'))
        filter_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # Clear old layout (if exists)
        if filter_group.layout():
            QWidget().setLayout(filter_group.layout())
        
        filter_layout = QGridLayout()
        filter_layout.setContentsMargins(*config['margins'])
        
        # Create new filter_inputs list
        data_tab.filter_inputs = []
        
        # Calculate available width
        cols_per_row = (num_params + 1) // 2
        
        # Create adaptive labels
        for i in range(num_params):
            label_text = data_tab.parameter_labels[i]
            
            # Calculate maximum label width for current parameter
            max_label_width = 80  # Base maximum width
            # Use adaptive label creation method
            if hasattr(data_tab, '_create_adaptive_label'):
                label = data_tab._create_adaptive_label(f"{label_text}:", max_label_width, 8)
            else:
                label = QLabel(f"{label_text}:")
                label.setStyleSheet(f"""
                    font-weight: {data_tab.config.STYLES['label']['font_weight']};
                    color: {data_tab.config.STYLES['label']['color']};
                    font-size: 8pt;  /* Use smaller font */
                    margin-right: 0px;
                    padding-right: 0px;
                """)
            
            label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            label.setMaximumWidth(max_label_width)
            label.setMinimumWidth(max_label_width)
            
            # Enable text ellipsis
            label.setWordWrap(False)
            label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            
            # Input box - use wider input box
            input_field = QLineEdit()
            input_field.setPlaceholderText(">10")  # Simplified placeholder
            input_field.setFixedWidth(config['input_width'] + 30)  # Increase width
            input_field.setStyleSheet(f"""
                {data_tab._get_lineedit_style()}
                margin-left: 0px;
                padding-left: 0px;
                font-size: 8pt;  /* Use smaller font */
            """)
            
            # Add tooltip
            input_field.setToolTip(
                f"Filter for {label_text}\n"
                "Operators: >, >=, <, <=, =, !=\n"
                "Example: >10, <=5.5, =100"
            )
            
            data_tab.filter_inputs.append(input_field)
            
            # Calculate row and column position
            row = i % 2
            col_pair = i // 2
            
            label_col = col_pair * 3
            input_col = col_pair * 3 + 1
            spacer_col = col_pair * 3 + 2
            
            # Add to layout
            filter_layout.addWidget(label, row, label_col)
            filter_layout.addWidget(input_field, row, input_col)
            
            # Set column width and stretch
            filter_layout.setColumnStretch(label_col, 0)
            filter_layout.setColumnMinimumWidth(label_col, max_label_width)
            filter_layout.setColumnStretch(input_col, 0)
            filter_layout.setColumnMinimumWidth(input_col, config['input_width'] + 30)
            
            if col_pair < cols_per_row - 1:
                filter_layout.setColumnStretch(spacer_col, 0)
                filter_layout.setColumnMinimumWidth(spacer_col, 15)
    
        filter_layout.setHorizontalSpacing(5)
        filter_layout.setVerticalSpacing(8)
        filter_group.setLayout(filter_layout)
        
        # Dynamically adjust group width
        total_width = cols_per_row * (max_label_width + config['input_width'] + 30 + 15) + 20
        filter_group.setMinimumWidth(total_width)
        filter_group.setMaximumWidth(total_width + 50)
        
        return filter_group
    
    def _create_dynamic_data_group(self, data_tab, num_params):
        """Create dynamic number of data display group"""
        config = data_tab.config.DATA_TAB['data_group']
        
        data_group = QGroupBox(config['title'])
        data_group.setStyleSheet(data_tab._get_groupbox_style('data_group'))
        data_group.setMinimumWidth(config['min_width'])
        data_group.setMaximumWidth(config['max_width'])
        data_group.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        data_layout = QVBoxLayout()
        data_layout.setContentsMargins(8, 8, 8, 8)
        data_layout.setSpacing(3)
        data_tab.data_boxes = []
        
        for i in range(num_params):
            label = QLabel(data_tab.data_display_labels[i])
            label.setStyleSheet(f"""
                font-weight: {data_tab.config.STYLES['label']['font_weight']};
                color: {data_tab.config.STYLES['label']['color']};
                font-size: {data_tab.config.STYLES['label']['font_size']['small']};
                padding: 2px;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 3px;
                margin: 0px;
            """)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFixedHeight(20)
            
            # Data display box
            data_display = QLineEdit()
            data_display.setReadOnly(True)
            data_display.setFixedHeight(35)
            data_display.setStyleSheet(f"""
                {data_tab._get_data_display_style()}
                margin: 0px;
                padding: 2px;
            """)
            data_display.setPlaceholderText("No data")
            
            data_tab.data_boxes.append(data_display)
            
            # Add to data layout
            data_layout.addWidget(label)
            data_layout.addWidget(data_display)
            
            # Only add small spacing between items
            if i < num_params - 1:
                data_layout.addSpacing(2)
    
        data_group.setLayout(data_layout)
        title_height = 25
        label_height = 20
        data_box_height = 35
        spacing_between_items = 2
        layout_margins = 16
        layout_spacing = 3       
        height_per_param = label_height + layout_spacing + data_box_height + spacing_between_items
        total_height = title_height + layout_margins + (height_per_param * num_params) - spacing_between_items
        data_group.setFixedHeight(total_height)
        
        return data_group
    
    def _create_new_plots_container(self, data_tab, num_plots):
        """Create new plots container"""
        config = data_tab.config.DATA_TAB['plots_container']
        # Create new plots container
        plots_container = QGroupBox(config['title'])
        plots_container.setStyleSheet(data_tab._get_groupbox_style('plots_container'))
        plots_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        plots_layout = QVBoxLayout()
        plots_layout.setContentsMargins(*config['margins'])
        plots_layout.setSpacing(config['spacing'])

        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scroll_area.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        scroll_area.wheelEvent = data_tab.scroll_area_wheel_event

        # Create scroll content widget
        scroll_content = QWidget()
        scroll_content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scroll_content.wheelEvent = data_tab.scroll_area_wheel_event
        
        # Create grid layout, maintain 2 columns n rows format
        main_grid_layout = QGridLayout(scroll_content)
        main_grid_layout.setSpacing(config['grid_spacing'])
        main_grid_layout.setContentsMargins(*config['scroll_margins'])
        data_tab.plot_groups = []
        data_tab.canvases = []
        for i in range(num_plots):
            plot_group = self._create_individual_plot_group(data_tab, i, data_tab.plot_titles[i])
            data_tab.plot_groups.append(plot_group)
            
            # Calculate row and column position (2 columns, n rows)
            row = i // 2
            col = i % 2
            main_grid_layout.addWidget(plot_group, row, col)
            # Set row and column stretch factors
            main_grid_layout.setRowStretch(row, 1)
            main_grid_layout.setColumnStretch(col, 1)
        # Set scroll content
        scroll_area.setWidget(scroll_content)
        data_tab.scroll_area = scroll_area
        plots_layout.addWidget(scroll_area)
        plots_container.setLayout(plots_layout)
        return plots_container
    
    def _create_individual_plot_group(self, data_tab, index, title):
        """Create individual independent plot group"""
        config = data_tab.config.DATA_TAB['plots_container']
        plot_group = QGroupBox(title)
        plot_group.setStyleSheet(data_tab._get_groupbox_style('individual_plot'))
        plot_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        plot_group.setMinimumSize(*config['plot_min_size'])
        plot_layout = QVBoxLayout()
        plot_layout.setContentsMargins(*config['plot_margins'])
        plot_layout.setSpacing(config['plot_spacing'])
        control_layout = QHBoxLayout()
        control_layout.setSpacing(config['control_spacing'])
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(lambda checked, idx=index: data_tab.refresh_plot(idx))
        refresh_btn.setMaximumWidth(config['button_max_width'])
        refresh_btn.setStyleSheet(data_tab._get_button_style())
        
        # Export button
        export_btn = QPushButton("Export")
        export_btn.clicked.connect(lambda checked, idx=index: data_tab.export_plot(idx))
        export_btn.setMaximumWidth(config['button_max_width'])
        export_btn.setStyleSheet(data_tab._get_button_style())
        
        control_layout.addWidget(refresh_btn)
        control_layout.addWidget(export_btn)
        control_layout.addStretch()
        canvas = MplCanvas()
        canvas.setMinimumSize(*config['canvas_min_size'])
        canvas.setMaximumSize(16777215, 16777215)
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        canvas.wheelEvent = data_tab.canvas_wheel_event
        
        # Set fixed aspect ratio to 1:1 (square)
        canvas.setFixedAspectRatio(True)
        canvas.ax.set_title(title)
        canvas.ax.text(0.5, 0.5, f'{title}\n(No Data)', 
                      ha='center', va='center', transform=canvas.ax.transAxes)
        canvas.ax.grid(True, alpha=0.3)
        canvas.ax.set_aspect('equal', adjustable='box')
        canvas.draw()
        data_tab.canvases.append(canvas)

        plot_layout.addLayout(control_layout)
        plot_layout.addWidget(canvas, 1)
        plot_group.setLayout(plot_layout)
        return plot_group
    def setup_data_tab_callbacks(self, window):
        """Setup data tab callbacks"""
        window.data_tab.load_specimen_data = window.data_tab.load_specimen_data_complete
        window.data_tab.apply_filter_colors_callback = lambda site, specimen: self.apply_filter_colors_and_text_colors(window, site, specimen)

        # window.data_tab.apply_filter_colors_callback = lambda site, specimen: window.data_tab.apply_independent_parameter_colors(site, specimen)

    def apply_filter_colors_and_text_colors(self, window, site, specimen):
        """Apply filter colors and text colors to data boxes based on independent parameter conditions"""
        if not hasattr(window.data_tab, 'test_data_generator'):
            return
        
        test_data = window.data_tab.test_data_generator
        
        # Get current range settings
        try:
            range_up = int(window.data_tab.range_up_combo.currentText())
            range_down = int(window.data_tab.range_down_combo.currentText())
        except (ValueError, AttributeError):
            range_up = 100
            range_down = 1
        from config import LayoutConfig
        filter_colors = LayoutConfig.STYLES['filter_colors']
    
        # Apply colors to each data box independently
        for i, data_box in enumerate(window.data_tab.data_boxes):
            if i < len(test_data.parameter_labels) and i < len(window.data_tab.filter_inputs):
                # Get the condition for this specific parameter only
                filter_input = window.data_tab.filter_inputs[i]
                condition_str = filter_input.text().strip()
                
                # Check this parameter condition independently
                param_match = test_data.check_parameter_condition_independently(
                    site, specimen, i, condition_str, range_up, range_down
                )
                
                if not condition_str or not condition_str.strip():

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

    def get_independent_parameter_colors(self, window, site, specimen):
        """Get color information for each parameter independently"""
        if not hasattr(window.data_tab, 'test_data_generator'):
            return {}
        
        test_data = window.data_tab.test_data_generator
        
        # Get current range settings
        try:
            range_up = int(window.data_tab.range_up_combo.currentText())
            range_down = int(window.data_tab.range_down_combo.currentText())
        except (ValueError, AttributeError):
            range_up = 100
            range_down = 1
        
        # Get filter conditions
        filter_conditions = []
        for i in range(test_data.num_params):
            if i < len(window.data_tab.filter_inputs):
                condition = window.data_tab.filter_inputs[i].text().strip()
                filter_conditions.append(condition)
            else:
                filter_conditions.append("")
        
        # Calculate color for each parameter independently
        parameter_colors = {}
        
        for i, param_label in enumerate(test_data.parameter_labels):
            if i < len(filter_conditions):
                condition_str = filter_conditions[i]
                
                if not condition_str or not condition_str.strip():
                    # No condition - default color
                    parameter_colors[param_label] = {
                        'background': 'white',
                        'text': 'black',
                        'match': True,
                        'reason': 'No condition specified'
                    }
                else:
                    # Check condition independently
                    param_match = test_data.check_parameter_condition_independently(
                        site, specimen, i, condition_str, range_up, range_down
                    )
                    
                    if param_match:
                        # Condition met
                        parameter_colors[param_label] = {
                            'background': 'lightgreen',
                            'text': 'black',
                            'match': True,
                            'reason': f'Condition "{condition_str}" met'
                        }
                    else:
                        # Condition not met
                        parameter_colors[param_label] = {
                            'background': 'lightcoral',
                            'text': 'black',
                            'match': False,
                            'reason': f'Condition "{condition_str}" not met'
                        }
            else:
                # No condition for this parameter
                parameter_colors[param_label] = {
                    'background': 'white',
                    'text': 'black',
                    'match': True,
                    'reason': 'No condition specified'
                }
        
        return parameter_colors