import sys
import numpy as np
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTreeWidget, QTreeWidgetItem, QGroupBox, QSplitter, QSizePolicy,
    QScrollArea
)
from PySide6.QtCore import Qt
from config import LayoutConfig
from preview_manager import PreviewManager


class SelectionTab(QWidget):
    """Selection tab widget for specimen selection and preview management"""
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.config = LayoutConfig
        
        # Create preview manager
        self.preview_manager = PreviewManager(main_window, self)
        
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
        
        # Use invisible splitter style - remove visible gray column
        main_splitter.setStyleSheet(self._get_invisible_splitter_style())
        
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

    def _get_invisible_splitter_style(self):
        """Get invisible splitter style - completely invisible but retains functionality"""
        return """
            QSplitter::handle {
                background-color: transparent;
                border: none;
                width: 0px;
                height: 0px;
                margin: 0px;
                padding: 0px;
            }
            QSplitter::handle:horizontal {
                width: 0px;
                background-color: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }
            QSplitter::handle:vertical {
                height: 0px;
                background-color: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }
            QSplitter::handle:hover {
                background-color: transparent;
            }
            QSplitter::handle:pressed {
                background-color: transparent;
            }
        """

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
        """Create tree structure group"""
        config = self.config.SELECTION_TAB['tree_group']
        tree_group = QGroupBox(config['title'])
        tree_group.setStyleSheet(self._get_groupbox_style('tree_group'))
        tree_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        tree_layout = QVBoxLayout()
        tree_layout.setContentsMargins(*config['margins'])
        tree_layout.setSpacing(config['spacing'])
        
        # Create scroll area to contain the tree widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)  # Remove scroll area frame
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Create tree widget
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Sites and Specimens")
        self.tree.setSelectionMode(QTreeWidget.SelectionMode.MultiSelection)
        self.tree.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Apply tree widget style from configuration
        self.tree.setStyleSheet(self.config.get_tree_widget_style())
        
        # Get tree widget attributes from configuration
        tree_config = self.config.SELECTION_TAB_STYLES['tree_widget']
        self.tree.setIndentation(int(tree_config['indentation'].replace('px', '')))
        self.tree.setRootIsDecorated(tree_config['root_decorated'])
        self.tree.setAnimated(tree_config['animated'])
        
        # Apply scroll area style from configuration
        scroll_area.setStyleSheet(self.config.get_scroll_area_style())
        
        # Put tree widget into scroll area
        scroll_area.setWidget(self.tree)
        
        # Connect signals
        self.tree.itemClicked.connect(self.on_item_clicked)
        
        # Create control buttons - remove Analyze button
        button_layout = QHBoxLayout()
        button_layout.setSpacing(config['button_spacing'])
        
        # Get button maximum width, use default if not in configuration
        button_max_width = config.get('button_max_width', 100)
        
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
        
        button_layout.addWidget(self.select_all_btn)
        button_layout.addWidget(self.deselect_all_btn)
        button_layout.addStretch()
        
        # Selection info display - use style from configuration
        self.selection_info = QLabel("0/11 specimens selected")
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
        self.tree.clear()
        
        # Get sample_data from DataTab
        if hasattr(self.main_window, 'data_tab') and hasattr(self.main_window.data_tab, 'sample_data'):
            sample_data = self.main_window.data_tab.sample_data
            
            for site_name, specimens in sample_data.items():
                # Create site node, default to showing unchecked symbol
                site_item = QTreeWidgetItem([f"☐ {site_name}"])
                site_item.setExpanded(True)  # Default expanded
                site_item.setData(0, Qt.ItemDataRole.UserRole, {'type': 'site', 'name': site_name, 'selected': False})
                
                # Directly add specimens as child nodes of the site
                for specimen in specimens:
                    specimen_item = QTreeWidgetItem([f"☐ {specimen}"])
                    specimen_item.setData(0, Qt.ItemDataRole.UserRole, {'type': 'specimen', 'name': specimen, 'selected': False})
                    site_item.addChild(specimen_item)
                
                self.tree.addTopLevelItem(site_item)
            
            # Update selection info
            self.update_selection_info()
            
            # Also update preview manager's site dropdown menu
            self.preview_manager.populate_site_preview_combo()
        else:
            # If no data, show placeholder
            placeholder_item = QTreeWidgetItem(["No data available - Load data in Data View tab first"])
            self.tree.addTopLevelItem(placeholder_item)

    def on_item_clicked(self, item, column):
        """Handle item click events - support clicking to toggle selected/deselected"""
        item_data = item.data(0, Qt.ItemDataRole.UserRole)
        if item_data:
            # Toggle selection state
            current_selected = item_data.get('selected', False)
            new_selected = not current_selected
            
            item_data['selected'] = new_selected
            item.setData(0, Qt.ItemDataRole.UserRole, item_data)
            
            # Update visual effect
            self.update_item_appearance(item)
            
            # If it's a parent item, update all child items
            if item_data['type'] == 'site':
                self.update_children_selection(item, new_selected)
            
            # If it's a child item, update parent item status
            elif item_data['type'] == 'specimen':
                self.update_parent_selection(item)
            
            # Update selection info and button status
            self.update_selection_info()
            
            # Update preview plot - directly update preview when selection changes
            self.preview_manager.update_selection_preview()

    def update_children_selection(self, parent_item, selected):
        """Update selection state of all child items"""
        for i in range(parent_item.childCount()):
            child = parent_item.child(i)
            child_data = child.data(0, Qt.ItemDataRole.UserRole)
            if child_data:
                child_data['selected'] = selected
                child.setData(0, Qt.ItemDataRole.UserRole, child_data)
                self.update_item_appearance(child)

    def update_parent_selection(self, item):
        """Update parent item selection state"""
        parent = item.parent()
        if parent:
            parent_data = parent.data(0, Qt.ItemDataRole.UserRole)
            if parent_data and parent_data['type'] == 'site':
                # Check status of all child items
                all_selected = True
                any_selected = False
                
                for i in range(parent.childCount()):
                    child = parent.child(i)
                    child_data = child.data(0, Qt.ItemDataRole.UserRole)
                    if child_data:
                        if child_data.get('selected', False):
                            any_selected = True
                        else:
                            all_selected = False
                
                # Update parent item status
                if all_selected:
                    parent_data['selected'] = True
                else:
                    parent_data['selected'] = False
                
                parent.setData(0, Qt.ItemDataRole.UserRole, parent_data)
                self.update_item_appearance(parent)

    def get_selected_items(self):
        """Get all selected items (only return leaf nodes)"""
        selected_items = []
        
        def traverse_tree(item):
            item_data = item.data(0, Qt.ItemDataRole.UserRole)
            if item_data and item_data.get('selected', False):
                # Only add leaf nodes (specimens)
                if item_data['type'] == 'specimen':
                    # Build path: Site → Specimen
                    parent = item.parent()
                    if parent:
                        parent_data = parent.data(0, Qt.ItemDataRole.UserRole)
                        if parent_data:
                            selected_items.append(f"{parent_data['name']} → {item_data['name']}")
            
            # Recursively process child items
            for i in range(item.childCount()):
                traverse_tree(item.child(i))
        
        # Traverse all top-level items
        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            traverse_tree(root.child(i))
        
        return selected_items

    def select_all_items(self):
        """Select all items"""
        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            site_item = root.child(i)
            site_data = site_item.data(0, Qt.ItemDataRole.UserRole)
            if site_data:
                # Select site
                site_data['selected'] = True
                site_item.setData(0, Qt.ItemDataRole.UserRole, site_data)
                site_name = site_data['name']
                site_item.setText(0, f"☑ {site_name}")
                
                # Select all child items
                self.update_children_selection(site_item, True)
        
        self.update_selection_info()
        self.preview_manager.update_selection_preview()

    def deselect_all_items(self):
        """Deselect all items"""
        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            site_item = root.child(i)
            site_data = site_item.data(0, Qt.ItemDataRole.UserRole)
            if site_data:
                # Deselect site
                site_data['selected'] = False
                site_item.setData(0, Qt.ItemDataRole.UserRole, site_data)
                site_name = site_data['name']
                site_item.setText(0, f"☐ {site_name}")
                
                # Deselect all child items
                self.update_children_selection(site_item, False)
        
        self.update_selection_info()
        self.preview_manager.update_selection_preview()

    def update_selection_info(self):
        """Update selection info display"""
        selected_items = self.get_selected_items()
        selected_count = len(selected_items)
        
        # Calculate total specimen count
        total_count = 0
        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            site_item = root.child(i)
            site_data = site_item.data(0, Qt.ItemDataRole.UserRole)
            if site_data:  # Ensure it's not a placeholder item
                total_count += site_item.childCount()
        
        # Update selection count display on UI
        if hasattr(self, 'selection_info'):
            self.selection_info.setText(f"{selected_count}/{total_count} specimens selected")

    def update_item_appearance(self, item):
        """Update visual display of item"""
        item_data = item.data(0, Qt.ItemDataRole.UserRole)
        if item_data:
            item_name = item_data['name']
            if item_data.get('selected', False):
                item.setText(0, f"☑ {item_name}")
            else:
                item.setText(0, f"☐ {item_name}")

    def apply_selection(self):
        """Apply selection - now automatically called directly when selection changes"""
        selected_items = self.get_selected_items()
        
        if selected_items:
            # Update preview plot
            self.preview_manager.update_selection_preview()
            
            # Notify main window that selection has changed
            self.notify_selection_changed(selected_items)
        else:
            self.preview_manager.clear_preview_plots()

    def notify_selection_changed(self, selected_items):
        """Notify main window that selection has changed"""
        if hasattr(self.main_window, 'on_selection_changed'):
            self.main_window.on_selection_changed(selected_items)