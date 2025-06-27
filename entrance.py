import sys
import numpy as np
import re
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon


class TestData:
    """Test data generator for scientific specimen analysis and visualization"""
    
    def __init__(self, num_plots=8, num_params=5, custom_param_labels=None):
        """
        Initialize test data generator
        
        Args:
            num_plots (int): Number of plots to generate
            num_params (int): Number of parameters for filtering
            custom_param_labels (list): Custom parameter labels
        """
        self.num_plots = num_plots
        self.num_params = num_params
        
        # Site and specimen data structure
        self.sites = {
            "Site A": ["Sample A1", "Sample A2", "Sample A3"],
            "Site B": ["Sample B1", "Sample B2"],
            "Site C": ["Sample C1", "Sample C2", "Sample C3", "Sample C4"],
            "Site D": ["Sample D1", "Sample D2"]
        }
        
        # Generate parameter labels based on num_params and custom labels
        if custom_param_labels and len(custom_param_labels) >= num_params:
            self.parameter_labels = custom_param_labels[:num_params]
        else:
            default_labels = [
                "Temperature", "Pressure", "Humidity", "Voltage", "Current",
                "Resistance", "Frequency", "Amplitude", "Phase", "Power"
            ]
            self.parameter_labels = []
            for i in range(num_params):
                if i < len(default_labels):
                    self.parameter_labels.append(default_labels[i])
                else:
                    self.parameter_labels.append(f"Param {i+1}")
        
        # Data display labels correspond to parameter labels
        self.data_display_labels = self.parameter_labels.copy()
        
        # Dynamically generate plot titles based on num_plots
        self.plot_titles = [f"Plot {i+1}" for i in range(self.num_plots)]
        
        # Add data caching system
        self.data_cache = {}
        self._initialize_all_data()
    
    def _initialize_all_data(self):
        """
        Initialize all specimen data once and cache it
        """
        print("Initializing all specimen data...")
        
        # Set random seed for reproducible results
        np.random.seed(42)
        
        # Generate data for all sites and specimens
        for site_name, specimens in self.sites.items():
            for specimen in specimens:
                # Create cache key
                cache_key = f"{site_name}_{specimen}"
                
                # Generate all plot data for this specimen
                specimen_data = {}
                for i in range(self.num_plots):
                    plot_key = f'plot{i+1}'
                    specimen_data[plot_key] = self._generate_single_plot_data(i, specimen, site_name)
                
                # Cache the data
                self.data_cache[cache_key] = specimen_data
        
        print(f"Data initialization complete. Cached {len(self.data_cache)} specimens.")
    
    def _generate_single_plot_data(self, plot_index, specimen, site_name):
        """
        Generate data for a single plot with deterministic randomness
        
        Args:
            plot_index (int): Index of the plot (0-based)
            specimen (str): Name of the specimen
            site_name (str): Name of the site
            
        Returns:
            dict: Plot data with x, y values and metadata
        """
        # Create deterministic seed based on site + specimen + plot_index
        seed_string = f"{site_name}_{specimen}_{plot_index}"
        seed = abs(hash(seed_string)) % (2**32)
        np.random.seed(seed)
        
        plot_types = [
            self._generate_sin_data,
            self._generate_exp_data,
            self._generate_multi_line_data,
            self._generate_polynomial_data,
            self._generate_gaussian_data,
            self._generate_log_data,
            self._generate_damped_oscillation_data,
            self._generate_spiral_data,
            self._generate_noise_data,
            self._generate_step_data
        ]
        
        plot_func = plot_types[plot_index % len(plot_types)]
        return plot_func(plot_index + 1, specimen)
    
    def clear_data_cache(self):
        """
        Clear the data cache and regenerate all data
        """
        print("Clearing data cache and regenerating...")
        self.data_cache.clear()
        self._initialize_all_data()
    
    def get_cache_info(self):
        """
        Get information about the data cache
        
        Returns:
            dict: Cache information
        """
        total_specimens = sum(len(specimens) for specimens in self.sites.values())
        cached_specimens = len(self.data_cache)
        
        return {
            'total_specimens': total_specimens,
            'cached_specimens': cached_specimens,
            'cache_complete': cached_specimens == total_specimens,
            'sites': list(self.sites.keys()),
            'cached_keys': list(self.data_cache.keys())
        }

    def format_significant_figures(self, value, sig_figs=5):
        """
        Format number to specified significant figures with scientific notation when appropriate
        
        Args:
            value: Numeric value to format
            sig_figs (int): Number of significant figures (default: 5)
            
        Returns:
            str: Formatted string with significant figures
        """
        try:
            val = float(value)
            if val == 0:
                return "0.0000"
            
            # Calculate the order of magnitude
            magnitude = int(np.floor(np.log10(abs(val))))
            
            # Use scientific notation for very large or very small numbers
            if magnitude >= 4 or magnitude < -2:
                # Scientific notation
                mantissa = val / (10 ** magnitude)
                formatted_mantissa = f"{mantissa:.{sig_figs-1}f}"
                return f"{formatted_mantissa}e{magnitude:+d}"
            else:
                # Regular notation with significant figures
                if magnitude >= 0:
                    # Number >= 1
                    decimal_places = max(0, sig_figs - magnitude - 1)
                    return f"{val:.{decimal_places}f}"
                else:
                    # Number < 1
                    decimal_places = sig_figs - magnitude - 1
                    return f"{val:.{decimal_places}f}"
                    
        except (ValueError, TypeError):
            return str(value)

    def parse_formatted_value(self, formatted_str):
        """
        Parse formatted string back to float value
        
        Args:
            formatted_str (str): Formatted string with significant figures
            
        Returns:
            float: Parsed numeric value
        """
        try:
            # Handle scientific notation
            if 'e' in formatted_str.lower():
                return float(formatted_str)
            else:
                return float(formatted_str)
        except (ValueError, TypeError):
            return 0.0

    def parse_filter_expression(self, expression):
        """
        Parse filter expression into operator and value
        
        Args:
            expression (str): Filter expression (e.g., ">5", "<=10")
            
        Returns:
            tuple: (operator, value) or None if invalid
        """
        if not expression or not expression.strip():
            return None
            
        expression = expression.strip()
        
        # Define supported operators in order of precedence
        patterns = [
            (r'^>=\s*(-?\d+\.?\d*)$', '>='),
            (r'^<=\s*(-?\d+\.?\d*)$', '<='),
            (r'^!=\s*(-?\d+\.?\d*)$', '!='),
            (r'^>\s*(-?\d+\.?\d*)$', '>'),
            (r'^<\s*(-?\d+\.?\d*)$', '<'),
            (r'^=\s*(-?\d+\.?\d*)$', '='),
            (r'^(-?\d+\.?\d*)$', '='),
        ]
        
        for pattern, operator in patterns:
            match = re.match(pattern, expression)
            if match:
                try:
                    value = float(match.group(1))
                    return (operator, value)
                except (ValueError, IndexError):
                    continue
        
        return None

    def check_parameter_condition_independently(self, site, specimen, parameter_index, condition_str, range_up=100, range_down=1):
        """
        Check parameter condition using string-based comparison for exact matching
        """
        # Validate parameter index
        if parameter_index < 0 or parameter_index >= len(self.parameter_labels):
            return True  # Invalid index, default to pass
        
        param_label = self.parameter_labels[parameter_index]
        
        # If no condition specified, parameter passes
        if not condition_str or not condition_str.strip():
            return True
        
        # Get specimen summary for this range
        specimen_summary = self.get_range_based_specimen_summary(site, specimen, range_up, range_down)
        specimen_value_str = specimen_summary.get(param_label, '0')
        
        # Parse the condition
        parsed = self.parse_filter_expression(condition_str)
        if not parsed:
            return True  # Invalid condition format, default to pass
        
        operator, threshold = parsed
        
        try:
            if specimen_value_str == 'N/A' or not specimen_value_str:
                return True  # No valid value, default to pass
            
            # For equality comparison, use string exact matching
            if operator == '=':
                # Format threshold to same format as display value
                threshold_formatted = self.format_significant_figures(threshold, 5)
                
                print(f"Debug: Parameter '{param_label}' - Display Value: '{specimen_value_str}', Formatted Threshold: '{threshold_formatted}', Condition: {operator}")
                
                # String exact comparison
                result = specimen_value_str.strip() == threshold_formatted.strip()
                
                print(f"Debug: String comparison result = {result}")
                return result
            
            # For other comparison operations, use numerical comparison
            specimen_value = self.parse_formatted_value(specimen_value_str)
            threshold_value = float(threshold)
            
            print(f"Debug: Parameter '{param_label}' - Display Value: '{specimen_value_str}' ({specimen_value}), Threshold: {threshold_value}, Condition: {operator}")
            
            if operator == '>':
                result = specimen_value > threshold_value
            elif operator == '>=':
                result = specimen_value >= threshold_value
            elif operator == '<':
                result = specimen_value < threshold_value
            elif operator == '<=':
                result = specimen_value <= threshold_value
            elif operator == '!=':
                # Use string comparison for inequality to ensure precision
                threshold_formatted = self.format_significant_figures(threshold_value, 5)
                result = specimen_value_str.strip() != threshold_formatted.strip()
            else:
                result = True
            
            print(f"Debug: Result = {result}")
            return result

        except (ValueError, TypeError) as e:
            print(f"Debug: Error parsing value '{specimen_value_str}': {e}")
            return True

    def evaluate_condition_normalized(self, specimen_value, operator, threshold_value):
        """
        Evaluate condition using normalized values (5 significant figures)
        """
        try:
            specimen_val = float(specimen_value)
            threshold_val = float(threshold_value)
            
            print(f"Evaluating: {specimen_val} {operator} {threshold_val}")
            
            if operator == '>':
                result = specimen_val > threshold_val
            elif operator == '>=':
                result = specimen_val >= threshold_val
            elif operator == '<':
                result = specimen_val < threshold_val
            elif operator == '<=':
                result = specimen_val <= threshold_val
            elif operator == '=':
                # Use small absolute error for equality
                result = abs(specimen_val - threshold_val) < 1e-8
            elif operator == '!=':
                # Use small absolute error for inequality
                result = abs(specimen_val - threshold_val) >= 1e-8
            else:
                result = True
            
            print(f"Result: {result}")
            return result
        
        except (ValueError, TypeError) as e:
            print(f"Error in evaluation: {e}")
            return True

    def evaluate_condition(self, specimen_value, operator, threshold_value):
        """
        Evaluate condition expression against specimen value
        """
        return self.evaluate_condition_normalized(specimen_value, operator, threshold_value)

    def generate_plot_data(self, plot_index, sample_name):
        """
        Get cached plot data (for backward compatibility)
        
        Args:
            plot_index (int): Index of the plot (0-based)
            sample_name (str): Name of the sample
            
        Returns:
            dict: Plot data with x, y values and metadata
        """
        # Find the site for this sample
        site_name = None
        for site, specimens in self.sites.items():
            if sample_name in specimens:
                site_name = site
                break
        
        if site_name is None:
            # Fallback: generate data directly if not found in cache
            return self._generate_single_plot_data(plot_index, sample_name, "Unknown")
        
        # Get from cache
        cache_key = f"{site_name}_{sample_name}"
        if cache_key in self.data_cache:
            plot_key = f'plot{plot_index + 1}'
            return self.data_cache[cache_key].get(plot_key, {})
        
        # Fallback
        return self._generate_single_plot_data(plot_index, sample_name, site_name)

    def generate_specimen_data_for_data_box(self, site, specimen):
        """
        Get cached specimen data for data box calculations
        
        Args:
            site (str): Site name
            specimen (str): Specimen name
            
        Returns:
            dict: Complete dataset for all plots of the specimen
        """
        cache_key = f"{site}_{specimen}"
        
        if cache_key in self.data_cache:
            return self.data_cache[cache_key]
        else:
            print(f"Warning: Data not found in cache for {site} - {specimen}")
            # Regenerate if not in cache
            specimen_data = {}
            for i in range(self.num_plots):
                plot_key = f'plot{i+1}'
                specimen_data[plot_key] = self._generate_single_plot_data(i, specimen, site)
            
            # Cache it for future use
            self.data_cache[cache_key] = specimen_data
            return specimen_data

    def generate_specimen_data_full_range(self, site, specimen):
        """
        Get cached specimen data using full data range
        
        Args:
            site (str): Site name
            specimen (str): Specimen name
            
        Returns:
            dict: Complete dataset for all plots of the specimen using full range
        """
        # Same as data_box version since we cache the raw data
        return self.generate_specimen_data_for_data_box(site, specimen)

    def generate_specimen_data(self, site, specimen):
        """
        Get cached specimen data (for backward compatibility)
        
        Args:
            site (str): Site name
            specimen (str): Specimen name
            
        Returns:
            dict: Complete dataset for all plots of the specimen
        """
        return self.generate_specimen_data_full_range(site, specimen)

    def calculate_range_based_averages(self, site, specimen, range_up=100, range_down=1):
        """
        Calculate range-based averages based on Range Tab settings
        
        Args:
            site (str): Site name
            specimen (str): Specimen name
            range_up (int): Upper range limit
            range_down (int): Lower range limit
            
        Returns:
            dict: Range-based statistics for all plots
        """        
        specimen_data = self.generate_specimen_data_for_data_box(site, specimen)
        
        range_averages = {
            'site': site,
            'specimen': specimen,
            'range_up': range_up,
            'range_down': range_down,
            'plot_averages': {},
            'overall_statistics': {}
        }
        
        all_y_values = []
        
        for i in range(self.num_plots):
            plot_key = f'plot{i+1}'
            if plot_key in specimen_data:
                data = specimen_data[plot_key]
                x_values = data['x']
                
                if 'y1' in data and 'y2' in data:
                    # Multi-line data processing
                    y1_values = data['y1']
                    y2_values = data['y2']
                    
                    range_mask = (x_values >= range_down) & (x_values <= range_up)
                    
                    if np.any(range_mask):
                        y1_range = y1_values[range_mask]
                        y2_range = y2_values[range_mask]
                        x_range = x_values[range_mask]
                        
                        y1_avg = np.mean(y1_range)
                        y2_avg = np.mean(y2_range)
                        combined_avg = np.mean(np.concatenate([y1_range, y2_range]))
                        
                        range_averages['plot_averages'][plot_key] = {
                            'type': 'multi_line',
                            'x_range_count': len(x_range),
                            'y1_average': float(y1_avg),
                            'y2_average': float(y2_avg),
                            'combined_average': float(combined_avg),
                            'y1_std': float(np.std(y1_range)),
                            'y2_std': float(np.std(y2_range)),
                            'x_range': [float(np.min(x_range)), float(np.max(x_range))]
                        }
                        
                        all_y_values.extend(y1_range)
                        all_y_values.extend(y2_range)
                    else:
                        range_averages['plot_averages'][plot_key] = {
                            'type': 'multi_line',
                            'error': 'No data points in specified range'
                        }
                else:
                    # Single-line data processing
                    y_values = data['y']
                    
                    range_mask = (x_values >= range_down) & (x_values <= range_up)
                    
                    if np.any(range_mask):
                        y_range = y_values[range_mask]
                        x_range = x_values[range_mask]
                        
                        y_avg = np.mean(y_range)
                        y_std = np.std(y_range)
                        y_min = np.min(y_range)
                        y_max = np.max(y_range)
                        y_median = np.median(y_range)
                        
                        range_averages['plot_averages'][plot_key] = {
                            'type': 'single_line',
                            'x_range_count': len(x_range),
                            'y_average': float(y_avg),
                            'y_std': float(y_std),
                            'y_min': float(y_min),
                            'y_max': float(y_max),
                            'y_median': float(y_median),
                            'x_range': [float(np.min(x_range)), float(np.max(x_range))]
                        }
                        
                        all_y_values.extend(y_range)
                    else:
                        range_averages['plot_averages'][plot_key] = {
                            'type': 'single_line',
                            'error': 'No data points in specified range'
                        }
        
        # Calculate overall statistics across all plots
        if all_y_values:
            all_y_array = np.array(all_y_values)
            range_averages['overall_statistics'] = {
                'total_data_points': len(all_y_values),
                'overall_average': float(np.mean(all_y_array)),
                'overall_std': float(np.std(all_y_array)),
                'overall_min': float(np.min(all_y_array)),
                'overall_max': float(np.max(all_y_array)),
                'overall_median': float(np.median(all_y_array)),
                'range_coverage': f"{range_down} to {range_up}",
                'valid_plots': len([p for p in range_averages['plot_averages'].values() if 'error' not in p])
            }
        else:
            range_averages['overall_statistics'] = {
                'error': 'No valid data points found in any plot within specified range'
            }
        
        return range_averages

    def get_range_based_specimen_summary(self, site, specimen, range_up=100, range_down=1):
        """
        Get range-based specimen summary data - display average values for each parameter
        """
        range_averages = self.calculate_range_based_averages(site, specimen, range_up, range_down)
        
        summary = {}
        
        for i in range(self.num_params):
            label = self.data_display_labels[i]
            
            # Each parameter displays the average value of the corresponding plot
            plot_index = i  # The i-th parameter displays the average of the (i+1)-th plot
            if plot_index < self.num_plots:
                plot_key = f'plot{plot_index + 1}'
                if (plot_key in range_averages['plot_averages'] and 
                    'error' not in range_averages['plot_averages'][plot_key]):
                    
                    plot_data = range_averages['plot_averages'][plot_key]
                    
                    if plot_data['type'] == 'multi_line':
                        # Multi-line data: display combined average
                        if 'combined_average' in plot_data:
                            avg_val = plot_data['combined_average']
                            formatted_val = self.format_significant_figures(avg_val, 5)
                            summary[label] = formatted_val
                        else:
                            summary[label] = 'N/A'
                    else:
                        # Single-line data: display y average
                        if 'y_average' in plot_data:
                            avg_val = plot_data['y_average']
                            formatted_val = self.format_significant_figures(avg_val, 5)
                            summary[label] = formatted_val
                        else:
                            summary[label] = 'N/A'
                else:
                    summary[label] = 'N/A'  # No data in range for this plot
            else:
                summary[label] = 'N/A'  # Exceeds plot count
        
        return summary

    # Data generation methods
    def _generate_sin_data(self, plot_num, sample_name):
        """Generate sine wave data"""
        x = np.linspace(0, 10, 50)
        y = np.sin(x + plot_num * 0.5) + 0.1 * np.random.random(50)
        
        return {
            'x': x,
            'y': y,
            'title': f'Plot {plot_num} - {sample_name}',
            'xlabel': 'X Values',
            'ylabel': 'Y Values'
        }
    
    def _generate_exp_data(self, plot_num, sample_name):
        """Generate exponential decay data"""
        x = np.linspace(0, 5, 30)
        y = np.exp(-x * plot_num * 0.3) + 0.05 * np.random.random(30)
        
        return {
            'x': x,
            'y': y,
            'title': f'Plot {plot_num} - {sample_name}',
            'xlabel': 'X Values',
            'ylabel': 'Y Values'
        }
    
    def _generate_multi_line_data(self, plot_num, sample_name):
        """Generate multi-line data with two data series"""
        x = np.linspace(0, 8, 40)
        y1 = np.cos(x + plot_num * 0.2) + 0.1 * np.random.random(40)
        y2 = np.sin(x + plot_num * 0.3) + 0.1 * np.random.random(40)
        
        return {
            'x': x,
            'y1': y1,
            'y2': y2,
            'title': f'Plot {plot_num} - {sample_name}',
            'xlabel': 'X Values',
            'ylabel': 'Y Values'
        }
    
    def _generate_polynomial_data(self, plot_num, sample_name):
        """Generate polynomial data"""
        x = np.linspace(0, 6, 25)
        y = (x**2) * (0.1 * plot_num) + 0.05 * np.random.random(25)
        
        return {
            'x': x,
            'y': y,
            'title': f'Plot {plot_num} - {sample_name}',
            'xlabel': 'X Values',
            'ylabel': 'Y Values'
        }
    
    def _generate_gaussian_data(self, plot_num, sample_name):
        """Generate Gaussian-like distribution data"""
        x = np.linspace(-5, 5, 100)
        y = (1 / (1 + x**2)) * plot_num * 0.5 + 0.02 * np.random.random(100)
        
        return {
            'x': x,
            'y': y,
            'title': f'Plot {plot_num} - {sample_name}',
            'xlabel': 'X Values',
            'ylabel': 'Y Values'
        }
    
    def _generate_log_data(self, plot_num, sample_name):
        """Generate logarithmic data"""
        x = np.linspace(0.1, 4, 35)
        y = np.log(x + plot_num * 0.5) + 0.1 * np.random.random(35)
        
        return {
            'x': x,
            'y': y,
            'title': f'Plot {plot_num} - {sample_name}',
            'xlabel': 'X Values',
            'ylabel': 'Y Values'
        }
    
    def _generate_damped_oscillation_data(self, plot_num, sample_name):
        """Generate damped oscillation data"""
        x = np.linspace(0, 10, 50)
        y = np.exp(-x * 0.2) * np.sin(x * plot_num) + 0.05 * np.random.random(50)
        
        return {
            'x': x,
            'y': y,
            'title': f'Plot {plot_num} - {sample_name}',
            'xlabel': 'X Values',
            'ylabel': 'Y Values'
        }
    
    def _generate_spiral_data(self, plot_num, sample_name):
        """Generate spiral data in Cartesian coordinates"""
        t = np.linspace(0, 4*np.pi, 50)
        x = t * np.cos(t + plot_num)
        y = t * np.sin(t + plot_num) + 0.1 * np.random.random(50)
        
        return {
            'x': x,
            'y': y,
            'title': f'Plot {plot_num} - {sample_name}',
            'xlabel': 'X Values',
            'ylabel': 'Y Values'
        }
    
    def _generate_noise_data(self, plot_num, sample_name):
        """Generate noise data with random variations"""
        x = np.linspace(0, 5, 30)
        y = plot_num * 0.5 + np.random.normal(0, 0.5, 30)
        
        return {
            'x': x,
            'y': y,
            'title': f'Plot {plot_num} - {sample_name}',
            'xlabel': 'X Values',
            'ylabel': 'Y Values'
        }
    
    def _generate_step_data(self, plot_num, sample_name):
        """Generate step function data"""
        x = np.linspace(0, 10, 50)
        y = np.where(x < 5, plot_num * 0.3, plot_num * 0.8) + 0.1 * np.random.random(50)
        
        return {
            'x': x,
            'y': y,
            'title': f'Plot {plot_num} - {sample_name}',
            'xlabel': 'X Values',
            'ylabel': 'Y Values'
        }

    def generate_single_site_plot_data(self, site_name, selected_items, range_up=100, range_down=1):
        """
        Generate plot data for single site preview with 1sigma error calculation
        
        Args:
            site_name (str): Site name
            selected_items (list): List of selected items from selection tab
            range_up (int): Upper range limit
            range_down (int): Lower range limit
            
        Returns:
            dict: Plot data for preview with mean and 1sigma values
        """
        if not site_name or site_name == "Select a site...":
            return {}
        
        # Parse selected items - handle both string and dict formats
        site_specimens = []
        for item in selected_items:
            if isinstance(item, str):
                # Handle string format like "Site A → Sample A1"
                if ' → ' in item:
                    parts = item.split(' → ')
                    if len(parts) == 2:
                        item_site, item_specimen = parts[0].strip(), parts[1].strip()
                        if item_site == site_name:
                            site_specimens.append(item_specimen)
            elif isinstance(item, dict):
                # Handle dict format (for backward compatibility)
                if item.get('site') == site_name:
                    site_specimens.append(item.get('specimen'))
        
        if not site_specimens:
            # If no specific specimens selected, use all specimens from this site
            if site_name in self.sites:
                site_specimens = self.sites[site_name]
            else:
                return {}
        
        # Calculate statistics for all specimens in this site
        all_specimen_values = []
        specimen_data_list = []
        
        # Calculate averages for each specimen using range settings
        for specimen in site_specimens:
            specimen_summary = self.get_range_based_specimen_summary(site_name, specimen, range_up, range_down)
            
            # Convert summary to numerical values for plotting
            specimen_data = {'specimen': specimen, 'values': []}
            for i, label in enumerate(self.data_display_labels):
                if i < self.num_params:
                    value_str = specimen_summary.get(label, 'N/A')
                    if value_str != 'N/A':
                        try:
                            value = self.parse_formatted_value(value_str)
                            specimen_data['values'].append(value)
                        except:
                            specimen_data['values'].append(0.0)
                    else:
                        specimen_data['values'].append(0.0)
        
            specimen_data_list.append(specimen_data)  # 修复：在循环内添加
        
            # Collect values for statistics calculation
            if specimen_data['values']:
                all_specimen_values.append(specimen_data['values'])
        
        # Calculate mean and 1sigma for each parameter across all specimens
        parameter_stats = []
        if all_specimen_values:
            max_params = min(self.num_params, len(all_specimen_values[0]) if all_specimen_values else 0)
            
            for param_idx in range(max_params):
                param_values = []
                for specimen_values in all_specimen_values:
                    if param_idx < len(specimen_values):
                        param_values.append(specimen_values[param_idx])
                
                if param_values:
                    mean_val = np.mean(param_values)
                    std_val = np.std(param_values)  # 1sigma
                    parameter_stats.append({
                        'mean': mean_val,
                        'std': std_val,
                        'upper_1sigma': mean_val + std_val,
                        'lower_1sigma': mean_val - std_val,
                        'count': len(param_values)
                    })
                else:
                    parameter_stats.append({
                        'mean': 0.0,
                        'std': 0.0,
                        'upper_1sigma': 0.0,
                        'lower_1sigma': 0.0,
                        'count': 0
                    })
        
        # Generate combined plot data for all specimens in this site
        plot_data = {
            'site': site_name,
            'specimens': site_specimens,
            'range_up': range_up,
            'range_down': range_down,
            'plot_averages': specimen_data_list,  # Individual specimen data
            'parameter_stats': parameter_stats,   # Mean and 1sigma statistics
            'specimen_count': len(site_specimens)
        }
        
        return plot_data

    def generate_all_sites_plot_data(self, selected_items, range_up=100, range_down=1):
        """
        Generate plot data for all sites preview with 1sigma error calculation

        Args:
            selected_items (list): List of selected items from selection tab
            range_up (int): Upper range limit
            range_down (int): Lower range limit
            
        Returns:
            dict: Plot data for all sites preview with mean and 1sigma values
        """
        plot_data = {
            'range_up': range_up,
            'range_down': range_down,
            'sites_data': {},
            'global_stats': {}
        }
        
        # Parse selected items - handle both string and dict formats
        sites_specimens = {}
        for item in selected_items:
            if isinstance(item, str):
                # Handle string format like "Site A → Sample A1"
                if ' → ' in item:
                    parts = item.split(' → ')
                    if len(parts) == 2:
                        site, specimen = parts[0].strip(), parts[1].strip()
                        if site not in sites_specimens:
                            sites_specimens[site] = []
                        sites_specimens[site].append(specimen)
            elif isinstance(item, dict):
                # Handle dict format (for backward compatibility)
                site = item.get('site')
                specimen = item.get('specimen')
                if site and specimen:
                    if site not in sites_specimens:
                        sites_specimens[site] = []
                    sites_specimens[site].append(specimen)

        # If no specific selection, use all data
        if not sites_specimens:
            sites_specimens = self.sites.copy()
        
        # Collect all site averages for global statistics
        all_site_averages = []
        
        # Generate data for each site
        for site_name, specimens in sites_specimens.items():
            site_specimen_values = []
            site_data = []
            
            for specimen in specimens:
                specimen_summary = self.get_range_based_specimen_summary(site_name, specimen, range_up, range_down)
                
                # Convert summary to numerical values
                specimen_values = {'specimen': specimen, 'values': []}
                for i, label in enumerate(self.data_display_labels):
                    if i < self.num_params:
                        value_str = specimen_summary.get(label, 'N/A')
                        if value_str != 'N/A':
                            try:
                                value = self.parse_formatted_value(value_str)
                                specimen_values['values'].append(value)
                            except:
                                specimen_values['values'].append(0.0)
                        else:
                            specimen_values['values'].append(0.0)
                
                site_data.append(specimen_values)
                if specimen_values['values']:
                    site_specimen_values.append(specimen_values['values'])
            
            # Calculate site-level statistics
            site_stats = []
            site_averages = []
            if site_specimen_values:
                max_params = min(self.num_params, len(site_specimen_values[0]) if site_specimen_values else 0)
                
                for param_idx in range(max_params):
                    param_values = []
                    for specimen_values in site_specimen_values:
                        if param_idx < len(specimen_values):
                            param_values.append(specimen_values[param_idx])
                    
                    if param_values:
                        mean_val = np.mean(param_values)
                        std_val = np.std(param_values)
                        site_stats.append({
                            'mean': mean_val,
                            'std': std_val,
                            'upper_1sigma': mean_val + std_val,
                            'lower_1sigma': mean_val - std_val,
                            'count': len(param_values)
                        })
                        site_averages.append(mean_val)
                    else:
                        site_stats.append({
                            'mean': 0.0,
                            'std': 0.0,
                            'upper_1sigma': 0.0,
                            'lower_1sigma': 0.0,
                            'count': 0
                        })
                        site_averages.append(0.0)
            
            plot_data['sites_data'][site_name] = {
                'specimens': site_data,
                'site_stats': site_stats,
                'site_averages': site_averages,
                'specimen_count': len(specimens)
            }
            
            # Collect for global statistics
            if site_averages:
                all_site_averages.append(site_averages)
        
        # Calculate global statistics across all sites
        if all_site_averages:
            global_stats = []
            max_params = min(self.num_params, len(all_site_averages[0]) if all_site_averages else 0)
            
            for param_idx in range(max_params):
                param_values = []
                for site_averages in all_site_averages:
                    if param_idx < len(site_averages):
                        param_values.append(site_averages[param_idx])
                
                if param_values:
                    global_mean = np.mean(param_values)
                    global_std = np.std(param_values)
                    global_stats.append({
                        'mean': global_mean,
                        'std': global_std,
                        'upper_1sigma': global_mean + global_std,
                        'lower_1sigma': global_mean - global_std,
                        'count': len(param_values)
                    })
                else:
                    global_stats.append({
                        'mean': 0.0,
                        'std': 0.0,
                        'upper_1sigma': 0.0,
                        'lower_1sigma': 0.0,
                        'count': 0
                    })
            
            plot_data['global_stats'] = global_stats
        
        return plot_data

    def plot_selection_preview_data(self, canvas, plot_data):
        """
        Plot selection preview data on canvas
        
        Args:
            canvas: Matplotlib canvas to plot on
            plot_data (dict): Plot data to visualize
        """
        try:
            canvas.ax.clear()
            
            if not plot_data:
                canvas.ax.set_title('No data available')
                canvas.ax.text(0.5, 0.5, 'No data to display', 
                              ha='center', va='center', transform=canvas.ax.transAxes,
                              fontsize=10, color='gray')
                canvas.draw()
                return
            
            # Check if this is single site or all sites data
            if 'specimens' in plot_data:
                # Single site preview
                self._plot_single_site_preview(canvas, plot_data)
            elif 'sites_data' in plot_data:
                # All sites preview
                self._plot_all_sites_preview(canvas, plot_data)
            else:
                canvas.ax.set_title('Invalid data format')
                canvas.ax.text(0.5, 0.5, 'Invalid data format', 
                              ha='center', va='center', transform=canvas.ax.transAxes,
                              fontsize=10, color='red')
            
            canvas.draw()
            
        except Exception as e:
            canvas.ax.clear()
            canvas.ax.set_title('Error plotting data')
            canvas.ax.text(0.5, 0.5, f'Error: {str(e)}', 
                          ha='center', va='center', transform=canvas.ax.transAxes,
                          fontsize=10, color='red')
            canvas.draw()

    def _plot_single_site_preview(self, canvas, plot_data):
        """Single Site Preview: specimen均值+1σ误差棒，选中为实心，未选中为空心，选中均值/1σ横线"""
        site_name = plot_data.get('site', 'Unknown Site')
        all_specimens = self.sites.get(site_name, [])

        # 选中specimen
        selected_items = getattr(self, 'selection_tab', None).get_selected_items() if hasattr(self, 'selection_tab') else []
        selected_specimens = set()
        for item in selected_items:
            if isinstance(item, str) and ' → ' in item:
                parts = item.split(' → ')
                if len(parts) == 2 and parts[0].strip() == site_name:
                    selected_specimens.add(parts[1].strip())

        specimen_names = []
        averages = []
        stds = []
        is_selected = []

        for specimen in all_specimens:
            summary = self.get_range_based_specimen_summary(site_name, specimen,
                                                            plot_data.get('range_up', 100),
                                                            plot_data.get('range_down', 1))
            values = []
            for idx, label in enumerate(self.data_display_labels):
                if idx < self.num_params:
                    val_str = summary.get(label, 'N/A')
                    if val_str != 'N/A':
                        try:
                            val = self.parse_formatted_value(val_str)
                            values.append(val)
                        except:
                            values.append(0.0)
            if not values:
                continue
            specimen_names.append(specimen)
            avg = np.mean(values)
            std = np.std(values) if len(values) > 1 else 0.0
            averages.append(avg)
            stds.append(std)
            is_selected.append(specimen in selected_specimens)

        if not specimen_names:
            canvas.ax.set_title(f'{site_name} - No valid data')
            canvas.ax.text(0.5, 0.5, 'No valid data available',
                           ha='center', va='center', transform=canvas.ax.transAxes,
                           fontsize=10, color='gray')
            return

        x_positions = np.arange(len(specimen_names))
        for i, (avg, std, sel) in enumerate(zip(averages, stds, is_selected)):
            if sel:
                canvas.ax.errorbar(i, avg, yerr=std, fmt='o', color='blue',
                                   markersize=8, capsize=5, capthick=2, alpha=0.9)
            else:
                canvas.ax.errorbar(i, avg, yerr=std, fmt='o', color='white',
                                   markeredgecolor='blue', markeredgewidth=2, markersize=8,
                                   capsize=5, capthick=2, alpha=0.7)

        # 只用选中的 specimen 计算均值和1σ
        selected_vals = [avg for avg, sel in zip(averages, is_selected) if sel]
        if selected_vals:
            mean_sel = np.mean(selected_vals)
            std_sel = np.std(selected_vals)
            canvas.ax.axhline(y=mean_sel, color='red', linestyle='-', linewidth=2, alpha=0.8, label='Selected Mean')
            canvas.ax.axhline(y=mean_sel + std_sel, color='red', linestyle='--', linewidth=1.5, alpha=0.6, label='+1σ')
            canvas.ax.axhline(y=mean_sel - std_sel, color='red', linestyle='--', linewidth=1.5, alpha=0.6, label='-1σ')

        canvas.ax.set_xlabel('Specimens')
        canvas.ax.set_ylabel('Parameter Average')
        canvas.ax.set_title(f'{site_name} - All Specimens with 1σ Error Bars')
        canvas.ax.set_xticks(x_positions)
        canvas.ax.set_xticklabels(specimen_names, rotation=45, ha='right')
        canvas.ax.grid(True, alpha=0.3)
        canvas.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    def _plot_all_sites_preview(self, canvas, plot_data):
        """All Site Preview: site均值+1σ误差棒，选中为实心，未选中为空心，选中均值/1σ横线"""
        
        all_sites = list(self.sites.keys())
        if not all_sites:
            canvas.ax.set_title('All Sites - No sites available')
            canvas.ax.text(0.5, 0.5, 'No sites available',
                           ha='center', va='center', transform=canvas.ax.transAxes,
                           fontsize=10, color='gray')
            return

        selected_items = getattr(self, 'selection_tab', None).get_selected_items() if hasattr(self, 'selection_tab') else []
        selected_sites = set()
        for item in selected_items:
            if isinstance(item, str) and ' → ' in item:
                parts = item.split(' → ')
                if len(parts) == 2:
                    selected_sites.add(parts[0].strip())

        site_names = []
        site_averages = []
        site_stds = []
        site_selected = []

        range_up = plot_data.get('range_up', 100)
        range_down = plot_data.get('range_down', 1)
        for site_name in all_sites:
            specimens = self.sites[site_name]
            specimen_vals = []
            for specimen in specimens:
                summary = self.get_range_based_specimen_summary(site_name, specimen, range_up, range_down)
                vals = []
                for idx, label in enumerate(self.data_display_labels):
                    if idx < self.num_params:
                        val_str = summary.get(label, 'N/A')
                        if val_str != 'N/A':
                            try:
                                val = self.parse_formatted_value(val_str)
                                vals.append(val)
                            except:
                                vals.append(0.0)
                if vals:
                    specimen_vals.append(np.mean(vals))

            if specimen_vals:
                site_avg = np.mean(specimen_vals)
                site_std = np.std(specimen_vals) if len(specimen_vals) > 1 else 0.0
                site_names.append(site_name)
                site_averages.append(site_avg)
                site_stds.append(site_std)
                site_selected.append(site_name in selected_sites)

        if not site_names:
            canvas.ax.set_title('All Sites - No valid data')
            canvas.ax.text(0.5, 0.5, 'No valid data available',
                           ha='center', va='center', transform=canvas.ax.transAxes,
                           fontsize=10, color='gray')
            return

        x_positions = np.arange(len(site_names))
        for i, (avg, std, sel) in enumerate(zip(site_averages, site_stds, site_selected)):
            if sel:
                canvas.ax.errorbar(i, avg, yerr=std, fmt='s', color='green',
                                   markersize=10, capsize=5, capthick=2, alpha=0.9)
            else:
                canvas.ax.errorbar(i, avg, yerr=std, fmt='s', color='white',
                                   markeredgecolor='green', markeredgewidth=2, markersize=10,
                                   capsize=5, capthick=2, alpha=0.7)

        # 只用选中的site计算均值和1σ
        selected_vals = [avg for avg, sel in zip(site_averages, site_selected) if sel]
        if selected_vals:
            mean_selected = np.mean(selected_vals)
            std_selected = np.std(selected_vals)
            canvas.ax.axhline(y=mean_selected, color='red', linestyle='-', linewidth=2, alpha=0.8, label='Selected Mean')
            canvas.ax.axhline(y=mean_selected + std_selected, color='red', linestyle='--', linewidth=1.5, alpha=0.6, label='+1σ')
            canvas.ax.axhline(y=mean_selected - std_selected, color='red', linestyle='--', linewidth=1.5, alpha=0.6, label='-1σ')

        canvas.ax.set_xlabel('Sites')
        canvas.ax.set_ylabel('Site Average')
        canvas.ax.set_title('All Sites - All Sites with 1σ Error Bars')
        canvas.ax.set_xticks(x_positions)
        canvas.ax.set_xticklabels(site_names, rotation=45, ha='right')
        canvas.ax.grid(True, alpha=0.3)
        canvas.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        

