#ui/layouts.py
from PyQt5 import QtWidgets, QtGui
import pathlib

def setup_combobox(main_window):
    lock_cs_num_layout = QtWidgets.QHBoxLayout()
    main_window.lock_cs_num_label = QtWidgets.QLabel("选择锁定的CS数:")
    main_window.lock_cs_num_label.setStyleSheet("color: black;")
    main_window.lock_cs_num_combobox = QtWidgets.QComboBox()
    main_window.lock_cs_num_combobox.addItems(["14", "16", "10", "8"])
    main_window.lock_cs_num_combobox.setFixedWidth(50)
    lock_cs_num_layout.addWidget(main_window.lock_cs_num_label)
    lock_cs_num_layout.addWidget(main_window.lock_cs_num_combobox)
    return lock_cs_num_layout

def setup_checkboxes(main_window):
    checkbox_layout = QtWidgets.QHBoxLayout()
    main_window.include_audio = QtWidgets.QCheckBox("包含音频文件")
    main_window.include_audio.setChecked(True)
    main_window.include_images = QtWidgets.QCheckBox("包含图片文件")
    main_window.include_images.setChecked(True)
    main_window.convert_sv = QtWidgets.QCheckBox("转换SV")
    main_window.convert_sv.setChecked(True)
    main_window.convert_sample_bg = QtWidgets.QCheckBox("转换采样背景音")
    main_window.convert_sample_bg.setChecked(True)
    main_window.remove_empty_columns = QtWidgets.QCheckBox("去除空列")
    main_window.remove_empty_columns.setChecked(True)
    main_window.lock_cs_set = QtWidgets.QCheckBox("去除空列时锁定CS数")
    main_window.lock_cs_set.setChecked(True)
    
    checkbox_layout.addWidget(main_window.include_audio)
    checkbox_layout.addWidget(main_window.include_images)
    checkbox_layout.addWidget(main_window.convert_sv)
    checkbox_layout.addWidget(main_window.convert_sample_bg)
    checkbox_layout.addWidget(main_window.remove_empty_columns)
    checkbox_layout.addWidget(main_window.lock_cs_set)
    return checkbox_layout

def setup_tabs(main_window):
    main_window.tabs = QtWidgets.QTabWidget()
    from ui.home_tab import HomeTab
    main_window.home_tab = HomeTab(main_window)
    main_window.tabs.addTab(main_window.home_tab, "Home")
    from ui.clm_tab import ClmTab
    main_window.clm_tab = ClmTab(main_window)
    main_window.tabs.addTab(main_window.clm_tab, "Clm")
    from ui.settings_tab import SettingsTab
    main_window.settings_tab = SettingsTab(main_window)
    main_window.tabs.addTab(main_window.settings_tab, "Settings")
    return main_window.tabs

def setup_main_layout(central_widget, main_window):
    main_layout = QtWidgets.QVBoxLayout(central_widget)

    input_layout = QtWidgets.QHBoxLayout()
    main_window.input_path = DropLineEdit(main_window, "input")
    main_window.input_path.setPlaceholderText("输入文件夹路径")
    input_button = QtWidgets.QPushButton("设置输入")
    input_button.clicked.connect(main_window.select_input)
    input_layout.addWidget(main_window.input_path)
    input_layout.addWidget(input_button)
    main_layout.addLayout(input_layout)
    
    output_layout = QtWidgets.QHBoxLayout()
    main_window.output_path = DropLineEdit(main_window, "output")
    main_window.output_path.setPlaceholderText("输出文件夹路径")
    output_button = QtWidgets.QPushButton("设置输出")
    output_button.clicked.connect(main_window.select_output)
    output_layout.addWidget(main_window.output_path)
    output_layout.addWidget(output_button)
    main_layout.addLayout(output_layout)

    main_window.start_button = QtWidgets.QPushButton("开始转换")
    main_window.start_button.clicked.connect(main_window.start_conversion)
    main_layout.addWidget(main_window.start_button)
    
    checkbox_layout = setup_checkboxes(main_window)
    main_layout.addLayout(checkbox_layout)

    lock_cs_num_layout = setup_combobox(main_window)
    main_layout.addLayout(lock_cs_num_layout)

    auto_create_output_folder_layout = QtWidgets.QHBoxLayout()
    main_window.auto_create_output_folder = QtWidgets.QCheckBox("自动创建主文件夹")
    main_window.auto_create_output_folder.setChecked(False)
    auto_create_output_folder_layout.addWidget(main_window.auto_create_output_folder)
    auto_create_output_folder_layout.addStretch()
    main_layout.addLayout(auto_create_output_folder_layout)

    tabs = setup_tabs(main_window)
    main_layout.addWidget(tabs)

    # 应用外发光效果
    apply_glow_effect(main_window.start_button)
    apply_glow_effect(input_button)
    apply_glow_effect(output_button)

class DropLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None, path_type="input"):
        super().__init__(parent)
        self.path_type = path_type
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if pathlib.Path(path).is_dir():
                self.setText(path)
                if self.path_type == "input":
                    self.parent().home_tab.input_tree.populate_tree(pathlib.Path(path))
                elif self.path_type == "output":
                    self.parent().home_tab.output_tree.populate_tree(pathlib.Path(path))

def apply_glow_effect(widget):
    glow_effect = QtWidgets.QGraphicsDropShadowEffect()
    glow_effect.setBlurRadius(5)
    glow_effect.setColor(QtGui.QColor(3, 3, 3, 100))
    glow_effect.setOffset(0, 0)
    widget.setGraphicsEffect(glow_effect)
