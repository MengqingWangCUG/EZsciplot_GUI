# 项目文件清单与功能概览

下面列出仓库根目录下的文件/目录，并对每个项用一句话说明其主要功能；随后列出主要类与函数的详细说明（含文件与符号链接，便于在 IDE 中打开）。

## 文件/目录总览（文件名 → 一句话功能）
- [app_manager.py](app_manager.py) — 测试应用管理器，生成与配置用于调试的 UI 与测试数据流程（`TestAppManager` 相关）。
- [color_picker.py](color_picker.py) — 颜色选择器与调色板界面与工具。
- [config.py](config.py) — UI 布局与样式配置常量与方法（LayoutConfig 等）。
- [contribution_builder.py](contribution_builder.py) — MagIC Contribution 与 MagicDataFrame 的实现与表格操作工具。
- [convert_2_magic.py](convert_2_magic.py) — 将其它格式转换为 MagIC 格式的转换工具脚本。
- [data_read_convert.py](data_read_convert.py) — 数据读取与格式转换的辅助工具。
- [data_tab.py](data_tab.py) — 应用中数据显示选项卡的 UI 组件与控件（`DataTab`）。
- [entrance.py](entrance.py) — 测试数据生成器（`TestData`）与应用启动入口（launch_test_app）。
- [gen_2_magic.py](gen_2_magic.py) — 通用 generic -> MagIC 转换逻辑与多个辅助函数（`generic`, `generic_to_middle_df` 等）。
- [IPRESETmqPint.py](IPRESETmqPint.py) — mqpint / 绘图与数据处理核心模块，包含多个绘图函数与数据类。
- [IPresetQS6.py](IPresetQS6.py) — Qt 主界面/备选实现，含 `MainWindow` 的另一版本（样本选择与绘图）。
- [main_window.py](main_window.py) — 主窗口实现，构建主布局并集成各 Tab（`MainWindow`）。
- [main.py](main.py) — 程序入口，创建 QApplication 及主窗口。
- [menu_manager.py](menu_manager.py) — 菜单与文件选择管理（`MenuManager`）。
- [mpl_canvas.py](mpl_canvas.py) — Matplotlib canvas 封装（`MplCanvas`）。
- [pint_plotting_functions.py](pint_plotting_functions.py) — 若干绘图辅助函数（pint 相关）。
- [pmag.py](pmag.py) — 与 pmagpy 有关的兼容或辅助函数（路径解析、写文件等工具）。
- [preview_manager.py](preview_manager.py) — 选择预览绘图与导出管理。
- [selection_tab.py](selection_tab.py) — 样本选择选项卡的 UI 与交互逻辑。
- [workspacelist.md](workspacelist.md) — 本文件。
- __pycache__/, .mypy_cache/ — Python 缓存目录。
- datareadtest/ — 测试数据目录。
- fig/ — 产出图像目录。
- icon/ — 应用图标资源。

---

## 详细函数 / 类 说明（按文件）

注意：每个符号后面的链接指向对应文件，点击可在 IDE 中打开该文件。

### app_manager.py
- [`TestAppManager`](app_manager.py) — 测试应用管理类，负责创建测试用窗口与绑定测试数据。
  - [`TestAppManager.create_test_application`](app_manager.py) — 创建并返回一个配置好的测试应用实例。
  - [`TestAppManager._setup_test_functionality`](app_manager.py) — 设置测试相关 UI 行为与回调（内部包含初始化参数状态、过滤器监听、范围监听等辅助闭包）。
  - [`TestAppManager._plot_single_line`](app_manager.py) — 在单一画布上绘制单条曲线。
  - [`TestAppManager._plot_multi_line`](app_manager.py) — 在画布上绘制多条线。
  - 布局与动态控件重建：[`TestAppManager._recreate_top_layout`](app_manager.py), [`TestAppManager._recreate_plots_container`](app_manager.py), 动态组建：[`TestAppManager._create_dynamic_filter_group`](app_manager.py), [`TestAppManager._create_dynamic_data_group`](app_manager.py)。