def launch_test_app():
    """Launch test application with predefined settings"""
    # Application configuration
    NUM_PLOTS = 8      
    NUM_PARAMS = 6     
    
    # Custom parameter labels for data display
    CUSTOM_LABELS = [
        "Plot1 Avg",      # Previously "Overall Avg"
        "Plot2 Avg",      # Previously "Overall Std"  
        "Plot3 Avg",      # Previously "Data Points"
        "Plot4 Avg",      # Previously "Valid Plots"
        "Plot5 Avg",      # Previously "Range Setting"
        "Plot6 Avg"       # Previously "Plot1 Avg"
    ]
    
    from main_window import MainWindow
    from app_manager import TestAppManager
    
    app = QApplication(sys.argv)
    
    # Set application icon
    app.setWindowIcon(QIcon('icon.png'))
    
    test_manager = TestAppManager()
    window = test_manager.create_test_application(
        num_plots=NUM_PLOTS, 
        num_params=NUM_PARAMS, 
        custom_param_labels=CUSTOM_LABELS
    )
    
    # Verify cache status
    if hasattr(window, 'data_tab') and hasattr(window.data_tab, 'test_data_generator'):
        test_data = window.data_tab.test_data_generator
        cache_info = test_data.get_cache_info()
        print(f"Cache Info: {cache_info}")
    
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    launch_test_app()
