from PySide6.QtWidgets import (
    QMenuBar, QFileDialog, QMessageBox
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from color_picker import PlotObjectListDialog, PlotObjectStyleDialog


class MenuManager:
    """Menu management class - handles creation and functionality of application menu bar"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.style_menu = None

    def create_menu_bar(self):
        """Create menu bar with all required menus"""
        from config import LayoutConfig
        
        menubar = self.main_window.menuBar()
        
        # Apply menu styling from configuration
        menubar.setStyleSheet(LayoutConfig.get_menu_bar_style())
        
        # Create individual menus
        self.create_file_menu(menubar)
        self.create_style_menu(menubar)
        self.create_about_menu(menubar)

    def create_file_menu(self, menubar):
        """Create File menu with data loading options"""
        file_menu = menubar.addMenu("File")
        
        # Open Folder action
        open_folder_action = QAction("Open Folder", self.main_window)
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)
        
        # Open File action
        open_file_action = QAction("Open File", self.main_window)
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)
        
        file_menu.addSeparator()
        
        # Load .redo File action
        load_redo_action = QAction("Load .redo File", self.main_window)
        load_redo_action.triggered.connect(self.load_redo_file)
        file_menu.addAction(load_redo_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("Exit", self.main_window)
        exit_action.triggered.connect(self.main_window.close)
        file_menu.addAction(exit_action)

    def create_style_menu(self, menubar):
        """Create Style menu with global and individual plot styling options"""
        self.style_menu = menubar.addMenu("Style")
        
        # Connect menu show event to update content dynamically
        self.style_menu.aboutToShow.connect(self.update_plot_menu_items)
        
        # Initialize menu content
        self.update_plot_menu_items()

    def update_plot_menu_items(self):
        """Update Style menu plot options based on available plots"""
        if not self.style_menu:
            return
            
        self.style_menu.clear()
        plot_found = False
        
        # Only get plots from Data Tab
        try:
            if (hasattr(self.main_window, 'data_tab') and 
                self.main_window.data_tab is not None and
                hasattr(self.main_window.data_tab, 'canvases') and
                hasattr(self.main_window.data_tab, 'plot_titles')):
                
                canvases = getattr(self.main_window.data_tab, 'canvases', [])
                plot_titles = getattr(self.main_window.data_tab, 'plot_titles', [])
                
                if canvases and plot_titles and len(canvases) == len(plot_titles):
                    # Add global style option at the top
                    apply_all_action = QAction("🎨 Apply Style to All Plots", self.main_window)
                    apply_all_action.triggered.connect(self.open_global_style_dialog)
                    self.style_menu.addAction(apply_all_action)
                    
                    # Add separator
                    self.style_menu.addSeparator()
                    
                    # Add individual plot options
                    for i, (canvas, title) in enumerate(zip(canvases, plot_titles)):
                        if canvas is not None:
                            plot_action = QAction(f"📊 {title}", self.main_window)
                            plot_info = {
                                'canvas': canvas,
                                'title': title,
                                'index': i,
                                'source': 'data_tab'
                            }
                            plot_action.triggered.connect(lambda checked, info=plot_info: self.open_plot_objects(info))
                            self.style_menu.addAction(plot_action)
                            plot_found = True
        except Exception as e:
            # Log error but continue execution
            pass
            
        # If no plots found, add a disabled placeholder item
        if not plot_found:
            no_plots_action = QAction("No plots available", self.main_window)
            no_plots_action.setEnabled(False)
            self.style_menu.addAction(no_plots_action)

    def open_global_style_dialog(self):
        """Open global style settings dialog for all plots"""
        try:
            # Create virtual object info for global style dialog
            global_object_info = {
                'type': 'global',
                'object': None,
                'label': 'All Plots',
                'index': -1
            }
            
            style_dialog = PlotObjectStyleDialog(
                self.main_window, 
                global_object_info, 
                self.on_global_style_changed
            )
            style_dialog.setWindowTitle("Global Style Settings - Apply to All Plots")
            style_dialog.exec()
        except Exception as e:
            QMessageBox.warning(
                self.main_window,
                "Error",
                f"Could not open global style dialog. Error: {str(e)}"
            )

    def on_global_style_changed(self, object_info, style):
        """Global style change callback - apply to all plots"""
        try:
            if (hasattr(self.main_window, 'data_tab') and 
                self.main_window.data_tab is not None and
                hasattr(self.main_window.data_tab, 'canvases')):
                
                canvases = getattr(self.main_window.data_tab, 'canvases', [])
                applied_count = 0
                
                for i, canvas in enumerate(canvases):
                    if canvas is not None:
                        try:
                            # Get all line objects on canvas
                            lines = canvas.ax.get_lines()
                            
                            for line in lines:
                                # Apply style to each line
                                if 'color' in style:
                                    line.set_color(style['color'])
                                if 'linestyle' in style:
                                    line.set_linestyle(style['linestyle'])
                                if 'linewidth' in style:
                                    line.set_linewidth(style['linewidth'])
                                if 'alpha' in style:
                                    line.set_alpha(style['alpha'])
                                if 'marker' in style:
                                    line.set_marker(style['marker'])
                                if 'markersize' in style:
                                    line.set_markersize(style['markersize'])
                                if 'markerfacecolor' in style:
                                    line.set_markerfacecolor(style['markerfacecolor'])
                                if 'markeredgecolor' in style:
                                    line.set_markeredgecolor(style['markeredgecolor'])
                                if 'markeredgewidth' in style:
                                    line.set_markeredgewidth(style['markeredgewidth'])
                            
                            # Get all collection objects (scatter plots, etc.)
                            collections = canvas.ax.collections
                            
                            for collection in collections:
                                if 'color' in style:
                                    collection.set_facecolors(style['color'])
                                if 'alpha' in style:
                                    collection.set_alpha(style['alpha'])
                            
                            # Get all text objects on canvas
                            texts = canvas.ax.texts
                            
                            for text in texts:
                                if 'color' in style:
                                    text.set_color(style['color'])
                                if 'alpha' in style:
                                    text.set_alpha(style['alpha'])
                            
                            # Refresh canvas
                            canvas.draw()
                            applied_count += 1
                            
                        except Exception as e:
                            # Skip this canvas and continue with others
                            continue
                
                # Show success message
                QMessageBox.information(
                    self.main_window,
                    "Style Applied",
                    f"Style successfully applied to {applied_count} plots."
                )
                
        except Exception as e:
            QMessageBox.warning(
                self.main_window,
                "Error",
                f"Could not apply global style. Error: {str(e)}"
            )

    def refresh_style_menu(self):
        """Refresh Style menu - can be called after data loading"""
        if self.style_menu:
            self.update_plot_menu_items()

    def open_plot_objects(self, plot_info):
        """Open plot objects list dialog for individual plot styling"""
        try:
            object_dialog = PlotObjectListDialog(self.main_window, plot_info)
            object_dialog.exec()
        except Exception as e:
            QMessageBox.warning(
                self.main_window,
                "Error",
                f"Could not open plot objects. Error: {str(e)}"
            )

    def create_about_menu(self, menubar):
        """Create About menu with application information"""
        about_menu = menubar.addMenu("About")
        
        # About This App action
        about_app_action = QAction("About This App", self.main_window)
        about_app_action.triggered.connect(self.show_about_dialog)
        about_menu.addAction(about_app_action)

    def show_about_dialog(self):
        """Display about dialog with application information"""
        about_text = """
<h2>IPRESET GUI</h2>
<p><b>Author:</b> Mengqing Wang</p>
<p><b>XXXX:</b> XXXXX</p>
<br>
<p><b>Article DOI:</b></p>
<p>XXXXXXXXXXXXX</p>
<br>
<p><b>GitHub Repository:</b></p>
<p><a href="https://github.com/MengqingWangCUG/EZsciplot_GUI">https://github.com/MengqingWangCUG/EZsciplot_GUI</a></p>
<br>
<p><i>A comprehensive tool for SCI data analysis and visualization.</i></p>
        """
        
        msg_box = QMessageBox(self.main_window)
        msg_box.setWindowTitle("About IPRESET GUI")
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setText(about_text)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Set dialog size
        msg_box.setMinimumWidth(400)
        msg_box.setMinimumHeight(300)
        
        msg_box.exec()

    def open_folder(self):
        """Open folder selection dialog"""
        folder_path = QFileDialog.getExistingDirectory(
            self.main_window,
            "Select Data Folder",
            "",
            QFileDialog.Option.ShowDirsOnly
        )
        
        if folder_path:
            self.main_window.current_folder = folder_path
            self.main_window.current_file = ""
            self.main_window.update_status_display()
            self.main_window.load_data()

    def open_file(self):
        """Open file selection dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Select Data File",
            "",
            "All Files (*);;Text Files (*.txt);;Data Files (*.dat)"
        )
        
        if file_path:
            self.main_window.current_file = file_path
            self.main_window.current_folder = ""
            self.main_window.update_status_display()
            self.main_window.load_data()

    def load_redo_file(self):
        """Load .redo file dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Select .redo File",
            "",
            "Redo Files (*.redo);;All Files (*)"
        )
        
        if file_path:
            self.main_window.current_file = file_path
            self.main_window.current_folder = ""
            self.main_window.update_status_display()
            self.main_window.load_redo_data()