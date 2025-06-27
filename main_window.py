from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from menu_manager import MenuManager
from data_tab import DataTab
from selection_tab import SelectionTab


class MainWindow(QMainWindow):
    """Main application window containing data view and sample selection tabs"""
    
    def __init__(self):
        super().__init__()
        from config import LayoutConfig
        self.config = LayoutConfig()
        self.setWindowTitle(self.config.MAIN_WINDOW['title'])
        self.resize(*self.config.MAIN_WINDOW['size'])
        self.setStyleSheet(self.config.get_main_window_style())
        self.current_folder = ""
        self.current_file = ""
        self.menu_manager = MenuManager(self)
        self.menu_manager.create_menu_bar()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Setup main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(*self.config.MAIN_WINDOW['margins'])
        main_layout.setSpacing(self.config.MAIN_WINDOW['spacing'])
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Apply borderless tab style (overrides configuration style)
        self.tab_widget.setStyleSheet(self._get_borderless_tab_style())
        
        # First tab: Data View
        self.data_tab = DataTab(self)
        self.tab_widget.addTab(self.data_tab, "Data View")
        
        # Second tab: Sample Selection
        self.selection_tab = SelectionTab(self)
        self.tab_widget.addTab(self.selection_tab, "Sample Selection")
        
        # Add tab widget to main layout with stretch factor
        main_layout.addWidget(self.tab_widget, 1)
        
        # Update initial status display
        self.update_status_display()

    def _get_borderless_tab_style(self):
        """Get borderless tab widget styling"""
        return """
            QTabWidget {
                border: none;
                background-color: transparent;
            }
            QTabWidget::pane {
                border: none;
                background-color: transparent;
                margin: 0px;
                padding: 0px;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-bottom: none;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                min-width: 100px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom: 1px solid #ffffff;
                margin-bottom: -1px;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background-color: #e8e8e8;
            }
        """

    def update_status_display(self):
        """Update status display based on current data state"""
        if not self.current_folder and not self.current_file:
            # Reset controls when no data is loaded
            self.data_tab.reset_controls()

    def on_selection_changed(self, selected_items):
        """Handle selection changes from Sample Selection tab
        
        Args:
            selected_items (list): List of selected specimen items
        """
        # Can add additional logic here for status updates, saving selections, etc.
        pass

    def load_data(self):
        """Load data and refresh style menu"""
        # Data loading logic implementation goes here
        # ...existing data loading code...
        
        # Refresh style menu after data loading
        if hasattr(self, 'menu_manager'):
            self.menu_manager.refresh_style_menu()

    def load_redo_data(self):
        """Load .redo data and refresh style menu"""
        # .redo data loading logic implementation goes here
        # ...existing redo data loading code...
        
        # Refresh style menu after data loading
        if hasattr(self, 'menu_manager'):
            self.menu_manager.refresh_style_menu()