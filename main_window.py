from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget, QToolBar,
    QMessageBox, QFileDialog, QInputDialog
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QSettings
from menu_manager import MenuManager
from data_tab import DataTab
from selection_tab import SelectionTab
from config import LayoutConfig
import logging

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window containing data view and sample selection tabs"""
    
    def __init__(self):
        super().__init__()
        self.config = LayoutConfig()
        self.settings = QSettings("ipRESET", "SpecimenViewer")
        self.setWindowTitle(self.config.MAIN_WINDOW['title'])
        self.resize(*self.config.MAIN_WINDOW['size'])
        self.current_folder = ""
        self.current_file = ""
        self.menu_manager = MenuManager(self)
        self.menu_manager.create_menu_bar()
        self.statusBar().showMessage("Ready")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Setup main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(*self.config.MAIN_WINDOW['margins'])
        main_layout.setSpacing(self.config.MAIN_WINDOW['spacing'])
        
        # Create top bar with import functionality
        self._create_top_bar()
        main_layout.addWidget(self.top_bar_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self._update_toolbar_state)
        
        # First tab: Data View
        self.data_tab = DataTab(self)
        self.tab_widget.addTab(self.data_tab, "Data View")
        
        # Second tab: Sample Selection
        self.selection_tab = SelectionTab(self)
        self.tab_widget.addTab(self.selection_tab, "Sample Selection")
        
        # Add tab widget to main layout with stretch factor
        main_layout.addWidget(self.tab_widget, 1)

        self._create_toolbar()
        self.update_status_display()
        self.restore_settings()
        self._update_toolbar_state()

    def update_status_display(self):
        """Update status display based on current data state"""
        if not self.current_folder and not self.current_file:
            # Reset controls when no data is loaded
            self.data_tab.reset_controls()
        self._show_status("Ready")

    def _create_top_bar(self):
        """Create top bar - removed buttons, moved to toolbar"""
        # Top bar is no longer needed, but keep the widget for compatibility
        from PySide6.QtWidgets import QWidget, QHBoxLayout
        
        self.top_bar_widget = QWidget()
        self.top_bar_widget.setMaximumHeight(0)  # Hide the top bar
        top_bar_layout = QHBoxLayout(self.top_bar_widget)
        top_bar_layout.setContentsMargins(0, 0, 0, 0)
    
    def _create_toolbar(self):
        """Create a unified toolbar for common plot actions"""
        self.toolbar = QToolBar("Workspace", self)
        self.toolbar.setObjectName("WorkspaceToolBar")
        self.toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)
        
        self.clear_plots_action = self.toolbar.addAction("Clear Plots", self._handle_clear_plots)
        self.clear_plots_action.setStatusTip("Clear all rendered plots")
        
        # Data View action (moved from top bar)
        self.data_view_action = self.toolbar.addAction("Data View", self._on_data_view)
        self.data_view_action.setStatusTip("View imported data in table format")
        self.data_view_action.setEnabled(False)
        
        # Map to Test Data action (moved from top bar)
        self.map_data_action = self.toolbar.addAction("Map to Test Data", self._on_map_data)
        self.map_data_action.setStatusTip("Map imported data columns to test data structure")
        self.map_data_action.setEnabled(False)
        
        self.toolbar.addSeparator()
        
        self.export_plot_action = self.toolbar.addAction("Export Plot…", self._handle_export_single_plot)
        self.export_plot_action.setStatusTip("Export a specific plot to an image file")
        
        self.export_all_plots_action = self.toolbar.addAction("Export All Plots…", self._handle_export_all_plots)
        self.export_all_plots_action.setStatusTip("Export every plot to a directory")
        
        self.toolbar.addSeparator()
        
        self.export_preview_action = self.toolbar.addAction("Export Preview…", self._handle_export_preview)
        self.export_preview_action.setStatusTip("Export the current selection preview canvases")

    def _update_toolbar_state(self, index=None):
        """Enable or disable toolbar actions based on the active tab"""
        enable_data_actions = self.tab_widget.currentWidget() == getattr(self, 'data_tab', None)
        data_actions = [
            getattr(self, 'clear_plots_action', None),
            getattr(self, 'export_plot_action', None),
            getattr(self, 'export_all_plots_action', None),
        ]
        for action in data_actions:
            if isinstance(action, QAction):
                action.setEnabled(enable_data_actions)

    def _show_status(self, message, timeout=4000):
        """Update the status bar text"""
        self.statusBar().showMessage(message, timeout)

    def show_error(self, message, exception=None):
        """Display a critical error dialog and log the issue"""
        if exception:
            logger.exception(message, exc_info=exception)
        else:
            logger.error(message)
        QMessageBox.critical(self, "Error", message)
        self._show_status(message, 5000)

    def _handle_clear_plots(self):
        """Toolbar action: clear plots"""
        self.data_tab.clear_all_plots()
        self._show_status("Plots cleared", 3000)

    def _handle_export_single_plot(self):
        """Toolbar action: export a single plot"""
        total = len(getattr(self.data_tab, 'canvases', []))
        if total == 0:
            self.show_error("No plots available to export.")
            return
        plot_number, ok = QInputDialog.getInt(
            self,
            "Export Plot",
            "Plot number:",
            1,
            1,
            total
        )
        if not ok:
            return
        result = self.data_tab.export_plot(plot_number - 1)
        if result:
            self._show_status(f"Plot {plot_number} exported to {result}", 4000)

    def _handle_export_all_plots(self):
        """Toolbar action: export every plot"""
        directory = QFileDialog.getExistingDirectory(self, "Select Export Folder")
        if not directory:
            return
        try:
            saved_files = self.data_tab.export_all_plots(directory)
        except Exception as exc:
            self.show_error("Failed to export all plots.", exc)
            return
        self._show_status(f"Saved {len(saved_files)} plots to {directory}", 5000)

    def _handle_export_preview(self):
        """Toolbar action: export selection previews"""
        try:
            self.selection_tab.preview_manager.export_preview_plots()
        except Exception as exc:
            self.show_error("Failed to export preview plots.", exc)
        else:
            self._show_status("Preview plots exported", 4000)

    def restore_settings(self):
        """Restore window geometry and child widget state"""
        geometry = self.settings.value("ui/geometry")
        if geometry:
            self.restoreGeometry(geometry)
        window_state = self.settings.value("ui/windowState")
        if window_state:
            self.restoreState(window_state)
        if hasattr(self, 'data_tab'):
            self.data_tab.restore_state(self.settings)
        if hasattr(self, 'selection_tab'):
            self.selection_tab.restore_state(self.settings)

    def save_settings(self):
        """Persist window geometry and child widget state"""
        self.settings.setValue("ui/geometry", self.saveGeometry())
        self.settings.setValue("ui/windowState", self.saveState())
        if hasattr(self, 'data_tab'):
            self.data_tab.save_state(self.settings)
        if hasattr(self, 'selection_tab'):
            self.selection_tab.save_state(self.settings)

    def closeEvent(self, event):
        """Ensure state is saved on exit"""
        self.save_settings()
        super().closeEvent(event)

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
    

    def _on_data_view(self):
        """Handle data view button click - show data in a dialog"""
        from data_view_dialog import DataViewDialog
        
        if not hasattr(self, 'imported_data'):
            self.statusBar().showMessage("No data imported yet", 3000)
            return
            
        # Create data view dialog
        dialog = DataViewDialog(self.imported_data, self.imported_file_path, self)
        dialog.exec()
    
    def _on_map_data(self):
        """Handle map data button click - open column mapping dialog"""
        from data_mapping_dialog import DataMappingDialog
        
        if not hasattr(self, 'imported_data'):
            self.statusBar().showMessage("No data imported yet", 3000)
            return
            
        # Create data mapping dialog
        dialog = DataMappingDialog(self.imported_data, self.data_tab.test_data_generator, self)
        if dialog.exec():
            # Data was mapped successfully
            self.statusBar().showMessage("Data mapped to test structure successfully", 3000)
            # Refresh the selection tab to show new data
            self.selection_tab.populate_tree()
