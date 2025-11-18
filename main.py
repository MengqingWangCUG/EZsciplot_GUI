import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    """
    Main program entry point
    
    This application is a PySide6-based scientific data viewer primarily used for viewing 
    and analyzing specimen data. The entire application consists of the following core modules.
   
    Flow:
    main.py -> main_window.py -> [data_tab.py, selection_tab.py]
                              -> menu_manager.py
                              -> mpl_canvas.py (used by data_tab and selection_tab)
                              -> preview_manager.py (used by selection_tab)
                              -> config.py (used by all modules)
                              -> entrance.py (test data generation)
                              -> app_manager.py (test application management)
                              -> color_picker.py (style customization)
    
    Supported Data Formats:
    - Text files (.txt)
    - CSV files (.csv) 
    - Data files (.dat)
    
    """
    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()