"""
Data Mapping Dialog for mapping imported data columns to test data structure
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, 
                              QTableWidgetItem, QPushButton, QLabel, QHeaderView, 
                              QComboBox, QGroupBox, QScrollArea, QFrame, QSpinBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import pandas as pd


class DataMappingDialog(QDialog):
    """Dialog for mapping imported data columns to test data structure"""
    
    def __init__(self, data, test_data_generator, parent=None):
        super().__init__(parent)
        self.data = data
        self.test_data_generator = test_data_generator
        self.setWindowTitle("Map Data to Test Structure")
        self.setMinimumSize(900, 600)
        self.resize(1000, 700)
        
        self.column_mappings = {}
        self.setup_ui()
        self.populate_data()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        # Header
        header_label = QLabel("Map Imported Data to Test Structure")
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_label.setStyleSheet("color: #1f2937; margin-bottom: 10px;")
        main_layout.addWidget(header_label)
        
        # Description
        desc_label = QLabel("Select which columns from your imported data correspond to the test data structure:")
        desc_label.setStyleSheet("color: #6b7280; font-size: 12px; margin-bottom: 20px;")
        main_layout.addWidget(desc_label)
        
        # Create scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Required mappings section
        required_group = QGroupBox("Required Field Mappings")
        required_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #374151;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #f9fafb;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: #f9fafb;
            }
        """)
        required_layout = QVBoxLayout(required_group)
        
        # Site column mapping
        site_row = QHBoxLayout()
        site_label = QLabel("Site Column:")
        site_label.setStyleSheet("font-weight: 600; color: #4b5563; min-width: 120px;")
        self.site_combo = QComboBox()
        self.site_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 12px;
                border: 2px solid #d1d5db;
                border-radius: 6px;
                background-color: white;
                font-size: 13px;
                min-width: 200px;
            }
            QComboBox:hover {
                border-color: #9ca3af;
            }
            QComboBox:focus {
                border-color: #3b82f6;
                outline: none;
            }
        """)
        site_row.addWidget(site_label)
        site_row.addWidget(self.site_combo)
        site_row.addStretch()
        required_layout.addLayout(site_row)
        
        # Sample column mapping
        sample_row = QHBoxLayout()
        sample_label = QLabel("Sample Column:")
        sample_label.setStyleSheet("font-weight: 600; color: #4b5563; min-width: 120px;")
        self.sample_combo = QComboBox()
        self.sample_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 12px;
                border: 2px solid #d1d5db;
                border-radius: 6px;
                background-color: white;
                font-size: 13px;
                min-width: 200px;
            }
            QComboBox:hover {
                border-color: #9ca3af;
            }
            QComboBox:focus {
                border-color: #3b82f6;
                outline: none;
            }
        """)
        sample_row.addWidget(sample_label)
        sample_row.addWidget(self.sample_combo)
        sample_row.addStretch()
        required_layout.addLayout(sample_row)
        
        content_layout.addWidget(required_group)
        
        # Optional data columns section
        optional_group = QGroupBox("Optional Data Columns")
        optional_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #374151;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #f9fafb;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: #f9fafb;
            }
        """)
        optional_layout = QVBoxLayout(optional_group)
        
        # Data preview table
        preview_label = QLabel("Data Preview (first 10 rows):")
        preview_label.setStyleSheet("font-weight: 600; color: #4b5563; margin-bottom: 10px;")
        optional_layout.addWidget(preview_label)
        
        self.preview_table = QTableWidget()
        self.preview_table.setAlternatingRowColors(True)
        self.preview_table.horizontalHeader().setStretchLastSection(True)
        self.preview_table.verticalHeader().setVisible(True)
        self.preview_table.setSortingEnabled(True)
        self.preview_table.setMaximumHeight(300)
        
        # Style the table
        self.preview_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                gridline-color: #f3f4f6;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f3f4f6;
            }
            QTableWidget::item:selected {
                background-color: #eff6ff;
                color: #1d4ed8;
            }
            QTableWidget::item:hover {
                background-color: #f8fafc;
            }
            QHeaderView::section {
                background-color: #f3f4f6;
                padding: 8px 12px;
                border: none;
                border-right: 1px solid #e5e7eb;
                border-bottom: 2px solid #d1d5db;
                font-weight: 600;
                color: #374151;
                font-size: 12px;
            }
            QHeaderView::section:first {
                border-top-left-radius: 6px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 6px;
                border-right: none;
            }
        """)
        
        optional_layout.addWidget(self.preview_table)
        content_layout.addWidget(optional_group)
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6b7280;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
            QPushButton:pressed {
                background-color: #374151;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        apply_btn = QPushButton("Apply Mapping")
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
            QPushButton:disabled {
                background-color: #d1d5db;
                color: #9ca3af;
            }
        """)
        apply_btn.clicked.connect(self.apply_mapping)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(apply_btn)
        
        main_layout.addLayout(button_layout)
    
    def populate_data(self):
        """Populate the dialog with data"""
        if self.data is None or self.data.empty:
            return
        
        # Populate column dropdowns
        columns = list(self.data.columns)
        self.site_combo.addItems(["-- Select Column --"] + columns)
        self.sample_combo.addItems(["-- Select Column --"] + columns)
        
        # Populate preview table
        max_rows = min(10, len(self.data))
        self.preview_table.setRowCount(max_rows)
        self.preview_table.setColumnCount(len(self.data.columns))
        self.preview_table.setHorizontalHeaderLabels(list(self.data.columns))
        
        for row in range(max_rows):
            for col in range(len(self.data.columns)):
                value = self.data.iloc[row, col]
                if pd.isna(value):
                    display_value = "NaN"
                else:
                    display_value = str(value)
                
                item = QTableWidgetItem(display_value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Read-only
                self.preview_table.setItem(row, col, item)
        
        self.preview_table.resizeColumnsToContents()
    
    def apply_mapping(self):
        """Apply the column mappings to test data"""
        site_col = self.site_combo.currentText()
        sample_col = self.sample_combo.currentText()
        
        if site_col == "-- Select Column --" or sample_col == "-- Select Column --":
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Missing Selection", "Please select both Site and Sample columns.")
            return
        
        try:
            # Clear existing test data
            self.test_data_generator.clear_all_sites()
            
            # Group data by site and sample
            grouped = self.data.groupby([site_col, sample_col])
            
            for (site_name, sample_name), group in grouped:
                # Add site if not exists
                if site_name not in self.test_data_generator.sites:
                    self.test_data_generator.add_site(site_name)
                
                # Add sample to site
                site = self.test_data_generator.sites[site_name]
                site.add_sample(sample_name)
                
                # Generate some sample data for the plots
                import numpy as np
                x_data = np.linspace(0, 10, 50)
                y1_data = np.random.normal(0, 1, 50) + np.sin(x_data)
                y2_data = np.random.normal(0, 1, 50) + np.cos(x_data)
                
                # Create plot data
                plot_key = f"plot_{len(site.samples[sample_name].plot_data)}"
                site.samples[sample_name].plot_data[plot_key] = {
                    'x': x_data.tolist(),
                    'y1': y1_data.tolist(),
                    'y2': y2_data.tolist(),
                    'title': f"Imported Data - {sample_name}"
                }
            
            self.accept()
            
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Mapping Error", f"Error applying mapping: {str(e)}")
