import sys
import numpy as np
import re
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon


class Sample:
    """Sample (Specimen) class - stores individual sample data and metadata"""
    
    def __init__(self, name, site_name, num_plots=8):
        """
        Initialize Sample instance
        
        Args:
            name (str): Sample name
            site_name (str): Parent site name
            num_plots (int): Number of plots for this sample
        """
        self.name = name
        self.site_name = site_name
        self.num_plots = num_plots
        self.plot_data = {}  # Store all plot data: {'plot1': {...}, 'plot2': {...}, ...}
        self.metadata = {}   # Store additional metadata
        self.statistics = {} # Store calculated statistics
        
    def add_plot_data(self, plot_index, data):
        """Add plot data for specific plot index"""
        plot_key = f'plot{plot_index + 1}'
        self.plot_data[plot_key] = data
        
    def get_plot_data(self, plot_index):
        """Get plot data for specific plot index"""
        plot_key = f'plot{plot_index + 1}'
        return self.plot_data.get(plot_key, None)
    
    def get_all_plot_data(self):
        """Get all plot data"""
        return self.plot_data.copy()
    
    def calculate_statistics(self, range_up=100, range_down=1):
        """Calculate statistics for this sample within specified range"""
        stats = {
            'range_up': range_up,
            'range_down': range_down,
            'plot_stats': {}
        }
        
        all_y_values = []
        
        for plot_key, data in self.plot_data.items():
            if not data:
                continue
                
            x_values = data.get('x')
            if x_values is None:
                continue
            
            # Handle multi-line data
            if 'y1' in data and 'y2' in data:
                y1_values = data['y1']
                y2_values = data['y2']
                range_mask = (x_values >= range_down) & (x_values <= range_up)
                
                if np.any(range_mask):
                    y1_range = y1_values[range_mask]
                    y2_range = y2_values[range_mask]
                    combined_avg = np.mean(np.concatenate([y1_range, y2_range]))
                    
                    stats['plot_stats'][plot_key] = {
                        'type': 'multi_line',
                        'average': float(combined_avg),
                        'y1_average': float(np.mean(y1_range)),
                        'y2_average': float(np.mean(y2_range)),
                        'std': float(np.std(np.concatenate([y1_range, y2_range])))
                    }
                    all_y_values.extend(y1_range)
                    all_y_values.extend(y2_range)
            # Handle single-line data
            elif 'y' in data:
                y_values = data['y']
                range_mask = (x_values >= range_down) & (x_values <= range_up)
                
                if np.any(range_mask):
                    y_range = y_values[range_mask]
                    stats['plot_stats'][plot_key] = {
                        'type': 'single_line',
                        'average': float(np.mean(y_range)),
                        'std': float(np.std(y_range)),
                        'min': float(np.min(y_range)),
                        'max': float(np.max(y_range)),
                        'median': float(np.median(y_range))
                    }
                    all_y_values.extend(y_range)
        
        # Calculate overall statistics
        if all_y_values:
            all_y_array = np.array(all_y_values)
            stats['overall'] = {
                'average': float(np.mean(all_y_array)),
                'std': float(np.std(all_y_array)),
                'min': float(np.min(all_y_array)),
                'max': float(np.max(all_y_array)),
                'median': float(np.median(all_y_array)),
                'count': len(all_y_values)
            }
        
        self.statistics = stats
        return stats
    
    def set_metadata(self, key, value):
        """Set metadata for this sample"""
        self.metadata[key] = value
        
    def get_metadata(self, key, default=None):
        """Get metadata for this sample"""
        return self.metadata.get(key, default)
    
    def __repr__(self):
        return f"Sample(name='{self.name}', site='{self.site_name}', plots={len(self.plot_data)})"


