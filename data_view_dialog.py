"""
Data View Dialog for displaying imported data in a table format
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, 
                              QTableWidgetItem, QPushButton, QLabel, QHeaderView, 
                              QSplitter, QTextEdit, QScrollArea, QFrame, QGroupBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import pandas as pd


class DataViewDialog(QDialog):
    """Dialog for viewing imported data with detailed information"""
    
    def __init__(self, data, file_path, parent=None):
        super().__init__(parent)
        self.data = data
        self.file_path = file_path
        self.setWindowTitle("Data View - Imported Data")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        self.setup_ui()
        self.populate_data()
    
    def setup_ui(self):
        """Setup the dialog UI with modern design"""
        # Set main dialog style
        self.setStyleSheet("""
            QDialog {
                background-color: #f8fafc;
                color: #1e293b;
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Modern header section
        header_widget = QFrame()
        header_widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #e2e8f0;
            }
        """)
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("Data Overview")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #0f172a; margin-bottom: 5px;")
        header_layout.addWidget(title_label)
        
        # File info row
        file_info_layout = QHBoxLayout()
        file_info_layout.setSpacing(20)
        
        file_label = QLabel(f"File: {self.file_path.split('/')[-1]}")
        file_label.setFont(QFont("Arial", 13, QFont.Medium))
        file_label.setStyleSheet("color: #475569;")
        
        rows_label = QLabel(f"{len(self.data):,} rows")
        rows_label.setFont(QFont("Arial", 12))
        rows_label.setStyleSheet("""
            color: white;
            background-color: #3b82f6;
            padding: 6px 12px;
            border-radius: 16px;
            font-weight: 600;
        """)
        
        cols_label = QLabel(f"{len(self.data.columns)} columns")
        cols_label.setFont(QFont("Arial", 12))
        cols_label.setStyleSheet("""
            color: white;
            background-color: #10b981;
            padding: 6px 12px;
            border-radius: 16px;
            font-weight: 600;
        """)
        
        file_info_layout.addWidget(file_label)
        file_info_layout.addStretch()
        file_info_layout.addWidget(rows_label)
        file_info_layout.addWidget(cols_label)
        header_layout.addLayout(file_info_layout)
        
        main_layout.addWidget(header_widget)
        
        # Create splitter for table and info panel
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #e2e8f0;
                width: 2px;
                border-radius: 1px;
            }
            QSplitter::handle:hover {
                background-color: #cbd5e1;
            }
        """)
        
        # Left side - Data table
        table_group = QGroupBox("Data Preview")
        table_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #1e293b;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                background-color: white;
            }
        """)
        table_layout = QVBoxLayout(table_group)
        table_layout.setContentsMargins(15, 20, 15, 15)
        
        self.table_widget = QTableWidget()
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.verticalHeader().setVisible(True)
        self.table_widget.setSortingEnabled(True)
        
        # Modern table styling
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                gridline-color: #f1f5f9;
                font-size: 12px;
                selection-background-color: #eff6ff;
            }
            QTableWidget::item {
                padding: 10px 8px;
                border-bottom: 1px solid #f1f5f9;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #1e40af;
            }
            QTableWidget::item:hover {
                background-color: #f8fafc;
            }
            QTableWidget::item:alternate {
                background-color: #fafbfc;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 12px 10px;
                border: none;
                border-right: 1px solid #e2e8f0;
                border-bottom: 2px solid #cbd5e1;
                font-weight: 600;
                color: #374151;
                font-size: 12px;
            }
            QHeaderView::section:first {
                border-top-left-radius: 8px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 8px;
                border-right: none;
            }
            QHeaderView::section:vertical {
                border-top: none;
                border-bottom: 1px solid #e2e8f0;
                border-right: 1px solid #e2e8f0;
                padding: 8px 4px;
            }
        """)
        
        table_layout.addWidget(self.table_widget)
        splitter.addWidget(table_group)
        
        # Right side - Data info panel
        info_group = QGroupBox("📈 Data Statistics")
        info_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #1e293b;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                background-color: white;
            }
        """)
        info_layout = QVBoxLayout(info_group)
        info_layout.setContentsMargins(15, 20, 15, 15)
        
        # Info text area with modern styling
        self.info_text = QTextEdit()
        self.info_text.setMaximumWidth(350)
        self.info_text.setReadOnly(True)
        self.info_text.setFont(QFont("Consolas", 10))
        self.info_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 15px;
                color: #374151;
                line-height: 1.4;
            }
        """)
        info_layout.addWidget(self.info_text)
        
        splitter.addWidget(info_group)
        
        # Set splitter sizes (85% table, 15% info)
        splitter.setSizes([1000, 200])
        main_layout.addWidget(splitter)
        
        # Modern bottom buttons
        button_widget = QFrame()
        button_widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 15px;
                border: 1px solid #e2e8f0;
            }
        """)
        button_layout = QHBoxLayout(button_widget)
        button_layout.setSpacing(15)
        
        refresh_btn = QPushButton("Refresh Info")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
                border-color: #9ca3af;
            }
            QPushButton:pressed {
                background-color: #d1d5db;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_info)
        
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        close_btn.clicked.connect(self.accept)
        
        button_layout.addStretch()
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(close_btn)
        
        main_layout.addWidget(button_widget)
    
    def populate_data(self):
        """Populate the table with data"""
        if self.data is None or self.data.empty:
            return
            
        # Set table dimensions
        self.table_widget.setRowCount(len(self.data))
        self.table_widget.setColumnCount(len(self.data.columns))
        
        # Set headers
        self.table_widget.setHorizontalHeaderLabels(list(self.data.columns))
        
        # Populate data (show first 1000 rows for performance)
        max_rows = min(1000, len(self.data))
        for row in range(max_rows):
            for col in range(len(self.data.columns)):
                value = self.data.iloc[row, col]
                # Handle different data types
                if pd.isna(value):
                    display_value = "NaN"
                elif isinstance(value, (int, float)):
                    if pd.isna(value):
                        display_value = "NaN"
                    else:
                        display_value = str(value)
                else:
                    display_value = str(value)
                
                item = QTableWidgetItem(display_value)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsSelectable)  # Read-only but selectable
                self.table_widget.setItem(row, col, item)
        
        # If data is truncated, show message
        if len(self.data) > 1000:
            self.table_widget.setRowCount(1001)
            truncation_item = QTableWidgetItem(f"... and {len(self.data) - 1000} more rows")
            truncation_item.setFlags(truncation_item.flags() | Qt.ItemFlag.ItemIsSelectable)
            for col in range(len(self.data.columns)):
                self.table_widget.setItem(1000, col, truncation_item)
        
        # Adjust column widths
        self.table_widget.resizeColumnsToContents()
        
        # Populate info panel
        self.refresh_info()
    
    def refresh_info(self):
        """Refresh the information panel with modern formatting"""
        if self.data is None:
            return
            
        info_text = []
        info_text.append("📊 DATA SUMMARY")
        info_text.append("═" * 35)
        info_text.append(f"📏 Shape: {self.data.shape[0]:,} rows × {self.data.shape[1]} columns")
        info_text.append(f"💾 Memory: {self.data.memory_usage(deep=True).sum() / 1024:.1f} KB")
        info_text.append("")
        
        info_text.append("📋 COLUMN DETAILS")
        info_text.append("─" * 35)
        
        for i, col in enumerate(self.data.columns, 1):
            dtype = self.data[col].dtype
            non_null = self.data[col].count()
            null_count = len(self.data) - non_null
            
            info_text.append(f"\n{i}. 🏷️  {col}")
            info_text.append(f"   📝 Type: {dtype}")
            info_text.append(f"   ✅ Non-null: {non_null:,}")
            info_text.append(f"   ❌ Null: {null_count}")
            
            # Show sample values for object columns
            if dtype == 'object':
                unique_vals = self.data[col].dropna().unique()
                sample_vals = unique_vals[:3] if len(unique_vals) > 3 else unique_vals
                if len(sample_vals) > 0:
                    info_text.append(f"   🔍 Samples: {', '.join(map(str, sample_vals))}")
                if len(unique_vals) > 3:
                    info_text.append(f"   📊 ... +{len(unique_vals) - 3} more unique")
            elif dtype in ['int64', 'float64']:
                info_text.append(f"   📊 Range: {self.data[col].min():.2f} - {self.data[col].max():.2f}")
                info_text.append(f"   📈 Mean: {self.data[col].mean():.2f}")
                info_text.append(f"   📉 Std: {self.data[col].std():.2f}")
        
        info_text.append("")
        info_text.append("👁️  PREVIEW (First 5 rows)")
        info_text.append("─" * 35)
        
        # Show first 5 rows as sample with better formatting
        sample_df = self.data.head()
        for i, (idx, row) in enumerate(sample_df.iterrows(), 1):
            info_text.append(f"\nRow {i}:")
            for col in sample_df.columns:
                val = row[col]
                if pd.isna(val):
                    val_str = "NaN"
                else:
                    val_str = str(val)[:30] + "..." if len(str(val)) > 30 else str(val)
                info_text.append(f"  {col}: {val_str}")
        
        self.info_text.setText("\n".join(info_text))
