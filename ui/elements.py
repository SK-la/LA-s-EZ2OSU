# ui/elements.py
from PyQt5 import QtWidgets
from ui.home_tab import HomeTab
from ui.clm_tab import ClmTab

def setup_combobox(main_window):
    lock_cs_num_layout = QtWidgets.QHBoxLayout()
    main_window.auto_create_output_folder = QtWidgets.QCheckBox("自动创建输出文件夹")
    main_window.auto_create_output_folder.setChecked(False)
    lock_cs_num_layout.addWidget(main_window.auto_create_output_folder)
    lock_cs_num_layout.addStretch()
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
    main_window.remove_empty_columns = QtWidgets.QCheckBox("去除原谱空列")
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
    main_window.home_tab = HomeTab(main_window)
    main_window.tabs.addTab(main_window.home_tab, "Home")
    main_window.clm_tab = ClmTab(main_window)
    main_window.tabs.addTab(main_window.clm_tab, "Clm")
    # 未来可以在这里添加其他标签页
    # self.other_tab = OtherTab(self)
    # self.tabs.addTab(self.other_tab, "Other")
    return main_window.tabs
