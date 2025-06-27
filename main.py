import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow


def main():
    """
    Main program entry point
    
    This application is a PySide6-based scientific data viewer primarily used for viewing 
    and analyzing specimen data. The entire application consists of the following core modules:
    
    1. main_window.py - Main Window Module
       Functional Controls:
       - Create main application window and layout
       - Manage tab switching (data view and specimen selection)
       - Maintain current data state (folder path, file path)
       - Provide data loading interfaces (folder, single file, .redo file)
       - Coordinate data transfer and state synchronization between modules
    
    2. menu_manager.py - Menu Management Module
       Functional Controls:
       - Create and manage application menu bar
       - File selection dialogs (select data folder, data file, .redo file)
       - Keyboard shortcut bindings (Ctrl+D for folder, Ctrl+O for file, etc.)
       - File type filtering and validation
       - Exit program functionality
    
    3. data_tab.py - Data View Tab Module
       Functional Controls:
       - Data status display (current site, specimen information)
       - Specimen navigation controls (previous/next buttons, keyboard arrow keys)
       - Data filter condition settings (four configurable filter parameters)
       - Plot area management (6 independent matplotlib canvases, 2-column 3-row layout)
       - Scroll control (mouse wheel vertical/horizontal scrolling with Shift/Ctrl modifiers)
       - Data display area (4 text boxes showing specimen detailed information)
       - Automatic data loading and chart updates
    
    4. selection_tab.py - Specimen Selection Tab Module
       Functional Controls:
       - Tree structure display of site and specimen hierarchical relationships
       - Batch selection operations (select all, deselect all, apply selection)
       - Selection preview plotting (matplotlib canvas displaying selected specimens)
       - Plot controls (update charts, clear charts, export charts)
       - Selection state management and validation
       - Prepare selected specimen data for subsequent analysis
    
    5. mpl_canvas.py - Matplotlib Canvas Wrapper Module
       Functional Controls:
       - Wrap matplotlib FigureCanvas as Qt widget
       - Provide standardized plotting interface
       - Automatic canvas size adjustment strategy
       - Provide unified plotting foundation for all plot areas
       - Support chart drawing, updating, and clearing operations
    
    6. preview_manager.py - Preview Management Module
       Functional Controls:
       - Manage selection preview plots in Selection Tab
       - Handle single site and all sites preview generation
       - Provide export functionality for preview plots
       - Coordinate with entrance.py for data visualization
       - Apply unified styling from configuration
    
    7. config.py - Configuration Management Module
       Functional Controls:
       - Centralized management of UI layout parameters and styles
       - Color schemes and styling configurations
       - Adaptive font sizing and responsive design settings
       - GroupBox and widget styling definitions
       - Theme management and style application methods
    
    8. entrance.py - Test Data and Application Launcher Module
       Functional Controls:
       - Generate test data for development and demonstration
       - Provide specimen data simulation with configurable parameters
       - Plot data generation and visualization methods
       - Application launcher for test mode
       - Statistical calculations and data processing utilities
    
    9. app_manager.py - Test Application Manager Module
       Functional Controls:
       - Create and configure test applications with custom parameters
       - Manage dynamic layout adjustments for different plot/parameter counts
       - Handle filter condition evaluation and visual feedback
       - Coordinate between test data and UI components
       - Provide testing and development utilities
    
    10. color_picker.py - Color Selection Module
        Functional Controls:
        - Adobe-style gradient color picker interface
        - HSV/RGB color space conversion and manipulation
        - Plot object style customization dialogs
        - Color palette management and preset colors
        - Style application to matplotlib objects
    
    Data Flow:
    main.py -> main_window.py -> [data_tab.py, selection_tab.py]
                              -> menu_manager.py
                              -> mpl_canvas.py (used by data_tab and selection_tab)
                              -> preview_manager.py (used by selection_tab)
                              -> config.py (used by all modules)
                              -> entrance.py (test data generation)
                              -> app_manager.py (test application management)
                              -> color_picker.py (style customization)
    
    User Interaction Workflow:
    1. Select data source through menu (folder or file)
    2. Browse and filter specimen data in data_tab
    3. Select specimens for analysis in selection_tab
    4. View real-time updated charts and data information
    5. Customize plot styles and export results
    
    Supported Data Formats:
    - Text files (.txt)
    - CSV files (.csv) 
    - Data files (.dat)
    - Redo files (.redo)
    
    Key Features:
    - Real-time data visualization with multiple plot types
    - Interactive specimen selection with tree hierarchy
    - Configurable filter conditions with visual feedback
    - Keyboard navigation and shortcuts
    - Export capabilities for plots and data
    - Responsive UI with adaptive styling
    - Test mode with simulated data for development
    """
    # Create application instance
    app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow()
    
    # Show window
    window.show()
    
    # Run application event loop
    sys.exit(app.exec())


if __name__ == '__main__':
    main()