import numpy as np
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGroupBox, QComboBox, QFileDialog, QMessageBox, QSizePolicy
)
from PySide6.QtCore import Qt
from mpl_canvas import MplCanvas


class PreviewManager:
    """Preview manager class - manages selection preview plots using unified configuration styles"""
    
    def __init__(self, main_window, selection_tab):
        self.main_window = main_window
        self.selection_tab = selection_tab
        self.config = selection_tab.config

    def create_preview_group(self):
        """Create selection preview group using configuration styles"""
        from config import LayoutConfig
        
        preview_config = LayoutConfig.PREVIEW_STYLES['preview_group']
        
        preview_group = QGroupBox(preview_config['title'])
        preview_group.setMinimumWidth(preview_config['min_width'])
        preview_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        preview_group.setStyleSheet(self._get_preview_group_style())
        
        layout = QVBoxLayout(preview_group)
        layout.setContentsMargins(*preview_config['margins'])
        layout.setSpacing(preview_config['spacing'])
        
        single_site_group = self.create_single_site_group()
        
        all_site_group = self.create_all_site_group()
        
        layout.addWidget(single_site_group, 1)  # Upper half
        layout.addWidget(all_site_group, 1)     # Lower half
        
        export_btn = self.create_export_button()
        layout.addWidget(export_btn)
        
        # Initialize preview plots
        self.populate_site_preview_combo()
        self.clear_preview_plots()
        
        return preview_group

    def create_single_site_group(self):
        """Create Single Site Preview group"""
        from config import LayoutConfig
        
        # Get configuration
        config = LayoutConfig.PREVIEW_STYLES['single_site_group']
        
        single_site_group = QGroupBox(config['title'])
        single_site_group.setStyleSheet(self._get_preview_subgroup_style('single_site'))
        
        single_site_layout = QVBoxLayout(single_site_group)
        single_site_layout.setContentsMargins(*config['margins'])
        single_site_layout.setSpacing(config['spacing'])
        
        # Site selection dropdown menu
        site_select_layout = self.create_site_selector()
        single_site_layout.addLayout(site_select_layout)
        
        # Single Site Preview canvas
        canvas_config = LayoutConfig.PREVIEW_STYLES['canvas']
        self.single_site_canvas = MplCanvas(
            width=canvas_config['width'], 
            height=canvas_config['height'], 
            dpi=canvas_config['dpi']
        )
        # Apply canvas style
        self.single_site_canvas.setStyleSheet(self._get_canvas_style())
        single_site_layout.addWidget(self.single_site_canvas)
        
        return single_site_group

    def create_all_site_group(self):
        """Create All Site Preview group"""
        from config import LayoutConfig
        
        # Get configuration
        config = LayoutConfig.PREVIEW_STYLES['all_site_group']
        
        all_site_group = QGroupBox(config['title'])
        all_site_group.setStyleSheet(self._get_preview_subgroup_style('all_site'))
        
        all_site_layout = QVBoxLayout(all_site_group)
        all_site_layout.setContentsMargins(*config['margins'])
        all_site_layout.setSpacing(config['spacing'])
        
        # All Site Preview canvas
        canvas_config = LayoutConfig.PREVIEW_STYLES['canvas']
        self.all_site_canvas = MplCanvas(
            width=canvas_config['width'], 
            height=canvas_config['height'], 
            dpi=canvas_config['dpi']
        )
        # Apply canvas style
        self.all_site_canvas.setStyleSheet(self._get_canvas_style())
        all_site_layout.addWidget(self.all_site_canvas)
        
        return all_site_group

    def create_site_selector(self):
        """Create site selector"""
        from config import LayoutConfig
        
        # Get style configuration
        selector_config = LayoutConfig.PREVIEW_STYLES['site_selector']
        
        site_select_layout = QHBoxLayout()
        
        # Label
        site_select_label = QLabel(selector_config['label_text'])
        site_select_label.setStyleSheet(self._get_site_selector_label_style())
        
        # Dropdown menu
        self.site_preview_combo = QComboBox()
        self.site_preview_combo.setMinimumWidth(selector_config['combo_min_width'])
        self.site_preview_combo.setStyleSheet(self._get_site_selector_combo_style())
        self.site_preview_combo.currentTextChanged.connect(self.on_preview_site_changed)
        
        site_select_layout.addWidget(site_select_label)
        site_select_layout.addWidget(self.site_preview_combo)
        site_select_layout.addStretch()
        
        return site_select_layout

    def create_export_button(self):
        """Create export button"""
        from config import LayoutConfig
        
        # Get button configuration
        button_config = LayoutConfig.PREVIEW_STYLES['export_button']
        
        export_btn = QPushButton(button_config['text'])
        export_btn.setStyleSheet(self._get_export_button_style())
        export_btn.clicked.connect(self.export_preview_plots)
        
        return export_btn

    # Style generation methods
    def _get_preview_group_style(self):
        """Get main preview group style"""
        from config import LayoutConfig
        style = LayoutConfig.PREVIEW_STYLES['preview_group']
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

    def _get_preview_subgroup_style(self, group_type='single_site'):
        """Get preview subgroup style"""
        from config import LayoutConfig
        if group_type == 'single_site':
            style = LayoutConfig.PREVIEW_STYLES['single_site_group']
        else:
            style = LayoutConfig.PREVIEW_STYLES['all_site_group']
        
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
                left: 8px;
                padding: 0 4px 0 4px;
                color: {style['title_color']};
                font-weight: {style['title_font_weight']};
            }}
        """

    def _get_site_selector_label_style(self):
        """Get site selector label style"""
        from config import LayoutConfig
        style = LayoutConfig.PREVIEW_STYLES['site_selector']
        return f"""
            QLabel {{
                font-size: {style['label_font_size']};
                color: {style['label_color']};
                font-weight: {style['label_font_weight']};
            }}
        """

    def _get_site_selector_combo_style(self):
        """Get site selector dropdown style"""
        from config import LayoutConfig
        style = LayoutConfig.PREVIEW_STYLES['site_selector']
        return f"""
            QComboBox {{
                background-color: {style['combo_background']};
                border: {style['combo_border']};
                border-radius: {style['combo_border_radius']};
                padding: {style['combo_padding']};
                font-size: {style['combo_font_size']};
                font-family: Arial, sans-serif;
                min-width: {style['combo_min_width']}px;
                max-height: {style['combo_max_height']};
            }}
            QComboBox:hover {{
                background-color: {style['combo_hover_bg']};
            }}
            QComboBox:focus {{
                border: {style['combo_focus_border']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: none;
                width: 0px;
                height: 0px;
            }}
            QComboBox::down-arrow:hover {{
                background-color: {style['combo_hover_bg']};
            }}
        """

    def _get_export_button_style(self):
        """Get export button style"""
        from config import LayoutConfig
        style = LayoutConfig.PREVIEW_STYLES['export_button']
        return f"""
            QPushButton {{
                font-size: {style['font_size']};
                padding: {style['padding']};
                background-color: {style['background_color']};
                color: {style['color']};
                border: {style['border']};
                border-radius: {style['border_radius']};
                font-weight: {style['font_weight']};
                min-height: {style['min_height']};
                min-width: {style['min_width']};
            }}
            QPushButton:disabled {{
                background-color: {style['disabled_bg']};
                color: {style['disabled_color']};
            }}
            QPushButton:enabled:hover {{
                background-color: {style['hover_bg']};
            }}
            QPushButton:enabled:pressed {{
                background-color: {style['pressed_bg']};
            }}
            QPushButton:focus {{
                outline: none;
            }}
        """

    def _get_canvas_style(self):
        """Get canvas style"""
        from config import LayoutConfig
        style = LayoutConfig.PREVIEW_STYLES['canvas']
        return f"""
            QWidget {{
                background-color: {style['background_color']};
                border: {style['border']};
                border-radius: {style['border_radius']};
            }}
        """

    def populate_site_preview_combo(self):
        """Populate site preview dropdown menu"""
        if not hasattr(self, 'site_preview_combo'):
            return
            
        self.site_preview_combo.clear()
        self.site_preview_combo.addItem("Select a site...")
        
        if hasattr(self.main_window, 'data_tab') and hasattr(self.main_window.data_tab, 'sample_data'):
            sample_data = self.main_window.data_tab.sample_data
            for site_name in sample_data.keys():
                self.site_preview_combo.addItem(site_name)

    def on_preview_site_changed(self, site_name):
        """Handle preview site selection change"""
        self.update_single_site_preview(site_name)

    def clear_preview_plots(self):
        """Clear preview plots"""
        # Clear Single Site Preview
        self.single_site_canvas.ax.clear()
        self.single_site_canvas.ax.set_title('Single Site Preview - Select a site')
        self.single_site_canvas.ax.text(0.5, 0.5, 'Select a site from dropdown above', 
                                       ha='center', va='center', transform=self.single_site_canvas.ax.transAxes,
                                       fontsize=10, color='gray')
        self.single_site_canvas.draw()
        
        # Clear All Site Preview
        self.all_site_canvas.ax.clear()
        self.all_site_canvas.ax.set_title('All Site Preview - No data')
        self.all_site_canvas.ax.text(0.5, 0.5, 'No data available', 
                                    ha='center', va='center', transform=self.all_site_canvas.ax.transAxes,
                                    fontsize=10, color='gray')
        self.all_site_canvas.draw()

    def get_current_range_settings(self):
        """Get current range settings"""
        range_up = 100
        range_down = 1
        if hasattr(self.main_window, 'data_tab'):
            if hasattr(self.main_window.data_tab, 'range_up_combo'):
                try:
                    range_up = int(self.main_window.data_tab.range_up_combo.currentText())
                    range_down = int(self.main_window.data_tab.range_down_combo.currentText())
                except:
                    pass
        return range_up, range_down

    def update_single_site_preview(self, site_name):
        """Update Single Site Preview using current range settings for data box compatibility"""
        if site_name == "Select a site..." or not site_name:
            self.single_site_canvas.ax.clear()
            self.single_site_canvas.ax.set_title('Single Site Preview - Select a site')
            self.single_site_canvas.ax.text(0.5, 0.5, 'Select a site from dropdown above', 
                                           ha='center', va='center', transform=self.single_site_canvas.ax.transAxes,
                                           fontsize=10, color='gray')
            self.single_site_canvas.draw()
            return
        
        if not hasattr(self.main_window, 'data_tab') or not hasattr(self.main_window.data_tab, 'test_data_generator'):
            return
        
        test_data = self.main_window.data_tab.test_data_generator
        selected_items = self.selection_tab.get_selected_items()
        
        range_up, range_down = self.get_current_range_settings()
        
        # Generate plot data using range-affected methods (matches data box calculations)
        plot_data = test_data.generate_single_site_plot_data(site_name, selected_items, range_up, range_down)
        
        # Use entrance.py plotting methods
        test_data.plot_selection_preview_data(self.single_site_canvas, plot_data)

    def update_all_site_preview(self):
        """Update All Site Preview using current range settings for data box compatibility"""
        if not hasattr(self.main_window, 'data_tab') or not hasattr(self.main_window.data_tab, 'test_data_generator'):
            return
        
        test_data = self.main_window.data_tab.test_data_generator
        selected_items = self.selection_tab.get_selected_items()
        
        # 使用当前的 range 设置（这样预览数据会基于 data box 的结果）
        range_up, range_down = self.get_current_range_settings()
        
        # Generate plot data using range-affected methods (matches data box calculations)
        plot_data = test_data.generate_all_sites_plot_data(selected_items, range_up, range_down)
        
        # Use entrance.py plotting methods
        test_data.plot_selection_preview_data(self.all_site_canvas, plot_data)

    def update_selection_preview(self):
        """Update selection preview - replacement for the original update_selection_plot"""
        # Update Single Site Preview
        current_site = self.site_preview_combo.currentText()
        if current_site != "Select a site...":
            self.update_single_site_preview(current_site)
        
        # Update All Site Preview
        self.update_all_site_preview()

    def export_preview_plots(self):
        """Export preview plots"""
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Export Preview Plots",
            "preview_plots.png",
            "PNG Files (*.png);;PDF Files (*.pdf);;SVG Files (*.svg);;All Files (*)"
        )
        
        if file_path:
            try:
                # Create combined plot
                import matplotlib.pyplot as plt
                
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
                
                # Copy Single Site Preview
                for line in self.single_site_canvas.ax.get_lines():
                    ax1.plot(line.get_xdata(), line.get_ydata(), 
                            color=line.get_color(), linestyle=line.get_linestyle(), 
                            linewidth=line.get_linewidth(), alpha=line.get_alpha())
                
                for collection in self.single_site_canvas.ax.collections:
                    if hasattr(collection, 'get_offsets') and len(collection.get_offsets()) > 0:
                        ax1.scatter(collection.get_offsets()[:, 0], collection.get_offsets()[:, 1])
                
                ax1.set_title(self.single_site_canvas.ax.get_title())
                ax1.set_xlabel(self.single_site_canvas.ax.get_xlabel())
                ax1.set_ylabel(self.single_site_canvas.ax.get_ylabel())
                ax1.grid(True, alpha=0.3)
                
                # Copy All Site Preview
                for line in self.all_site_canvas.ax.get_lines():
                    ax2.plot(line.get_xdata(), line.get_ydata(), 
                            color=line.get_color(), linestyle=line.get_linestyle(), 
                            linewidth=line.get_linewidth(), alpha=line.get_alpha())
                
                for collection in self.all_site_canvas.ax.collections:
                    if hasattr(collection, 'get_offsets'):
                        ax2.scatter(collection.get_offsets()[:, 0], collection.get_offsets()[:, 1])
                
                ax2.set_title(self.all_site_canvas.ax.get_title())
                ax2.set_xlabel(self.all_site_canvas.ax.get_xlabel())
                ax2.set_ylabel(self.all_site_canvas.ax.get_ylabel())
                ax2.grid(True, alpha=0.3)
                
                plt.tight_layout()
                plt.savefig(file_path, dpi=300, bbox_inches='tight')
                plt.close()
                
                QMessageBox.information(None, "Export Success", f"Plots exported to: {file_path}")
                
            except Exception as e:
                QMessageBox.warning(None, "Export Error", f"Error exporting plots: {e}")