### data_tab.py
- [`DataTab`](data_tab.py) — 数据选项卡 UI 类，负责展示过滤器、范围控件与多个绘图画布。
  - [`DataTab.init_test_data`](data_tab.py) — 从 `entrance.TestData` 初始化测试数据与标签。
  - [`DataTab.create_ui`](data_tab.py) — 构建整个 DataTab 的 UI。
  - [`DataTab.create_filter_group`](data_tab.py) — 使用参数标签创建过滤条件输入组。
  - [`DataTab.create_plots_container`](data_tab.py) — 创建绘图容器（多个子画布）。
  - [`DataTab.create_individual_plot_group`](data_tab.py) — 为单个图创建 Group。
  - [`DataTab.create_data_group`](data_tab.py) — 创建用于显示数值/信息的区域。
  - 辅助：[`DataTab._create_adaptive_label`](data_tab.py), [`DataTab.create_status_group`](data_tab.py), [`DataTab.create_range_group`](data_tab.py)。

### entrance.py
- [`TestData`](entrance.py) — 测试数据生成器与预览绘图辅助，用于本地测试与 UI 演示。
  - 数据生成器方法：[`TestData._generate_exp_data`](entrance.py), [`TestData._generate_multi_line_data`](entrance.py), [`TestData._generate_polynomial_data`](entrance.py), [`TestData._generate_gaussian_data`](entrance.py), [`TestData._generate_log_data`](entrance.py), [`TestData._generate_damped_oscillation_data`](entrance.py), [`TestData._generate_spiral_data`](entrance.py), [`TestData._generate_noise_data`](entrance.py), [`TestData._generate_step_data`](entrance.py)。
  - 站点/样本汇总与绘图：[`TestData.generate_single_site_plot_data`](entrance.py), [`TestData.generate_all_sites_plot_data`](entrance.py)。
  - 预览绘图：[`TestData._plot_single_site_preview`](entrance.py), [`TestData._plot_all_sites_preview`](entrance.py), [`TestData.plot_selection_preview_data`](entrance.py)。
  - 启动：[`launch_test_app`](entrance.py)。

### gen_2_magic.py
- 文件提供 generic -> MagIC 的转换与若干工具函数。
  - [`generic`](gen_2_magic.py) — 主转换函数，从通用文本/格式文件生成 MagIC 表并写出（measurements/specimens/samples/sites/locations）。
  - [`generic_to_middle_df`](gen_2_magic.py) — 便捷 wrapper，直接返回 middle dataframe。
  - 辅助函数：[`read_generic_file`](gen_2_magic.py), [`sort_magic_file`](gen_2_magic.py), [`average_duplicates`](gen_2_magic.py), [`get_upper_level_name`](gen_2_magic.py), [`merge_pmag_recs`](gen_2_magic.py)。
  - 数据处理/特征提取：[`get_unique_treatment_types`](gen_2_magic.py), [`extract_treatment_step`](gen_2_magic.py), [`calculate_directions`](gen_2_magic.py), [`get_treatment_type`](gen_2_magic.py)。
  - 简易 MagIC 类：[`MagicDataFrame`](gen_2_magic.py)（轻量读写 table），[`Contribution`](gen_2_magic.py)（用于管理 tables，含 `add_magic_table`, `add_magic_table_from_data`, `write_table_to_file` 等）。

### contribution_builder.py
- 项目中对 MagIC 表格进行操作的核心模块，包含完整的 Contribution 与 MagicDataFrame 实现（大量方法用于传播、合并、删除等）。
  - [`Contribution`](contribution_builder.py) — 管理多个 MagicDataFrame 的高层接口：
    - 表格管理：[`Contribution.add_magic_table`](contribution_builder.py), [`Contribution.add_magic_table_from_data`](contribution_builder.py), [`Contribution.add_empty_magic_table`](contribution_builder.py), [`Contribution.add_custom_filenames`](contribution_builder.py)。
    - 传播/补全：[`Contribution.propagate_measurement_info`](contribution_builder.py), [`Contribution.propagate_all_tables_info`](contribution_builder.py), [`Contribution.propagate_name_down`](contribution_builder.py), [`Contribution.propagate_cols`](contribution_builder.py), [`Contribution.propagate_cols_up`](contribution_builder.py), [`Contribution.propagate_min_max_up`](contribution_builder.py)。
    - 输出与校验：[`Contribution.write_table_to_file`](contribution_builder.py), [`Contribution.remove_non_magic_cols`](contribution_builder.py), [`Contribution.find_missing_items`](contribution_builder.py)。
  - [`MagicDataFrame`](contribution_builder.py) — 每个 MagIC 表的 DataFrame 封装，包含大量数据操作方法：
    - 行/列操作：[`MagicDataFrame.add_row`](contribution_builder.py), [`MagicDataFrame.update_row`](contribution_builder.py), [`MagicDataFrame.delete_row`](contribution_builder.py), [`MagicDataFrame.delete_rows`](contribution_builder.py), [`MagicDataFrame.delete_rows`](contribution_builder.py)（多次出现并有不同实现）。
    - 合并/转换：[`MagicDataFrame.merge_dfs`](contribution_builder.py), [`MagicDataFrame.all_to_str`](contribution_builder.py), [`MagicDataFrame.remove_non_magic_cols_from_table`](contribution_builder.py)。
    - 输出：[`MagicDataFrame.write_magic_file`](contribution_builder.py), [`MagicDataFrame.write_magic_file`](contribution_builder.py)（多处重载/不同路径处理）。
    - 专用：[`MagicDataFrame.get_di_block`](contribution_builder.py) — 从测量表中提取 DI block（返回 [[dec, inc], ...]）。

