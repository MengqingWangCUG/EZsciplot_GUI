import sys
import numpy as np
from PySide6.QtWidgets import (QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QTreeWidget, 
                              QTreeWidgetItem, QSizePolicy, QScrollArea, QSplitter, 
                              QLabel, QPushButton)
from PySide6.QtCore import Qt
from config import LayoutConfig
from preview_manager import PreviewManager

try:
    TRI_STATE_FLAG = Qt.ItemFlag.ItemIsTristate
except AttributeError:
    TRI_STATE_FLAG = Qt.ItemFlag.ItemIsAutoTristate


class SelectionTab(QWidget):
    """Selection tab widget for specimen selection and preview management"""
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.config = LayoutConfig
        
        # Create preview manager
        self.preview_manager = PreviewManager(main_window, self)
        self.total_specimen_count = 0
        self._syncing_checks = False
        self._pending_selection_tokens = set()
        
        self.create_ui()

    def create_ui(self):
        """Create user interface - completely fill the window"""
        from PySide6.QtWidgets import QSplitter
        from PySide6.QtCore import Qt

        config = self.config.SELECTION_TAB
        
        # Main layout - remove margins to completely fill the content
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Completely remove margins
        layout.setSpacing(0)  # Remove spacing
        
        # Main content area - use QSplitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setChildrenCollapsible(False)
        main_splitter.setHandleWidth(1)
        
        # Use configured splitter style with visible handles
        main_splitter.setStyleSheet(self.config.get_selection_splitter_style())
        
        # Left side: Tree structure
        tree_group = self.create_tree_group()
        
        # Right side: Preview area (managed by PreviewManager)
        preview_group = self.preview_manager.create_preview_group()
        
        # Add to splitter
        main_splitter.addWidget(tree_group)
        main_splitter.addWidget(preview_group)
        
        # Set initial ratio (tree structure:preview area = 1:6)
        ratio = config['tree_plot_ratio']
        total_ratio = ratio[0] + ratio[1]
        tree_proportion = int((ratio[0] / total_ratio) * 1000)
        plot_proportion = int((ratio[1] / total_ratio) * 1000)
        main_splitter.setSizes([tree_proportion, plot_proportion])
        
        # Set minimum width constraints - ensure both areas have minimum usable width
        tree_group.setMinimumWidth(150)    # Tree structure minimum width
        tree_group.setMaximumWidth(400)    # Tree structure maximum width
        preview_group.setMinimumWidth(300) # Preview area minimum width
        # Don't set maximum width for preview_group, let it expand arbitrarily
        
        # Set splitter stretch factors
        main_splitter.setStretchFactor(0, ratio[0])   # Tree structure group stretch factor
        main_splitter.setStretchFactor(1, ratio[1])   # Preview group stretch factor
        
        # Let splitter occupy all space, completely fill the window
        layout.addWidget(main_splitter, 1)  # stretch factor = 1, occupy all space

    def _get_groupbox_style(self, style_name='default'):
        """Get group box style"""
        if not hasattr(self.config, 'GROUPBOX_STYLES'):
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

    def _get_button_style(self):
        """Get button style"""
        style = self.config.STYLES['button']
        return f"""
            QPushButton {{
                font-size: {style['font_size']};
                padding: {style['padding']};
                background-color: {style['background_color']};
                color: {style['color']};
                border: {style['border']};
                border-radius: {style['border_radius']};
                font-weight: {style['font_weight']};
                min-height: 25px;
                min-width: 80px;
            }}
            QPushButton:disabled {{
                background-color: {style['disabled_bg']};
                color: {style['disabled_color']};
            }}
            QPushButton:enabled:hover {{
                background-color: {style['hover_bg']};
            }}
            QPushButton:focus {{
                outline: none;
                border: none;
            }}
        """

    def create_tree_group(self):
        """Create tree structure group with improved modern design"""
        # Modern tree group with clean design
        tree_group = QGroupBox("Sample Selection")
        tree_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 8px;
                background-color: #fafafa;
                font-size: 13px;
                font-weight: 600;
                color: #2c3e50;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                background-color: #fafafa;
            }
        """)
        tree_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        tree_layout = QVBoxLayout()
        tree_layout.setContentsMargins(12, 20, 12, 12)
        tree_layout.setSpacing(8)
        
        # Create modern scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                background-color: white;
            }
            QScrollBar:vertical {
                border: none;
                background: #f5f5f5;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
        """)
        
        # Create tree widget with custom styling
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)  # Force single column
        self.tree.setHeaderHidden(True)
        self.tree.setSelectionMode(QTreeWidget.SelectionMode.NoSelection)  # Use checkboxes only
        self.tree.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tree.setUniformRowHeights(True)
        self.tree.setAlternatingRowColors(False)
        self.tree.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.tree.setIndentation(20)
        self.tree.setRootIsDecorated(True)
        self.tree.setAnimated(False)
        
        # Apply modern tree styling with clean checkboxes
        self.tree.setStyleSheet("""
            QTreeWidget {
                border: none;
                background-color: #ffffff;
                outline: none;
                font-size: 13px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            QTreeWidget::item {
                height: 36px;
                border: none;
                padding: 8px 12px;
                margin: 2px 8px;
                border-radius: 8px;
                background-color: transparent;
            }
            QTreeWidget::item:hover {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
            }
            QTreeWidget::item:selected {
                background-color: #eff6ff;
                border: 1px solid #3b82f6;
            }
            QTreeWidget::item:branch {
                background: transparent;
                border: none;
            }
            QTreeWidget::item:branch:has-children:!has-siblings:closed,
            QTreeWidget::item:branch:closed:has-children:has-siblings {
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHZpZXdCb3g9IjAgMCAxNCAxNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTUgM0w5IDdMNSAxMSIgc3Ryb2tlPSIjNjQ3NDhiIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4=);
            }
            QTreeWidget::item:branch:open:has-children:!has-siblings,
            QTreeWidget::item:branch:open:has-children:has-siblings {
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHZpZXdCb3g9IjAgMCAxNCAxNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTMgN0wxMSA3IiBzdHJva2U9IiM2NDc0OGIiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPg==);
            }
            QTreeWidget::indicator {
                width: 14px;
                height: 14px;
                border-radius: 3px;
                border: 2px solid #e2e8f0;
                background-color: #ffffff;
            }
            QTreeWidget::indicator:hover {
                border: 2px solid #3b82f6;
                background-color: #f0f9ff;
            }
            QTreeWidget::indicator:checked {
                border: 2px solid #3b82f6;
                background-color: #3b82f6;
            }
            QTreeWidget::indicator:unchecked {
                background-color: #ffffff;
                border: 2px solid #e2e8f0;
            }
            QTreeWidget::indicator:indeterminate {
                border: 2px solid #60a5fa;
                background-color: #dbeafe;
            }
            QTreeWidget::indicator:selected {
                border: 2px solid #3b82f6;
                background-color: #3b82f6;
            }
        """)
        
        # Force style update
        self.tree.style().unpolish(self.tree)
        self.tree.style().polish(self.tree)
        
        # Connect signals - only use itemClicked for better control
        self.tree.itemClicked.connect(self._on_tree_item_clicked)
        
        # Put tree widget into scroll area
        scroll_area.setWidget(self.tree)
        
        # Create control buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)  # Fixed spacing
        
        # Get button maximum width, use default if not in configuration
        button_max_width = 100
        
        # Import Data button
        self.import_btn = QPushButton("Import Data")
        self.import_btn.setMinimumWidth(button_max_width)
        self.import_btn.clicked.connect(self._on_import_data)
        
        # Data View button
        self.data_view_btn = QPushButton("Data View")
        self.data_view_btn.setMinimumWidth(button_max_width)
        self.data_view_btn.clicked.connect(self._on_data_view)
        self.data_view_btn.setEnabled(False)  # Enable only after data is imported
        
        # Select all button
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.select_all_items)
        self.select_all_btn.setMaximumWidth(button_max_width)
        self.select_all_btn.setStyleSheet(self._get_button_style())
        
        # Deselect all button
        self.deselect_all_btn = QPushButton("Deselect All")
        self.deselect_all_btn.clicked.connect(self.deselect_all_items)
        self.deselect_all_btn.setMaximumWidth(button_max_width)
        self.deselect_all_btn.setStyleSheet(self._get_button_style())
        
        # Apply styles to new buttons
        self.import_btn.setStyleSheet(self._get_button_style())
        self.data_view_btn.setStyleSheet(self._get_button_style())
        
        # Add all buttons to layout
        button_layout.addWidget(self.import_btn)
        button_layout.addWidget(self.data_view_btn)
        button_layout.addWidget(self.select_all_btn)
        button_layout.addWidget(self.deselect_all_btn)
        button_layout.addStretch()
        
        # Selection info display - use style from configuration
        self.selection_info = QLabel("0/0 specimens selected")
        self.selection_info.setStyleSheet(self.config.get_selection_info_style())
        
        # Get fixed height from configuration
        info_config = self.config.SELECTION_TAB_STYLES['selection_info']
        self.selection_info.setFixedHeight(int(info_config['fixed_height'].replace('px', '')))
        
        # Layout assembly - scroll area occupies main space
        tree_layout.addWidget(scroll_area, 1)  # stretch factor = 1, occupy main space
        tree_layout.addLayout(button_layout)
        tree_layout.addWidget(self.selection_info)
        
        tree_group.setLayout(tree_layout)
        
        # Populate tree structure
        self.populate_tree()
        
        return tree_group

    def populate_tree(self):
        """Get data from DataTab and populate tree structure"""
        self.tree.blockSignals(True)
        self.tree.clear()
        self.total_specimen_count = 0
        
        # Get sample_data from DataTab
        if hasattr(self.main_window, 'data_tab') and hasattr(self.main_window.data_tab, 'sample_data'):
            sample_data = self.main_window.data_tab.sample_data
            
            # Iterate through sites (now Site objects)
            for site_name, site_obj in sample_data.items():
                # Create site item
                site_item = QTreeWidgetItem([site_name])
                site_item.setFlags(site_item.flags() | Qt.ItemFlag.ItemIsUserCheckable | TRI_STATE_FLAG)
                site_item.setCheckState(0, Qt.CheckState.Unchecked)
                site_item.setData(0, Qt.ItemDataRole.UserRole, {'type': 'site', 'name': site_name})
                
                # Get specimens from Site object
                if isinstance(site_obj, list):
                    specimens = site_obj
                elif hasattr(site_obj, 'get_sample_names'):
                    specimens = site_obj.get_sample_names()
                elif hasattr(site_obj, 'samples'):
                    specimens = list(site_obj.samples.keys())
                else:
                    specimens = []
                
                for specimen in specimens:
                    # Create specimen item
                    specimen_item = QTreeWidgetItem([specimen])
                    specimen_item.setFlags(specimen_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    specimen_item.setCheckState(0, Qt.CheckState.Unchecked)
                    specimen_item.setData(0, Qt.ItemDataRole.UserRole, {
                        'type': 'specimen',
                        'name': specimen,
                        'site': site_name
                    })
                    
                    site_item.addChild(specimen_item)
                    self.total_specimen_count += 1
                
                # Expand site items by default for better visibility
                site_item.setExpanded(True)
                self.tree.addTopLevelItem(site_item)
            
            self.preview_manager.populate_site_preview_combo()
        else:
            placeholder_item = QTreeWidgetItem(["No data available - Load data in Data View tab first"])
            placeholder_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.tree.addTopLevelItem(placeholder_item)
        
        self.tree.blockSignals(False)
        self._apply_pending_selection()
        self.update_selection_info()

    def _on_tree_item_clicked(self, item, column):
        """Toggle selection when clicking the item"""
        if not item:
            return
        if not (item.flags() & Qt.ItemFlag.ItemIsUserCheckable):
            return
        if self._syncing_checks:
            return
        
        # Toggle check state
        current = item.checkState(0)
        new_state = Qt.CheckState.Unchecked if current == Qt.CheckState.Checked else Qt.CheckState.Checked
        
        # Set the new state
        item.setCheckState(0, new_state)
        
        # Process the change
        self.on_item_check_state_changed(item, 0)

    def on_item_check_state_changed(self, item, column):
        """Enhanced parent/child check state sync with visual feedback"""
        if self._syncing_checks:
            return
        item_data = item.data(0, Qt.ItemDataRole.UserRole)
        if not item_data:
            return
        
        self._syncing_checks = True
        try:
            if item_data['type'] == 'site':
                # Site clicked: sync all children and update TestData
                site_name = item_data['name']
                new_state = item.checkState(0)
                
                for i in range(item.childCount()):
                    child = item.child(i)
                    child_data = child.data(0, Qt.ItemDataRole.UserRole)
                    if child_data and child_data['type'] == 'specimen':
                        specimen_name = child_data['name']
                        child.setCheckState(0, new_state)
                        
                        # Update TestData selection state
                        if hasattr(self.main_window, 'data_tab') and hasattr(self.main_window.data_tab, 'test_data_generator'):
                            test_data = self.main_window.data_tab.test_data_generator
                            if new_state == Qt.CheckState.Checked:
                                test_data.add_selected_sample(site_name, specimen_name)
                            else:
                                test_data.remove_selected_sample(site_name, specimen_name)
                
                # Visual styling handled by CSS
                
            elif item_data['type'] == 'specimen':
                # Specimen clicked: update parent site state
                parent = item.parent()
                if parent:
                    parent_data = parent.data(0, Qt.ItemDataRole.UserRole)
                    site_name = parent_data['name']
                    specimen_name = item_data['name']
                    
                    # Update TestData selection state
                    if hasattr(self.main_window, 'data_tab') and hasattr(self.main_window.data_tab, 'test_data_generator'):
                        test_data = self.main_window.data_tab.test_data_generator
                        if item.checkState(0) == Qt.CheckState.Checked:
                            test_data.add_selected_sample(site_name, specimen_name)
                        else:
                            test_data.remove_selected_sample(site_name, specimen_name)
                    
                    # Update parent site check state based on children
                    checked_children = sum(
                        1 for i in range(parent.childCount())
                        if parent.child(i).checkState(0) == Qt.CheckState.Checked
                    )
                    total_children = parent.childCount()
                    
                    if checked_children == total_children:
                        parent.setCheckState(0, Qt.CheckState.Checked)
                    elif checked_children == 0:
                        parent.setCheckState(0, Qt.CheckState.Unchecked)
                    else:
                        parent.setCheckState(0, Qt.CheckState.PartiallyChecked)
                
        finally:
            self._syncing_checks = False
        
        self._handle_selection_change()
    
    # Style methods removed - using CSS styles instead

    def _handle_selection_change(self):
        """Update info text, previews, and toolbar state after a selection change"""
        self.update_selection_info()
        self.preview_manager.update_selection_preview()

    def get_selected_items(self):
        """Get all selected items (only return leaf nodes) - return dict format for compatibility"""
        selected_items = []
        
        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            site_item = root.child(i)
            site_data = site_item.data(0, Qt.ItemDataRole.UserRole)
            if not site_data or site_data.get('type') != 'site':
                continue
            for j in range(site_item.childCount()):
                specimen_item = site_item.child(j)
                if specimen_item.checkState(0) != Qt.CheckState.Checked:
                    continue
                specimen_data = specimen_item.data(0, Qt.ItemDataRole.UserRole)
                if specimen_data and specimen_data.get('type') == 'specimen':
                    # Return dict format for compatibility with data_utils.py
                    selected_items.append({
                        'type': 'specimen',
                        'site': site_data['name'],
                        'name': specimen_data['name']
                    })
        
        return selected_items

    def select_all_items(self):
        """Select all items"""
        self._syncing_checks = True
        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            root.child(i).setCheckState(0, Qt.CheckState.Checked)
        self._syncing_checks = False
        self._handle_selection_change()

    def deselect_all_items(self):
        """Deselect all items"""
        self._syncing_checks = True
        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            root.child(i).setCheckState(0, Qt.CheckState.Unchecked)
        self._syncing_checks = False
        self._handle_selection_change()

    def update_selection_info(self):
        """Update selection info display"""
        selected_count = 0
        total_count = 0
        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            site_item = root.child(i)
            site_data = site_item.data(0, Qt.ItemDataRole.UserRole)
            if not site_data or site_data.get('type') != 'site':
                continue
            total_count += site_item.childCount()
            for j in range(site_item.childCount()):
                if site_item.child(j).checkState(0) == Qt.CheckState.Checked:
                    selected_count += 1
        
        # Update selection count display on UI
        if hasattr(self, 'selection_info'):
            total_display = self.total_specimen_count or total_count
            self.selection_info.setText(f"{selected_count}/{total_display} specimens selected")

    def apply_selection(self):
        """Apply selection - now automatically called directly when selection changes"""
        selected_items = self.get_selected_items()
        
        if selected_items:
            self.preview_manager.update_selection_preview()
        else:
            self.preview_manager.clear_preview_plots()
        self.notify_selection_changed(selected_items)

    def notify_selection_changed(self, selected_items):
        """Notify main window that selection has changed"""
        if hasattr(self.main_window, 'on_selection_changed'):
            self.main_window.on_selection_changed(selected_items)

    def save_state(self, settings):
        """Persist the currently checked specimens"""
        settings.beginGroup("SelectionTab")
        settings.setValue("selected", self._get_selected_tokens())
        settings.endGroup()

    def restore_state(self, settings):
        """Restore checked specimens from settings"""
        if not settings:
            return
        settings.beginGroup("SelectionTab")
        tokens = settings.value("selected", [])
        settings.endGroup()
        if isinstance(tokens, str):
            tokens = [tokens]
        self._pending_selection_tokens = set(filter(None, tokens))
        self._apply_pending_selection()

    def _make_item_token(self, site_name, specimen_name):
        return f"{site_name}::{specimen_name}"

    def _get_selected_tokens(self):
        """Return an internal list of selected specimen identifiers"""
        tokens = []
        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            site_item = root.child(i)
            site_data = site_item.data(0, Qt.ItemDataRole.UserRole)
            if not site_data or site_data.get('type') != 'site':
                continue
            site_name = site_data['name']
            for j in range(site_item.childCount()):
                specimen_item = site_item.child(j)
                specimen_data = specimen_item.data(0, Qt.ItemDataRole.UserRole)
                if (specimen_item.checkState(0) == Qt.CheckState.Checked and
                        specimen_data and specimen_data.get('type') == 'specimen'):
                    tokens.append(self._make_item_token(site_name, specimen_data['name']))
        return tokens

    def _apply_pending_selection(self):
        """Apply any saved selection tokens to the current tree"""
        if not getattr(self, '_pending_selection_tokens', None):
            return
        root = self.tree.invisibleRootItem()
        if root.childCount() == 0:
            return
        self._syncing_checks = True
        try:
            for i in range(root.childCount()):
                site_item = root.child(i)
                site_data = site_item.data(0, Qt.ItemDataRole.UserRole)
                if not site_data or site_data.get('type') != 'site':
                    continue
                site_name = site_data['name']
                for j in range(site_item.childCount()):
                    specimen_item = site_item.child(j)
                    specimen_data = specimen_item.data(0, Qt.ItemDataRole.UserRole)
                    if not specimen_data or specimen_data.get('type') != 'specimen':
                        continue
                    token = self._make_item_token(site_name, specimen_data['name'])
                    if token in self._pending_selection_tokens:
                        specimen_item.setCheckState(0, Qt.CheckState.Checked)
        finally:
            self._syncing_checks = False
        self._pending_selection_tokens.clear()
        self._handle_selection_change()

    # Selection marker methods removed - using CSS indicators instead
    
    def _on_import_data(self):
        """Handle data import button click"""
        from PySide6.QtWidgets import QFileDialog
        import pandas as pd
        import os
        
        # Supported file formats
        file_filter = "Data Files (*.xlsx *.xls *.csv *.txt *.dat);;Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;Text Files (*.txt *.dat);;All Files (*)"
        
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Data File",
            "",
            file_filter
        )
        
        if not file_path:
            return
            
        try:
            # Determine file type and read accordingly
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in ['.xlsx', '.xls']:
                # Excel file
                df = pd.read_excel(file_path)
            elif file_ext == '.csv':
                # CSV file - try different encodings
                try:
                    df = pd.read_csv(file_path, encoding='utf-8')
                except UnicodeDecodeError:
                    try:
                        df = pd.read_csv(file_path, encoding='gbk')
                    except UnicodeDecodeError:
                        df = pd.read_csv(file_path, encoding='latin-1')
            elif file_ext in ['.txt', '.dat']:
                # Text file - try tab or comma delimiter
                try:
                    df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
                except:
                    try:
                        df = pd.read_csv(file_path, sep=',', encoding='utf-8')
                    except UnicodeDecodeError:
                        try:
                            df = pd.read_csv(file_path, sep='\t', encoding='gbk')
                        except:
                            df = pd.read_csv(file_path, sep=',', encoding='gbk')
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
            
            # Store imported data
            self.imported_data = df
            self.imported_file_path = file_path
            
            # Enable data view button
            self.data_view_btn.setEnabled(True)
            
            # Show success message
            self._show_message(f"Successfully imported {len(df)} rows from {os.path.basename(file_path)}")
            
        except Exception as e:
            self._show_message(f"Error importing file: {str(e)}", "error")
    
    def _on_data_view(self):
        """Handle data view button click - show data in a dialog"""
        from data_view_dialog import DataViewDialog
        
        if not hasattr(self, 'imported_data'):
            self._show_message("No data imported yet", "warning")
            return
            
        # Create data view dialog
        dialog = DataViewDialog(self.imported_data, self.imported_file_path, self)
        dialog.exec()
    
    def _show_message(self, message, msg_type="info"):
        """Show status message to user"""
        # Update selection info label temporarily
        original_text = self.selection_info.text()
        self.selection_info.setText(message)
        
        # Set color based on message type
        if msg_type == "error":
            self.selection_info.setStyleSheet("color: red; font-weight: bold;")
        elif msg_type == "warning":
            self.selection_info.setStyleSheet("color: orange; font-weight: bold;")
        else:
            self.selection_info.setStyleSheet("color: green; font-weight: bold;")
        
        # Reset after 3 seconds
        from PySide6.QtCore import QTimer
        QTimer.singleShot(3000, lambda: self._reset_selection_info(original_text))
    
    def _reset_selection_info(self, original_text):
        """Reset selection info to original text"""
        self.selection_info.setText(original_text)
        self.selection_info.setStyleSheet(self.config.get_selection_info_style())