class Site:
    """Site class - manages collection of samples"""
    
    def __init__(self, name):
        """
        Initialize Site instance
        
        Args:
            name (str): Site name
        """
        self.name = name
        self.samples = {}  # Dictionary of samples: {sample_name: Sample instance}
        self.metadata = {} # Store site-level metadata
        self.statistics = {} # Store site-level statistics
        
    def add_sample(self, sample_name, num_plots=8):
        """
        Add a new sample to this site
        
        Args:
            sample_name (str): Name of the sample
            num_plots (int): Number of plots for this sample
            
        Returns:
            Sample: The created Sample instance
        """
        if sample_name in self.samples:
            print(f"Warning: Sample '{sample_name}' already exists in site '{self.name}'")
            return self.samples[sample_name]
        
        sample = Sample(sample_name, self.name, num_plots)
        self.samples[sample_name] = sample
        return sample
    
    def remove_sample(self, sample_name):
        """
        Remove a sample from this site
        
        Args:
            sample_name (str): Name of the sample to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        if sample_name in self.samples:
            del self.samples[sample_name]
            return True
        return False
    
    def get_sample(self, sample_name):
        """Get a sample by name"""
        return self.samples.get(sample_name, None)
    
    def get_all_samples(self):
        """Get all samples in this site"""
        return self.samples.copy()
    
    def get_sample_names(self):
        """Get list of all sample names"""
        return list(self.samples.keys())
    
    def calculate_statistics(self, range_up=100, range_down=1):
        """Calculate site-level statistics from all samples"""
        if not self.samples:
            return {}
        
        # First ensure all samples have calculated their statistics
        for sample in self.samples.values():
            sample.calculate_statistics(range_up, range_down)
        
        stats = {
            'range_up': range_up,
            'range_down': range_down,
            'sample_count': len(self.samples),
            'samples_stats': {}
        }
        
        # Collect averages from all samples
        all_sample_averages = []
        
        for sample_name, sample in self.samples.items():
            if sample.statistics and 'overall' in sample.statistics:
                sample_avg = sample.statistics['overall']['average']
                all_sample_averages.append(sample_avg)
                stats['samples_stats'][sample_name] = sample.statistics['overall']
        
        # Calculate site-level statistics
        if all_sample_averages:
            avg_array = np.array(all_sample_averages)
            stats['site_overall'] = {
                'average': float(np.mean(avg_array)),
                'std': float(np.std(avg_array)),
                'min': float(np.min(avg_array)),
                'max': float(np.max(avg_array)),
                'median': float(np.median(avg_array)),
                'count': len(all_sample_averages)
            }
        
        self.statistics = stats
        return stats
    
    def set_metadata(self, key, value):
        """Set metadata for this site"""
        self.metadata[key] = value
        
    def get_metadata(self, key, default=None):
        """Get metadata for this site"""
        return self.metadata.get(key, default)
    
    def __repr__(self):
        return f"Site(name='{self.name}', samples={len(self.samples)})"
    
    def __getitem__(self, sample_name):
        """Allow dict-like access to samples"""
        return self.get_sample(sample_name)
    
    def __contains__(self, sample_name):
        """Check if sample exists in site"""
        return sample_name in self.samples


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
        
        # Site management - now uses Site class
        self.sites = {}  # Dictionary of sites: {site_name: Site instance}
        
        # Data storage for filtering states and calculation results
        self.filter_states = {}  # Store filter conditions: {site: {specimen: {param_index: condition}}}
        self.filter_results = {}  # Store filter match results: {site: {specimen: {param_index: bool}}}
        self.calculation_cache = {}  # Cache calculation results: {site: {specimen: {range_key: stats}}}
        self.plot_data_cache = {}  # Cache plot data: {site: {specimen: plot_data}}
        
        # Range settings storage
        self.current_range_up = 100  # Current range upper limit
        self.current_range_down = 1  # Current range lower limit
        self.range_history = []  # History of range changes: [(up, down, timestamp), ...]
        
        # Current selection state
        self.current_site = None  # Currently selected site
        self.current_specimen = None  # Currently selected specimen
        self.selection_history = []  # History of selections: [(site, specimen, timestamp), ...]
        
        # Sample selection state (for selection tab)
        self.selected_samples = set()  # Set of selected sample identifiers: {(site, specimen), ...}
        self.selection_plot_data = {}  # Cached plot data for selections: {selection_key: plot_data}
        
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
        
        # Initialize default test sites and samples
        self._initialize_default_data()
    
    def _initialize_default_data(self):
        """Initialize default test sites and samples"""
        print("Initializing default test data structure...")
        
        # Set random seed for reproducible results
        np.random.seed(42)
        
        # Define default structure
        default_structure = {
            "Site A": ["Sample A1", "Sample A2", "Sample A3"],
            "Site B": ["Sample B1", "Sample B2"],
            "Site C": ["Sample C1", "Sample C2", "Sample C3", "Sample C4"],
            "Site D": ["Sample D1", "Sample D2"]
        }
        
        # Create sites and samples
        for site_name, sample_names in default_structure.items():
            self.add_site(site_name)
            for sample_name in sample_names:
                self.add_sample(site_name, sample_name)
        
        print(f"Initialization complete. Created {len(self.sites)} sites with {sum(len(site.samples) for site in self.sites.values())} samples.")
    
    # ========== Site Management Methods ==========
    
    def add_site(self, site_name):
        """
        Add a new site
        
        Args:
            site_name (str): Name of the site to add
            
        Returns:
            Site: The created Site instance, or existing site if already exists
        """
        if site_name in self.sites:
            print(f"Warning: Site '{site_name}' already exists")
            return self.sites[site_name]
        
        site = Site(site_name)
        self.sites[site_name] = site
        print(f"Added site: {site_name}")
        return site
    
    def remove_site(self, site_name):
        """
        Remove a site and all its samples
        
        Args:
            site_name (str): Name of the site to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        if site_name in self.sites:
            sample_count = len(self.sites[site_name].samples)
            del self.sites[site_name]
            print(f"Removed site: {site_name} (with {sample_count} samples)")
            return True
        print(f"Warning: Site '{site_name}' not found")
        return False
    
    def get_site(self, site_name):
        """
        Get a site by name
        
        Args:
            site_name (str): Name of the site
            
        Returns:
            Site: Site instance or None if not found
        """
        return self.sites.get(site_name, None)
    
    def get_all_sites(self):
        """Get all sites"""
        return self.sites.copy()
    
    def get_site_names(self):
        """Get list of all site names"""
        return list(self.sites.keys())
    
    def rename_site(self, old_name, new_name):
        """
        Rename a site
        
        Args:
            old_name (str): Current site name
            new_name (str): New site name
            
        Returns:
            bool: True if renamed successfully, False otherwise
        """
        if old_name not in self.sites:
            print(f"Warning: Site '{old_name}' not found")
            return False
        
        if new_name in self.sites:
            print(f"Warning: Site '{new_name}' already exists")
            return False
        
        site = self.sites[old_name]
        site.name = new_name
        
        # Update all samples' site_name
        for sample in site.samples.values():
            sample.site_name = new_name
        
        self.sites[new_name] = site
        del self.sites[old_name]
        
        print(f"Renamed site: {old_name} -> {new_name}")
        return True
    
    # ========== Sample Management Methods ==========
    
    def add_sample(self, site_name, sample_name, num_plots=None):
        """
        Add a new sample to a site
        
        Args:
            site_name (str): Name of the site
            sample_name (str): Name of the sample
            num_plots (int): Number of plots (default: use self.num_plots)
            
        Returns:
            Sample: The created Sample instance or None if site not found
        """
        site = self.get_site(site_name)
        if not site:
            print(f"Warning: Site '{site_name}' not found. Creating site first.")
            site = self.add_site(site_name)
        
        if num_plots is None:
            num_plots = self.num_plots
        
        sample = site.add_sample(sample_name, num_plots)
        
        # Generate plot data for this sample
        self._generate_sample_data(site_name, sample_name)
        
        print(f"Added sample: {sample_name} to site: {site_name}")
        return sample
    
    def remove_sample(self, site_name, sample_name):
        """
        Remove a sample from a site
        
        Args:
            site_name (str): Name of the site
            sample_name (str): Name of the sample to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        site = self.get_site(site_name)
        if not site:
            print(f"Warning: Site '{site_name}' not found")
            return False
        
        result = site.remove_sample(sample_name)
        if result:
            print(f"Removed sample: {sample_name} from site: {site_name}")
        else:
            print(f"Warning: Sample '{sample_name}' not found in site '{site_name}'")
        return result
    
    def get_sample(self, site_name, sample_name):
        """
        Get a sample from a site
        
        Args:
            site_name (str): Name of the site
            sample_name (str): Name of the sample
            
        Returns:
            Sample: Sample instance or None if not found
        """
        site = self.get_site(site_name)
        if not site:
            return None
        return site.get_sample(sample_name)
    
    def rename_sample(self, site_name, old_name, new_name):
        """
        Rename a sample within a site
        
        Args:
            site_name (str): Name of the site
            old_name (str): Current sample name
            new_name (str): New sample name
            
        Returns:
            bool: True if renamed successfully, False otherwise
        """
        site = self.get_site(site_name)
        if not site:
            print(f"Warning: Site '{site_name}' not found")
            return False
        
        sample = site.get_sample(old_name)
        if not sample:
            print(f"Warning: Sample '{old_name}' not found in site '{site_name}'")
            return False
        
        if new_name in site.samples:
            print(f"Warning: Sample '{new_name}' already exists in site '{site_name}'")
            return False
        
        # Update sample name
        sample.name = new_name
        site.samples[new_name] = sample
        del site.samples[old_name]
        
        print(f"Renamed sample: {old_name} -> {new_name} in site: {site_name}")
        return True
    
    def move_sample(self, from_site, to_site, sample_name):
        """
        Move a sample from one site to another
        
        Args:
            from_site (str): Source site name
            to_site (str): Destination site name
            sample_name (str): Name of the sample to move
            
        Returns:
            bool: True if moved successfully, False otherwise
        """
        source_site = self.get_site(from_site)
        if not source_site:
            print(f"Warning: Source site '{from_site}' not found")
            return False
        
        sample = source_site.get_sample(sample_name)
        if not sample:
            print(f"Warning: Sample '{sample_name}' not found in site '{from_site}'")
            return False
        
        # Create destination site if it doesn't exist
        dest_site = self.get_site(to_site)
        if not dest_site:
            dest_site = self.add_site(to_site)
        
        # Check if sample already exists in destination
        if sample_name in dest_site.samples:
            print(f"Warning: Sample '{sample_name}' already exists in site '{to_site}'")
            return False
        
        # Move sample
        sample.site_name = to_site
        dest_site.samples[sample_name] = sample
        del source_site.samples[sample_name]
        
        print(f"Moved sample: {sample_name} from {from_site} to {to_site}")
        return True
    
    # ========== Data Generation Methods ==========
    
    def _generate_sample_data(self, site_name, sample_name):
        """
        Generate plot data for a specific sample
        
        Args:
            site_name (str): Name of the site
            sample_name (str): Name of the sample
        """
        sample = self.get_sample(site_name, sample_name)
        if not sample:
            return
        
        # Generate data for each plot
        for i in range(sample.num_plots):
            plot_data = self._generate_single_plot_data(i, sample_name, site_name)
            sample.add_plot_data(i, plot_data)
    
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
    
    def regenerate_sample_data(self, site_name, sample_name):
        """
        Regenerate plot data for a specific sample
        
        Args:
            site_name (str): Name of the site
            sample_name (str): Name of the sample
            
        Returns:
            bool: True if regenerated successfully
        """
        sample = self.get_sample(site_name, sample_name)
        if not sample:
            print(f"Warning: Sample '{sample_name}' not found in site '{site_name}'")
            return False
        
        # Clear existing plot data
        sample.plot_data.clear()
        
        # Regenerate
        self._generate_sample_data(site_name, sample_name)
        print(f"Regenerated data for sample: {sample_name} in site: {site_name}")
        return True
    
    def regenerate_all_data(self):
        """Regenerate all plot data for all samples in all sites"""
        print("Regenerating all data...")
        np.random.seed(42)  # Reset seed for reproducibility
        
        for site_name, site in self.sites.items():
            for sample_name in site.get_sample_names():
                sample = site.get_sample(sample_name)
                sample.plot_data.clear()
                self._generate_sample_data(site_name, sample_name)
        
        print("All data regenerated.")
    
    # ========== Legacy Compatibility Methods ==========
    
    def get_cache_info(self):
        """
        Get information about the data structure (legacy compatibility)
        
        Returns:
            dict: Data structure information
        """
        total_specimens = sum(len(site.samples) for site in self.sites.values())
        
        return {
            'total_sites': len(self.sites),
            'total_specimens': total_specimens,
            'sites': self.get_site_names(),
            'structure': {
                site_name: site.get_sample_names() 
                for site_name, site in self.sites.items()
            }
        }

    def format_significant_figures(self, value, sig_figs=5):
        """Format number to specified significant figures"""
        try:
            val = float(value)
            if val == 0:
                return "0.0000"
            
            magnitude = int(np.floor(np.log10(abs(val))))
            
            if magnitude >= 4 or magnitude < -2:
                mantissa = val / (10 ** magnitude)
                formatted_mantissa = f"{mantissa:.{sig_figs-1}f}"
                return f"{formatted_mantissa}e{magnitude:+d}"
            else:
                if magnitude >= 0:
                    decimal_places = max(0, sig_figs - magnitude - 1)
                    return f"{val:.{decimal_places}f}"
                else:
                    decimal_places = sig_figs - magnitude - 1
                    return f"{val:.{decimal_places}f}"
                    
        except (ValueError, TypeError):
            return str(value)

    def parse_formatted_value(self, formatted_str):
        """Parse formatted string back to float value"""
        try:
            return float(formatted_str)
        except (ValueError, TypeError):
            return 0.0

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

    # ========== Compatibility Methods for Existing Code ==========
    
    def generate_specimen_data_for_data_box(self, site, specimen):
        """Get specimen data (legacy compatibility)"""
        sample = self.get_sample(site, specimen)
        if sample:
            return sample.get_all_plot_data()
        return {}
    
    def generate_specimen_data(self, site, specimen):
        """Generate data for a specific specimen"""
        sample = self.get_sample(site, specimen)
        if not sample:
            return {}
        
        return sample.get_all_plot_data()
    
    def generate_specimen_data_full_range(self, site, specimen):
        """
        Generate full range specimen data (same as generate_specimen_data)
        保持向后兼容性
        """
        return self.generate_specimen_data(site, specimen)
    
    def calculate_range_based_averages(self, site, specimen, range_up=None, range_down=None):
        """
        Calculate range-based averages (uses Sample.calculate_statistics)
        Uses current range settings if not specified
        """
        # Use current range settings if not provided
        if range_up is None:
            range_up = self.current_range_up
        if range_down is None:
            range_down = self.current_range_down
        
        sample = self.get_sample(site, specimen)
        if not sample:
            return {}
        
        stats = sample.calculate_statistics(range_up, range_down)
        
        # Convert to legacy format
        range_averages = {
            'site': site,
            'specimen': specimen,
            'range_up': range_up,
            'range_down': range_down,
            'plot_averages': {},
            'overall_statistics': stats.get('overall', {})
        }
        
        # Convert plot stats to legacy format
        for plot_key, plot_stats in stats.get('plot_stats', {}).items():
            range_averages['plot_averages'][plot_key] = plot_stats
        
        return range_averages
    
    def get_range_based_specimen_summary(self, site, specimen, range_up=None, range_down=None):
        """
        Get range-based specimen summary
        Uses current range settings if not specified
        """
        range_averages = self.calculate_range_based_averages(site, specimen, range_up, range_down)
        
        summary = {}
        
        for i in range(self.num_params):
            label = self.data_display_labels[i]
            
            plot_index = i
            if plot_index < self.num_plots:
                plot_key = f'plot{plot_index + 1}'
                if plot_key in range_averages.get('plot_averages', {}):
                    plot_data = range_averages['plot_averages'][plot_key]
                    
                    if 'average' in plot_data:
                        avg_val = plot_data['average']
                        formatted_val = self.format_significant_figures(avg_val, 5)
                        summary[label] = formatted_val
                    else:
                        summary[label] = 'N/A'
                else:
                    summary[label] = 'N/A'
            else:
                summary[label] = 'N/A'
        
        return summary
    
    # ========== Methods using external functions from data_utils ==========
    
    def check_parameter_condition_independently(self, site, specimen, parameter_index, 
                                               condition_str, range_up=100, range_down=1):
        """
        Check if a parameter meets the condition independently
        Uses external function from data_utils
        
        Args:
            site (str): Site name
            specimen (str): Specimen name
            parameter_index (int): Parameter index
            condition_str (str): Condition string (e.g., ">10", "<=5.5")
            range_up (int): Range upper limit
            range_down (int): Range lower limit
            
        Returns:
            bool: Whether condition is met
        """
        from data_utils import check_parameter_condition_independently
        
        result = check_parameter_condition_independently(
            self, site, specimen, parameter_index, condition_str, range_up, range_down
        )
        
        # Store filter state and result
        if site not in self.filter_states:
            self.filter_states[site] = {}
        if specimen not in self.filter_states[site]:
            self.filter_states[site][specimen] = {}
        self.filter_states[site][specimen][parameter_index] = condition_str
        
        if site not in self.filter_results:
            self.filter_results[site] = {}
        if specimen not in self.filter_results[site]:
            self.filter_results[site][specimen] = {}
        self.filter_results[site][specimen][parameter_index] = result
        
        return result
    
    def generate_single_site_plot_data(self, site_name, selected_items, range_up=100, range_down=1):
        """
        Generate plot data for single site preview
        Uses external function from data_utils
        
        Args:
            site_name (str): Site name
            selected_items (list): Selected items list
            range_up (int): Range upper limit
            range_down (int): Range lower limit
            
        Returns:
            dict: Plot data
        """
        from data_utils import generate_single_site_plot_data
        
        plot_data = generate_single_site_plot_data(self, site_name, selected_items, range_up, range_down)
        
        # Cache plot data
        cache_key = f"{site_name}_{range_up}_{range_down}"
        if site_name not in self.plot_data_cache:
            self.plot_data_cache[site_name] = {}
        self.plot_data_cache[site_name][cache_key] = plot_data
        
        return plot_data
    
    def generate_all_sites_plot_data(self, selected_items, range_up=100, range_down=1):
        """
        Generate plot data for all sites preview
        Uses external function from data_utils
        
        Args:
            selected_items (list): Selected items list
            range_up (int): Range upper limit
            range_down (int): Range lower limit
            
        Returns:
            dict: Plot data
        """
        from data_utils import generate_all_sites_plot_data
        
        plot_data = generate_all_sites_plot_data(self, selected_items, range_up, range_down)
        
        # Cache plot data
        cache_key = f"all_sites_{range_up}_{range_down}"
        self.plot_data_cache[cache_key] = plot_data
        
        return plot_data
    
    def plot_selection_preview_data(self, canvas, plot_data):
        """
        Plot selection preview data on canvas
        Uses external function from data_utils
        
        Args:
            canvas: MplCanvas instance
            plot_data (dict): Plot data dictionary
        """
        from data_utils import plot_selection_preview_data
        
        plot_selection_preview_data(canvas, plot_data)
    
    def get_filter_state(self, site, specimen, parameter_index=None):
        """
        Get filter state for a specimen
        
        Args:
            site (str): Site name
            specimen (str): Specimen name
            parameter_index (int, optional): Specific parameter index
            
        Returns:
            dict or str: Filter state(s)
        """
        if site not in self.filter_states:
            return {} if parameter_index is None else ""
        if specimen not in self.filter_states[site]:
            return {} if parameter_index is None else ""
        
        if parameter_index is None:
            return self.filter_states[site][specimen]
        else:
            return self.filter_states[site][specimen].get(parameter_index, "")
    
    def get_filter_result(self, site, specimen, parameter_index=None):
        """
        Get filter result for a specimen
        
        Args:
            site (str): Site name
            specimen (str): Specimen name
            parameter_index (int, optional): Specific parameter index
            
        Returns:
            dict or bool: Filter result(s)
        """
        if site not in self.filter_results:
            return {} if parameter_index is None else True
        if specimen not in self.filter_results[site]:
            return {} if parameter_index is None else True
        
        if parameter_index is None:
            return self.filter_results[site][specimen]
        else:
            return self.filter_results[site][specimen].get(parameter_index, True)
    
    def clear_filter_cache(self, site=None, specimen=None):
        """
        Clear filter cache
        
        Args:
            site (str, optional): Specific site to clear, None for all
            specimen (str, optional): Specific specimen to clear
        """
        if site is None:
            self.filter_states.clear()
            self.filter_results.clear()
        elif specimen is None:
            if site in self.filter_states:
                del self.filter_states[site]
            if site in self.filter_results:
                del self.filter_results[site]
        else:
            if site in self.filter_states and specimen in self.filter_states[site]:
                del self.filter_states[site][specimen]
            if site in self.filter_results and specimen in self.filter_results[site]:
                del self.filter_results[site][specimen]
    
    def clear_calculation_cache(self, site=None, specimen=None):
        """
        Clear calculation cache
        
        Args:
            site (str, optional): Specific site to clear, None for all
            specimen (str, optional): Specific specimen to clear
        """
        if site is None:
            self.calculation_cache.clear()
        elif specimen is None:
            if site in self.calculation_cache:
                del self.calculation_cache[site]
        else:
            if site in self.calculation_cache and specimen in self.calculation_cache[site]:
                del self.calculation_cache[site][specimen]
    
    def parse_filter_expression(self, expression):
        """
        Parse and validate filter expression
        使用data_utils中的函数来验证表达式
        
        Args:
            expression (str): Filter expression (e.g., ">10", "<=5.5")
            
        Returns:
            dict or None: Parsed expression or None if invalid
        """
        from data_utils import check_parameter_condition
        
        if not expression or not expression.strip():
            return None
        
        # Try to parse the expression
        import re
        match = re.match(r'\s*(>=|<=|!=|>|<|=)\s*(-?\d+(?:\.\d+)?)\s*', expression.strip())
        if not match:
            return None
        
        return {
            'operator': match.group(1),
            'value': float(match.group(2)),
            'expression': expression.strip()
        }
    
    # ========== Range and Selection State Management ==========
    
    def set_range(self, range_up, range_down):
        """
        Set current range and store in history
        
        Args:
            range_up (int): Range upper limit
            range_down (int): Range lower limit
        """
        # Store in history
        import time
        self.range_history.append((range_up, range_down, time.time()))
        
        # Update current range
        self.current_range_up = range_up
        self.current_range_down = range_down
        
        # Clear caches that depend on range
        self.clear_calculation_cache()
        self.clear_plot_data_cache()
        
        print(f"Range updated: {range_down} - {range_up}")
    
    def get_current_range(self):
        """Get current range settings"""
        return {
            'range_up': self.current_range_up,
            'range_down': self.current_range_down
        }
    
    def set_current_selection(self, site, specimen):
        """
        Set current site and specimen selection
        
        Args:
            site (str): Site name
            specimen (str): Specimen name
        """
        # Store in history
        import time
        self.selection_history.append((site, specimen, time.time()))
        
        # Update current selection
        self.current_site = site
        self.current_specimen = specimen
        
        print(f"Selection updated: {site} -> {specimen}")
    
    def get_current_selection(self):
        """Get current selection"""
        return {
            'site': self.current_site,
            'specimen': self.current_specimen
        }
    
    def add_selected_sample(self, site, specimen):
        """
        Add a sample to the selection set
        
        Args:
            site (str): Site name
            specimen (str): Specimen name
        """
        self.selected_samples.add((site, specimen))
    
    def remove_selected_sample(self, site, specimen):
        """
        Remove a sample from the selection set
        
        Args:
            site (str): Site name
            specimen (str): Specimen name
        """
        self.selected_samples.discard((site, specimen))
    
    def clear_selected_samples(self):
        """Clear all selected samples"""
        self.selected_samples.clear()
    
    def get_selected_samples(self):
        """Get list of selected samples"""
        return [{'site': site, 'specimen': specimen} for site, specimen in self.selected_samples]
    
    def is_sample_selected(self, site, specimen):
        """Check if a sample is selected"""
        return (site, specimen) in self.selected_samples
    
    def clear_plot_data_cache(self):
        """Clear plot data cache"""
        self.plot_data_cache.clear()
        self.selection_plot_data.clear()


def launch_test_app():
    """Launch test application with predefined settings"""
    NUM_PLOTS = 8      
    NUM_PARAMS = 6     
    
    CUSTOM_LABELS = [
        "Plot1 Avg", "Plot2 Avg", "Plot3 Avg",
        "Plot4 Avg", "Plot5 Avg", "Plot6 Avg"
    ]
    
    from main_window import MainWindow
    from app_manager import TestAppManager
    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    
    test_manager = TestAppManager()
    window = test_manager.create_test_application(
        num_plots=NUM_PLOTS, 
        num_params=NUM_PARAMS, 
        custom_param_labels=CUSTOM_LABELS
    )
    
    # Verify structure
    if hasattr(window, 'data_tab') and hasattr(window.data_tab, 'test_data_generator'):
        test_data = window.data_tab.test_data_generator
        cache_info = test_data.get_cache_info()
        print(f"Data Structure: {cache_info}")
    
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    launch_test_app()