### IPRESETmqPint.py
- mqpint 与绘图 / 数据处理的综合模块，包含大量面向磁性/方向学分析与绘图工具。
  - 绘图/布局工具：[`mplot`](IPRESETmqPint.py), [`Szplot`](IPRESETmqPint.py), [`NSzplot`](IPRESETmqPint.py), [`arai1plot`](IPRESETmqPint.py), [`arai2plot`](IPRESETmqPint.py), [`RESETplotA`](IPRESETmqPint.py)。
  - 数据转换/处理：[`make_midle_df`](IPRESETmqPint.py)（或在此文件名为 `make_midle_df` / `make_midle_df`），[`generate_araidf`](IPRESETmqPint.py），[`makemqPint`](IPRESETmqPint.py）。
  - 步骤/排序工具：[`sortarai`](IPRESETmqPint.py） — 解析与分类实验步骤。
  - 数据结构：[`Specimen`](IPRESETmqPint.py), [`Site`](IPRESETmqPint.py), [`mqpintdata`](IPRESETmqPint.py) — 封装样本/站点信息并提供 critic/judge/plot 功能。

### IPresetQS6.py
- [`MainWindow`](IPresetQS6.py) — 主窗口的另一个实现（带数据选项卡与选择选项卡），含选择树、绘图更新、批量选择等方法：
  - 树/选择：[`MainWindow.get_selected_items`](IPresetQS6.py), [`MainWindow.select_all_items`](IPresetQS6.py), [`MainWindow.deselect_all_items`](IPresetQS6.py)。
  - 绘图：[`MainWindow.update_selection_plot`](IPresetQS6.py) — 根据选中项在画布上绘制示例数据或预览。
  - UI 构建：[`MainWindow.create_data_tab`](IPresetQS6.py), [`MainWindow.create_selection_tab`](IPresetQS6.py)。

### main_window.py
- [`MainWindow`](main_window.py) — 程序实际使用的主窗口类，集成 `MenuManager`, `DataTab`, `SelectionTab`，读取 `LayoutConfig` 并设置样式与布局。

### main.py
- [`main`](main.py) — 应用入口，创建 QApplication 并显示主窗口。

### menu_manager.py
- [`MenuManager`](menu_manager.py) — 菜单栏创建与操作（文件/打开/退出、快捷键绑定等）。

### mpl_canvas.py
- [`MplCanvas`](mpl_canvas.py) — Matplotlib FigureCanvas 的 Qt 封装，标准化画布行为。

### preview_manager.py
- 预览图管理：负责选择预览的生成、更新与导出（与 `entrance.TestData`、`selection_tab` 协作）。

### selection_tab.py
- 样本选择 UI：构造树状视图、选择/取消选择、导出与将选中项传回 DataTab，用于预览绘图。

### pmag.py / pint_plotting_functions.py / convert_2_magic.py / data_read_convert.py / color_picker.py / preview_manager.py
- 这些文件提供辅助工具：包含 pmag 兼容函数（路径解析、文件写入）、pint 相关的绘图函数、格式转换脚本、数据读取/转换辅助、颜色选择 UI 等（具体符号请在对应文件中查看实现）。

---

如果你希望我把上述内容直接写入工作区的 [workspacelist.md](workspacelist.md)，我可以把这份文档保存为该文件；或者你想要我把某个文件的函数说明扩展为更详细的 API 文档，请指明具体目标文件或类/函数名称。