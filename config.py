"""
Layout Configuration Module - Centralized management of all UI layout parameters and styles
"""


class LayoutConfig:
    """Layout configuration class - Centralized management of all UI layout parameters"""
    
    # Main window configuration
    MAIN_WINDOW = {
        'title': 'Specimen Viewer',
        'size': (1200, 800),
        'margins': (10, 10, 10, 10),
        'spacing': 5
    }
    
    # Range value configuration
    RANGE_VALUES = {
        'min': 1,
        'max': 100,
        'default_up': 100,
        'default_down': 1
    }
    
    # Data Tab configuration
    DATA_TAB = {
        # Top layout
        'top_layout_spacing': 15,
        
        # Current Specimen group configuration
        'specimen_group': {
            'title': 'Current Specimen',
            'max_width': 300,
            'min_width': 280,
            'margins': (8, 8, 8, 8),
            'spacing': 6,
            'label_width': 55,
            'combo_min_width': 130,
            'combo_max_height': 26,
            'button_width': 65,
            'button_max_height': 26
        },
        
        # Range Tab group configuration
        'range_group': {
            'title': 'Range Tab',
            'max_width': 200,
            'min_width': 180,
            'margins': (8, 8, 8, 8),
            'spacing': 6,
            'label_width': 65,
            'combo_min_width': 100,
            'combo_max_height': 26
        },
        
        # Data Filter group configuration
        'filter_group': {
            'title': 'Data Filter Conditions',
            'margins': (10, 10, 10, 10),
            'spacing': 8,
            'input_width': 60
        },
        
        # Plots container configuration
        'plots_container': {
            'title': 'Specimen Plots',
            'margins': (10, 10, 10, 10),
            'spacing': 5,
            'scroll_margins': (5, 5, 5, 5),
            'grid_spacing': 10,
            'plot_min_size': (350, 350),
            'plot_margins': (10, 10, 10, 10),
            'plot_spacing': 5,
            'control_spacing': 5,
            'button_max_width': 80,
            'canvas_min_size': (300, 300)
        },
        
        # Data display group configuration
        'data_group': {
            'title': 'Specimen Data',
            'min_width': 125,
            'max_width': 140,
            'margins': (6, 6, 6, 6),
            'spacing': 4,
            'container_spacing': 1,
            'display_min_height': 24,
            'display_max_height': 28
        }
    }
    
    # Selection Tab configuration
    SELECTION_TAB = {
        # Main layout
        'main_margins': (10, 10, 10, 10),
        'main_spacing': 10,
        'content_spacing': 15,
        'tree_plot_ratio': (1, 6),
        
        # Tree structure group configuration
        'tree_group': {
            'title': 'Sample Tree',
            'margins': (10, 10, 10, 10),
            'spacing': 8,
            'info_margins': 5,
            'button_spacing': 5,
            'button_max_width': 100
        },
        
        # Plot group configuration
        'plot_group': {
            'title': 'Selection Preview',
            'margins': (10, 10, 10, 10),
            'spacing': 8,
            'button_spacing': 5
        },
        
        # Preview group configuration
        'preview_group': {
            'title': 'Selection Preview',
            'min_width': 400,
            'max_width': 500,
            'margins': (10, 10, 10, 10),
            'spacing': 5,
            'canvas_size': (4, 3, 80)  # width, height, dpi
        }
    }
    
    # Main window style configuration - migrated from main_window.py
    MAIN_WINDOW_STYLES = {
        'main_window': {
            'background_color': '#f5f5f5',
            'color': '#000000'
        },
        'widget': {
            'background_color': '#f5f5f5',
            'color': '#000000',
            'font_family': '"Segoe UI", Arial, sans-serif'
        },
        'tab_widget': {
            'pane_border': '2px solid #333333',
            'pane_background': '#ffffff',
            'pane_margin_top': '-1px',
            'tab_bar_alignment': 'left',
            'tab_border': '1px solid #333333',
            'tab_padding': '8px 16px',
            'tab_margin_right': '2px',
            'tab_margin_bottom': '1px',
            'tab_background': '#f0f0f0',
            'tab_border_bottom': '1px solid #333333',
            'tab_selected_border_bottom': '1px solid #ffffff',
            'tab_selected_background': '#ffffff',
            'tab_selected_margin_bottom': '0px',
            'tab_hover_background': '#e6e6e6'
        }
    }
    
    # Menu style configuration - migrated from menu_manager.py
    MENU_STYLES = {
        'menu_bar': {
            'background_color': '#f0f0f0',
            'border_bottom': '1px solid #ccc'
        },
        'menu_bar_item': {
            'background_color': 'transparent',
            'padding': '5px 10px',
            'margin': '2px',
            'border': '2px solid #cccccc',  # Gray border
            'border_radius': '3px'
        },
        'menu_bar_item_selected': {
            'background_color': '#e0e0e0',
            'border': '2px solid #999999'  # Dark gray border
        },
        'menu_bar_item_pressed': {
            'background_color': '#d0d0d0'
        },
        'menu': {
            'border': '1px solid #999',
            'background_color': 'white'
        },
        'menu_item': {
            'padding': '5px 20px',
            'border': 'none'
        },
        'menu_item_selected': {
            'background_color': '#e0e0e0'
        }
    }
    
    # Selection Tab splitter style configuration - migrated from selection_tab.py
    SPLITTER_STYLES = {
        'splitter': {
            'handle_width': '0px',
            'handle_background': 'transparent'
        }
    }
    
    # Color picker style configuration - migrated from color_picker.py
    COLOR_PICKER_STYLES = {
        'color_preview': {
            'border': '1px solid #000',
            'border_radius': '3px'
        },
        'marker_preview': {
            'border': '1px solid black'
        }
    }
    
    # Basic control style configuration
    STYLES = {
        'label': {
            'font_weight': 'bold',
            'color': '#333333',
            'font_size': {
                'small': '9pt',
                'normal': '10pt',
                'medium': '10pt',
                'large': '12pt'
            }
        },
        'tree': {
            'background_color': '#ffffff',
            'border': '1px solid #cccccc',
            'selection_color': '#0078d4',
            'font_size': '9pt',
            'item_padding': '2px 4px'
        },
        'combobox': {
            'background_color': '#ffffff',
            'border': '1px solid #cccccc',
            'border_radius': '3px',
            'padding': '4px',
            'font_size': '9pt',
            'font_family': 'Arial, sans-serif',
            'focus_border': '2px solid #0078d4',
            'hover_bg': '#f0f0f0'
        },
        'button': {
            'background_color': '#f0f0f0',
            'border': '1px solid #cccccc',
            'border_radius': '3px',
            'padding': '4px 8px',
            'font_size': '9pt',
            'font_weight': 'normal',
            'color': '#333333',
            'hover_bg': '#e0e0e0',
            'pressed_bg': '#d0d0d0',
            'disabled_bg': '#f8f8f8',
            'disabled_color': '#999999',
            'min_height': '25px',
            'min_width': '80px'
        },
        'data_display': {
            'background_color': '#ffffff',
            'border': '1px solid #cccccc',
            'border_radius': '3px',
            'padding': '4px',
            'font_family': 'Arial, sans-serif',
            'font_size': '9pt',
            'font_weight': 'normal',
            'color': '#333333',
            'readonly_bg': '#f8f9fa'
        },
        'lineedit': {
            'background_color': '#ffffff',
            'border': '1px solid #cccccc',
            'border_radius': '3px',
            'padding': '4px',
            'font_size': '9pt',
            'font_family': 'Arial, sans-serif',
            'focus_border': '2px solid #0078d4'
        },
        # Filter condition color styles - migrated from app_manager.py
        'filter_colors': {
            'match_background': '#d4edda',     # Light green background (match)
            'match_border': '2px solid #28a745', # Green border (match)
            'match_text': '#0066cc',           # Blue text (match)
            'no_match_background': '#f8d7da',  # Light red background (no match)
            'no_match_border': '2px solid #dc3545', # Red border (no match)
            'no_match_text': '#cc0000',        # Red text (no match)
            'default_background': '#ffffff',   # Default white background
            'default_text': '#333333'          # Default black text
        },
        # Data label styles - migrated from app_manager.py
        'data_label': {
            'background_color': '#f0f0f0',
            'border': '1px solid #ccc',
            'border_radius': '3px',
            'padding': '2px',
            'fixed_height': '20px'
        }
    }
    
    # Color configuration
    COLORS = {
        'plot_colors': [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
    }
    
    # GroupBox style configuration - Unified control of all block borders and backgrounds
    GROUPBOX_STYLES = {
        'default': {
            'border': '1px solid #dddddd',
            'border_radius': '3px',
            'margin_top': '8px',
            'padding_top': '8px',
            'background_color': '#f5f5f5',  # Light gray background
            'title_color': '#333333',
            'title_font_weight': 'bold'
        },
        
        # Data Tab block styles
        'specimen_group': {
            'border': '1px solid #dddddd',
            'border_radius': '3px',
            'margin_top': '8px',
            'padding_top': '8px',
            'background_color': '#f5f5f5',  # Light gray background
            'title_color': '#333333',
            'title_font_weight': 'bold'
        },
        
        'range_group': {
            'border': '1px solid #dddddd',
            'border_radius': '3px',
            'margin_top': '8px',
            'padding_top': '8px',
            'background_color': '#f5f5f5',  # Light gray background
            'title_color': '#333333',
            'title_font_weight': 'bold'
        },
        
        'control_group': {
            'border': '1px solid #dddddd',
            'border_radius': '3px',
            'margin_top': '8px',
            'padding_top': '8px',
            'background_color': '#f5f5f5',  # Light gray background
            'title_color': '#333333',
            'title_font_weight': 'bold'
        },
        
        'data_display_group': {
            'border': '1px solid #dddddd',
            'border_radius': '3px',
            'margin_top': '8px',
            'padding_top': '8px',
            'background_color': '#f5f5f5',  # Light gray background
            'title_color': '#333333',
            'title_font_weight': 'bold'
        },
        
        'plots_container': {
            'border': '1px solid #dddddd',
            'border_radius': '3px',
            'margin_top': '8px',
            'padding_top': '8px',
            'background_color': '#f5f5f5',  # Light gray background
            'title_color': '#333333',
            'title_font_weight': 'bold'
        },
        
        'data_group': {
            'border': '1px solid #dddddd',
            'border_radius': '3px',
            'margin_top': '8px',
            'padding_top': '8px',
            'background_color': '#f5f5f5',  # Light gray background
            'title_color': '#333333',
            'title_font_weight': 'bold'
        },
        
        'filter_group': {
            'border': '1px solid #dddddd',
            'border_radius': '3px',
            'margin_top': '8px',
            'padding_top': '8px',
            'background_color': '#f5f5f5',  # Light gray background
            'title_color': '#333333',
            'title_font_weight': 'bold'
        },
        
        # Selection Tab block styles
        'tree_group': {
            'border': '1px solid #dddddd',
            'border_radius': '3px',
            'margin_top': '8px',
            'padding_top': '8px',
            'background_color': '#f5f5f5',  # Light gray background
            'title_color': '#333333',
            'title_font_weight': 'bold'
        },
        
        # Individual plot group styles
        'individual_plot': {
            'border': '1px solid #cccccc',
            'border_radius': '3px',
            'margin_top': '5px',
            'padding_top': '5px',
            'background_color': '#f8f8f8',  # Lighter gray
            'title_color': '#333333',
            'title_font_weight': 'normal'
        }
    }
    
    # Preview related style configuration
    PREVIEW_STYLES = {
        # Main preview group style
        'preview_group': {
            'title': 'Selection Preview',
            'min_width': 600,
            'max_width': 2000,
            'margins': (5, 5, 5, 5),
            'spacing': 5,
            'border': '1px solid #dddddd',
            'border_radius': '3px',
            'margin_top': '8px',
            'padding_top': '8px',
            'background_color': '#f5f5f5',  # Light gray
            'title_color': '#333333',
            'title_font_weight': 'bold'
        },
        
        # Single Site Preview group style
        'single_site_group': {
            'title': 'Single Site Preview',
            'border': '1px solid #dddddd',
            'border_radius': '3px',
            'margin_top': '8px',
            'padding_top': '8px',
            'background_color': '#f5f5f5',  # Light gray
            'title_color': '#333333',
            'title_font_weight': 'bold',
            'margins': (5, 5, 5, 5),
            'spacing': 5
        },
        
        # All Site Preview group style
        'all_site_group': {
            'title': 'All Site Preview',
            'border': '1px solid #dddddd',
            'border_radius': '3px',
            'margin_top': '8px',
            'padding_top': '8px',
            'background_color': '#f5f5f5',  # Light gray
            'title_color': '#333333',
            'title_font_weight': 'bold',
            'margins': (5, 5, 5, 5),
            'spacing': 5
        },
        
        # Site selector dropdown style
        'site_selector': {
            'label_text': 'Site:',
            'label_font_size': '9pt',
            'label_color': '#333333',
            'label_font_weight': 'normal',
            'combo_min_width': 130,
            'combo_background': '#ffffff',
            'combo_border': '1px solid #cccccc',
            'combo_border_radius': '3px',
            'combo_padding': '4px',
            'combo_font_size': '9pt',
            'combo_max_height': '26px',
            'combo_hover_bg': '#f0f0f0',
            'combo_focus_border': '2px solid #0078d4'
        },
        
        # Canvas style
        'canvas': {
            'width': 4,
            'height': 3,
            'dpi': 80,
            'background_color': '#ffffff',  # Keep canvas background white
            'border': '1px solid #dddddd',
            'border_radius': '2px'
        },
        
        # Export button style
        'export_button': {
            'text': 'Export Plots',
            'font_size': '9pt',
            'padding': '4px 8px',
            'background_color': '#f0f0f0',
            'color': '#333333',
            'border': '1px solid #cccccc',
            'border_radius': '3px',
            'font_weight': 'normal',
            'min_height': '25px',
            'min_width': '80px',
            'hover_bg': '#e0e0e0',
            'pressed_bg': '#d0d0d0',
            'disabled_bg': '#f8f8f8',
            'disabled_color': '#999999'
        }
    }
    
    # Adaptive font configuration
    ADAPTIVE_FONT = {
        'min_font_size': 6,      # Minimum font size
        'max_font_size': 12,     # Maximum font size
        'default_font_size': 9,  # Default font size
        'scaling_factor': 0.8,   # Scaling factor
        'enable_auto_scale': True  # Enable auto scaling
    }
    
    # Selection Tab style configuration
    SELECTION_TAB_STYLES = {
        # Tree widget style
        'tree_widget': {
            'background_color': '#ffffff',
            'border': '1px solid #cccccc',
            'selection_color': '#0078d4',
            'font_size': '9pt',
            'item_padding': '2px 4px',
            'item_height': '24px',
            'item_hover_bg': '#f0f0f0',
            'item_border_bottom': '1px solid #e0e0e0',
            'outline': 'none',
            'indentation': '20px',
            'root_decorated': True,
            'animated': True
        },
        
        # Tree widget branch style
        'tree_branch': {
            'background': 'transparent',
            'image': 'none',
            'border': 'none',
            'hover_bg': '#e6f3ff',
            'hover_border_radius': '3px',
            'closed_icon': '▶',
            'open_icon': '▼',
            'icon_color': '#666666',
            'icon_font_size': '12px',
            'icon_font_weight': 'bold',
            'icon_padding_left': '2px'
        },
        
        # Scroll area style
        'scroll_area': {
            'background_color': 'transparent',
            'border': 'none',
            'frame_shape': 'NoFrame'
        },
        
        # Vertical scrollbar style
        'vertical_scrollbar': {
            'background_color': '#f0f0f0',
            'width': '12px',
            'border_radius': '6px',
            'margin': '0px',
            'handle_bg': '#c0c0c0',
            'handle_min_height': '20px',
            'handle_border_radius': '6px',
            'handle_margin': '2px',
            'handle_hover_bg': '#a0a0a0',
            'handle_pressed_bg': '#808080',
            'add_line_height': '0px',
            'sub_line_height': '0px',
            'add_page_bg': 'none',
            'sub_page_bg': 'none'
        },
        
        # Horizontal scrollbar style
        'horizontal_scrollbar': {
            'background_color': '#f0f0f0',
            'height': '12px',
            'border_radius': '6px',
            'margin': '0px',
            'handle_bg': '#c0c0c0',
            'handle_min_width': '20px',
            'handle_border_radius': '6px',
            'handle_margin': '2px',
            'handle_hover_bg': '#a0a0a0',
            'handle_pressed_bg': '#808080',
            'add_line_width': '0px',
            'sub_line_width': '0px',
            'add_page_bg': 'none',
            'sub_page_bg': 'none'
        },
        
        # Selection info label style
        'selection_info': {
            'font_size': '9pt',
            'color': '#333333',
            'padding': '5px',
            'background_color': '#f0f0f0',
            'border': '1px solid #ccc',
            'border_radius': '3px',
            'fixed_height': '30px'
        },
        
        # Splitter style
        'splitter': {
            'handle_width': '0px',
            'handle_height': '0px',
            'handle_margin': '0px',
            'handle_padding': '0px',
            'handle_background': 'transparent'
        }
    }
    
    # Style generation methods
    @classmethod
    def get_main_window_style(cls):
        """Get main window style"""
        mw_style = cls.MAIN_WINDOW_STYLES
        return f"""
            QMainWindow {{
                background-color: {mw_style['main_window']['background_color']};
                color: {mw_style['main_window']['color']};
            }}
            
            QWidget {{
                background-color: {mw_style['widget']['background_color']};
                color: {mw_style['widget']['color']};
                font-family: {mw_style['widget']['font_family']};
            }}
        """
    
    @classmethod
    def get_tab_widget_style(cls):
        """Get Tab widget style"""
        tab_style = cls.MAIN_WINDOW_STYLES['tab_widget']
        return f"""
            QTabWidget::pane {{
                border: {tab_style['pane_border']};
                background-color: {tab_style['pane_background']};
                margin-top: {tab_style['pane_margin_top']};
            }}
            QTabWidget::tab-bar {{
                alignment: {tab_style['tab_bar_alignment']};
            }}
            QTabBar::tab {{
                border: {tab_style['tab_border']};
                padding: {tab_style['tab_padding']};
                margin-right: {tab_style['tab_margin_right']};
                margin-bottom: {tab_style['tab_margin_bottom']};
                background-color: {tab_style['tab_background']};
                border-bottom: {tab_style['tab_border_bottom']};
            }}
            QTabBar::tab:selected {{
                border-bottom: {tab_style['tab_selected_border_bottom']};
                background-color: {tab_style['tab_selected_background']};
                margin-bottom: {tab_style['tab_selected_margin_bottom']};
            }}
            QTabBar::tab:!selected {{
                background-color: {tab_style['tab_background']};
            }}
            QTabBar::tab:hover {{
                background-color: {tab_style['tab_hover_background']};
            }}
        """
    
    @classmethod
    def get_menu_bar_style(cls):
        """Get menu bar style"""
        menu_style = cls.MENU_STYLES
        return f"""
            QMenuBar {{
                background-color: {menu_style['menu_bar']['background_color']};
                border-bottom: {menu_style['menu_bar']['border_bottom']};
            }}
            QMenuBar::item {{
                background-color: {menu_style['menu_bar_item']['background_color']};
                padding: {menu_style['menu_bar_item']['padding']};
                margin: {menu_style['menu_bar_item']['margin']};
                border: {menu_style['menu_bar_item']['border']};
                border-radius: {menu_style['menu_bar_item']['border_radius']};
            }}
            QMenuBar::item:selected {{
                background-color: {menu_style['menu_bar_item_selected']['background_color']};
                border: {menu_style['menu_bar_item_selected']['border']};
            }}
            QMenuBar::item:pressed {{
                background-color: {menu_style['menu_bar_item_pressed']['background_color']};
            }}
            QMenu {{
                border: {menu_style['menu']['border']};
                background-color: {menu_style['menu']['background_color']};
            }}
            QMenu::item {{
                padding: {menu_style['menu_item']['padding']};
                border: {menu_style['menu_item']['border']};
            }}
            QMenu::item:selected {{
                background-color: {menu_style['menu_item_selected']['background_color']};
            }}
        """
    
    @classmethod
    def get_splitter_style(cls):
        """Get splitter style"""
        splitter_style = cls.SPLITTER_STYLES['splitter']
        return f"""
            QSplitter::handle {{
                width: {splitter_style['handle_width']};
                background: {splitter_style['handle_background']};
            }}
        """
    
    @classmethod
    def apply_theme(cls, theme_name='default'):
        """Apply theme to all block styles"""
        if theme_name not in cls.THEMES:
            theme_name = 'default'
        
        theme = cls.THEMES[theme_name]
        
        # Update border colors for all block styles
        for style_name in cls.GROUPBOX_STYLES:
            cls.GROUPBOX_STYLES[style_name]['border'] = f"{theme['border_width']} solid {theme['border_color']}"
            cls.GROUPBOX_STYLES[style_name]['background_color'] = theme['background']
    
    @classmethod
    def get_adaptive_font_size(cls, text, available_width, base_font_size=9):
        """Calculate adaptive font size based on available width"""
        if not cls.ADAPTIVE_FONT['enable_auto_scale']:
            return base_font_size
            
        # Estimate text width (rough calculation)
        char_width_ratio = 0.6  # Character width ratio
        estimated_width = len(text) * base_font_size * char_width_ratio
        
        if estimated_width <= available_width:
            return min(base_font_size, cls.ADAPTIVE_FONT['max_font_size'])
        
        # Calculate required font size
        scale_factor = available_width / estimated_width
        new_font_size = int(base_font_size * scale_factor * cls.ADAPTIVE_FONT['scaling_factor'])
        
        return max(cls.ADAPTIVE_FONT['min_font_size'], min(new_font_size, cls.ADAPTIVE_FONT['max_font_size']))
    
    @classmethod
    def get_tree_widget_style(cls):
        """Get tree widget style"""
        tree_style = cls.SELECTION_TAB_STYLES['tree_widget']
        branch_style = cls.SELECTION_TAB_STYLES['tree_branch']
        
        return f"""
            QTreeWidget {{
                background-color: {tree_style['background_color']};
                border: {tree_style['border']};
                selection-background-color: {tree_style['selection_color']};
                font-size: {tree_style['font_size']};
                outline: {tree_style['outline']};
            }}
            QTreeWidget::item {{
                padding: {tree_style['item_padding']};
                border-bottom: {tree_style['item_border_bottom']};
                height: {tree_style['item_height']};
            }}
            QTreeWidget::item:hover {{
                background-color: {tree_style['item_hover_bg']};
            }}
            QTreeWidget::item:selected {{
                background-color: {tree_style['selection_color']};
                color: white;
            }}
            
            /* Expand/collapse branch styles */
            QTreeWidget::branch {{
                background: {branch_style['background']};
            }}
            
            /* Branches with children that are open */
            QTreeWidget::branch:has-children:open {{
                background: {branch_style['background']};
                image: {branch_style['image']};
                border: {branch_style['border']};
            }}
            QTreeWidget::branch:has-children:open:hover {{
                background: {branch_style['hover_bg']};
                border-radius: {branch_style['hover_border_radius']};
            }}
            
            /* Branches with children that are closed */
            QTreeWidget::branch:has-children:closed {{
                background: {branch_style['background']};
                image: {branch_style['image']};
                border: {branch_style['border']};
            }}
            QTreeWidget::branch:has-children:closed:hover {{
                background: {branch_style['hover_bg']};
                border-radius: {branch_style['hover_border_radius']};
            }}
            
            /* Branches without children */
            QTreeWidget::branch:has-siblings:!has-children {{
                background: {branch_style['background']};
                image: {branch_style['image']};
                border: {branch_style['border']};
            }}
            
            /* Use Unicode symbols as expand/collapse indicators */
            QTreeWidget::branch:has-children:closed::before {{
                content: "{branch_style['closed_icon']}";
                color: {branch_style['icon_color']};
                font-size: {branch_style['icon_font_size']};
                font-weight: {branch_style['icon_font_weight']};
                padding-left: {branch_style['icon_padding_left']};
            }}
            QTreeWidget::branch:has-children:open::before {{
                content: "{branch_style['open_icon']}";
                color: {branch_style['icon_color']};
                font-size: {branch_style['icon_font_size']};
                font-weight: {branch_style['icon_font_weight']};
                padding-left: {branch_style['icon_padding_left']};
            }}
            
            /* Remove default branch lines */
            QTreeWidget::branch:has-siblings:adjoins-item,
            QTreeWidget::branch:!has-children:!has-siblings:adjoins-item,
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:has-children:!has-siblings:open {{
                border: {branch_style['border']};
                background: {branch_style['background']};
            }}
        """
    
    @classmethod
    def get_scroll_area_style(cls):
        """Get scroll area style"""
        scroll_style = cls.SELECTION_TAB_STYLES['scroll_area']
        v_scroll = cls.SELECTION_TAB_STYLES['vertical_scrollbar']
        h_scroll = cls.SELECTION_TAB_STYLES['horizontal_scrollbar']
        
        return f"""
            QScrollArea {{
                background-color: {scroll_style['background_color']};
                border: {scroll_style['border']};
            }}
            QScrollBar:vertical {{
                background-color: {v_scroll['background_color']};
                width: {v_scroll['width']};
                border-radius: {v_scroll['border_radius']};
                margin: {v_scroll['margin']};
            }}
            QScrollBar::handle:vertical {{
                background-color: {v_scroll['handle_bg']};
                min-height: {v_scroll['handle_min_height']};
                border-radius: {v_scroll['handle_border_radius']};
                margin: {v_scroll['handle_margin']};
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {v_scroll['handle_hover_bg']};
            }}
            QScrollBar::handle:vertical:pressed {{
                background-color: {v_scroll['handle_pressed_bg']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: {v_scroll['add_line_height']};
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: {v_scroll['add_page_bg']};
            }}
            QScrollBar:horizontal {{
                background-color: {h_scroll['background_color']};
                height: {h_scroll['height']};
                border-radius: {h_scroll['border_radius']};
                margin: {h_scroll['margin']};
            }}
            QScrollBar::handle:horizontal {{
                background-color: {h_scroll['handle_bg']};
                min-width: {h_scroll['handle_min_width']};
                border-radius: {h_scroll['handle_border_radius']};
                margin: {h_scroll['handle_margin']};
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {h_scroll['handle_hover_bg']};
            }}
            QScrollBar::handle:horizontal:pressed {{
                background-color: {h_scroll['handle_pressed_bg']};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: {h_scroll['add_line_width']};
            }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: {h_scroll['add_page_bg']};
            }}
        """
    
    @classmethod
    def get_selection_info_style(cls):
        """Get selection info label style"""
        info_style = cls.SELECTION_TAB_STYLES['selection_info']
        
        return f"""
            QLabel {{
                font-size: {info_style['font_size']};
                color: {info_style['color']};
                padding: {info_style['padding']};
                background-color: {info_style['background_color']};
                border: {info_style['border']};
                border-radius: {info_style['border_radius']};
            }}
        """
    
    @classmethod
    def get_selection_splitter_style(cls):
        """Get selection splitter style"""
        splitter_style = cls.SELECTION_TAB_STYLES['splitter']
        
        return f"""
            QSplitter::handle {{
                width: {splitter_style['handle_width']};
                height: {splitter_style['handle_height']};
                margin: {splitter_style['handle_margin']};
                padding: {splitter_style['handle_padding']};
                background: {splitter_style['handle_background']};
            }}
        """
    
    @classmethod
    def get_preview_group_style(cls):
        """Get main preview group style"""
        style = cls.PREVIEW_STYLES['preview_group']
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
    
    @classmethod
    def get_preview_subgroup_style(cls, group_type='single_site'):
        """Get preview subgroup style"""
        if group_type == 'single_site':
            style = cls.PREVIEW_STYLES['single_site_group']
        else:
            style = cls.PREVIEW_STYLES['all_site_group']
        
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
    
    @classmethod
    def get_site_selector_style(cls):
        """Get site selector style - unified with other dropdowns"""
        style = cls.PREVIEW_STYLES['site_selector']
        
        label_style = f"""
            QLabel {{
                font-size: {style['label_font_size']};
                color: {style['label_color']};
                font-weight: {style['label_font_weight']};
            }}
        """
        
        combo_style = f"""
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
        
        return {
            'label': label_style,
            'combo': combo_style
        }
    
    @classmethod
    def get_preview_export_button_style(cls):
        """Get preview export button style - unified with other buttons"""
        style = cls.PREVIEW_STYLES['export_button']
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
    
    @classmethod
    def get_preview_canvas_style(cls):
        """Get preview canvas style"""
        style = cls.PREVIEW_STYLES['canvas']
        return f"""
            QWidget {{
                background-color: {style['background_color']};
                border: {style['border']};
                border-radius: {style['border_radius']};
            }}
        """