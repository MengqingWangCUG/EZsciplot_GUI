"""
Data utility functions - external functions for TestData
所有业务逻辑函数外置，数据存储在TestData中
"""
import numpy as np
import re


def check_parameter_condition(value, condition_str):
    """
    检查单个参数值是否满足条件
    
    Args:
        value (float): 参数值
        condition_str (str): 条件字符串 (e.g., ">10", "<=5.5", "=100")
        
    Returns:
        bool: 是否满足条件
    """
    if not condition_str or not condition_str.strip():
        return True
    
    condition_str = condition_str.strip()
    
    # Parse condition: operator + number
    match = re.match(r'\s*(>=|<=|!=|>|<|=)\s*(-?\d+(?:\.\d+)?)\s*', condition_str)
    if not match:
        return False
    
    operator = match.group(1)
    threshold = float(match.group(2))
    
    try:
        value = float(value)
    except (ValueError, TypeError):
        return False
    
    # Apply condition
    if operator == '>':
        return value > threshold
    elif operator == '>=':
        return value >= threshold
    elif operator == '<':
        return value < threshold
    elif operator == '<=':
        return value <= threshold
    elif operator == '=':
        return abs(value - threshold) < 1e-9
    elif operator == '!=':
        return abs(value - threshold) >= 1e-9
    
    return False


def check_parameter_condition_independently(test_data, site, specimen, parameter_index, 
                                           condition_str, range_up=100, range_down=1):
    """
    独立检查单个参数的条件（从TestData获取数据）
    
    Args:
        test_data: TestData实例
        site (str): 站点名称
        specimen (str): 样本名称
        parameter_index (int): 参数索引
        condition_str (str): 条件字符串
        range_up (int): 范围上限
        range_down (int): 范围下限
        
    Returns:
        bool: 是否满足条件
    """
    if not condition_str or not condition_str.strip():
        return True
    
    # Get specimen summary data
    specimen_summary = test_data.get_range_based_specimen_summary(site, specimen, range_up, range_down)
    
    if parameter_index >= len(test_data.data_display_labels):
        return False
    
    param_label = test_data.data_display_labels[parameter_index]
    
    if param_label not in specimen_summary:
        return False
    
    value_str = specimen_summary[param_label]
    
    if value_str == 'N/A' or not value_str:
        return False
    
    # Parse value (handle scientific notation)
    try:
        value = test_data.parse_formatted_value(value_str)
    except (ValueError, TypeError):
        return False
    
    return check_parameter_condition(value, condition_str)


def generate_single_site_plot_data(test_data, site_name, selected_items, range_up=100, range_down=1):
    """
    生成单个站点的预览图数据
    
    Args:
        test_data: TestData实例
        site_name (str): 站点名称
        selected_items (list): 选中的项目列表 [{'type': 'specimen', 'site': ..., 'name': ...}, ...]
        range_up (int): 范围上限
        range_down (int): 范围下限
        
    Returns:
        dict: 绘图数据
    """
    plot_data = {
        'site_name': site_name,
        'specimens': [],
        'x_values': [],
        'y_values': [],
        'labels': []
    }
    
    # Filter specimens belonging to this site
    site_specimens = [
        item for item in selected_items 
        if item.get('type') == 'specimen' and item.get('site') == site_name
    ]
    
    if not site_specimens:
        return plot_data
    
    # For each specimen, calculate average within range
    for item in site_specimens:
        specimen_name = item['name']
        sample = test_data.get_sample(site_name, specimen_name)
        
        if not sample:
            continue
        
        # Calculate statistics for this specimen
        stats = sample.calculate_statistics(range_up, range_down)
        
        if 'overall' in stats and 'average' in stats['overall']:
            avg_value = stats['overall']['average']
            plot_data['specimens'].append(specimen_name)
            plot_data['y_values'].append(avg_value)
            plot_data['labels'].append(specimen_name)
    
    # Generate x values (indices)
    plot_data['x_values'] = list(range(len(plot_data['specimens'])))
    
    return plot_data


def generate_all_sites_plot_data(test_data, selected_items, range_up=100, range_down=1):
    """
    生成所有站点的预览图数据
    
    Args:
        test_data: TestData实例
        selected_items (list): 选中的项目列表
        range_up (int): 范围上限
        range_down (int): 范围下限
        
    Returns:
        dict: 绘图数据
    """
    plot_data = {
        'sites': [],
        'x_values': [],
        'y_values': [],
        'labels': []
    }
    
    # Group specimens by site
    sites_dict = {}
    for item in selected_items:
        if item.get('type') == 'specimen':
            site_name = item['site']
            if site_name not in sites_dict:
                sites_dict[site_name] = []
            sites_dict[site_name].append(item['name'])
    
    # Calculate average for each site
    for site_name, specimen_names in sites_dict.items():
        site_averages = []
        
        for specimen_name in specimen_names:
            sample = test_data.get_sample(site_name, specimen_name)
            if not sample:
                continue
            
            stats = sample.calculate_statistics(range_up, range_down)
            if 'overall' in stats and 'average' in stats['overall']:
                site_averages.append(stats['overall']['average'])
        
        if site_averages:
            site_avg = np.mean(site_averages)
            plot_data['sites'].append(site_name)
            plot_data['y_values'].append(site_avg)
            plot_data['labels'].append(site_name)
    
    # Generate x values (indices)
    plot_data['x_values'] = list(range(len(plot_data['sites'])))
    
    return plot_data


def plot_selection_preview_data(canvas, plot_data):
    """
    在canvas上绘制预览数据
    
    Args:
        canvas: MplCanvas实例
        plot_data (dict): 绘图数据
    """
    canvas.ax.clear()
    
    if not plot_data.get('x_values') or not plot_data.get('y_values'):
        canvas.ax.set_title('No data to display')
        canvas.ax.text(0.5, 0.5, 'No specimens selected', 
                      ha='center', va='center', transform=canvas.ax.transAxes,
                      fontsize=10, color='gray')
        canvas.draw()
        return
    
    x_values = plot_data['x_values']
    y_values = plot_data['y_values']
    labels = plot_data.get('labels', [])
    
    # Plot bar chart
    canvas.ax.bar(x_values, y_values, color='steelblue', alpha=0.7)
    
    # Set labels
    if labels:
        canvas.ax.set_xticks(x_values)
        canvas.ax.set_xticklabels(labels, rotation=45, ha='right')
    
    # Set title based on data type
    if 'site_name' in plot_data:
        title = f"Single Site: {plot_data['site_name']}"
    else:
        title = "All Sites Preview"
    
    canvas.ax.set_title(title)
    canvas.ax.set_xlabel('Specimens/Sites')
    canvas.ax.set_ylabel('Average Value')
    canvas.ax.grid(True, alpha=0.3, axis='y')
    
    canvas.figure.tight_layout()
    canvas.draw()


def calculate_statistics_for_sample(sample, range_up=100, range_down=1):
    """
    为样本计算统计数据（外置函数版本）
    实际调用Sample类的方法
    
    Args:
        sample: Sample实例
        range_up (int): 范围上限
        range_down (int): 范围下限
        
    Returns:
        dict: 统计结果
    """
    return sample.calculate_statistics(range_up, range_down)


def calculate_statistics_for_site(site, range_up=100, range_down=1):
    """
    为站点计算统计数据（外置函数版本）
    实际调用Site类的方法
    
    Args:
        site: Site实例
        range_up (int): 范围上限
        range_down (int): 范围下限
        
    Returns:
        dict: 统计结果
    """
    return site.calculate_statistics(range_up, range_down)
