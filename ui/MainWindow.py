import pathlib
from PyQt5 import QtWidgets, QtGui, QtCore
from Dispatch_file import process_file
from ui.ui_styling import set_window_icon, set_background_image
from ui.home_tab import HomeTab
from ui.clm_tab import ClmTab

# 未来可以导入其他标签页
# from ui.other_tab import OtherTab

class ConversionSettings:
    def __init__(self, include_audio, include_images, remove_empty_columns, lock_cs_set, cs_number):
        self.include_audio = include_audio
        self.include_images = include_images
        self.remove_empty_columns = remove_empty_columns
        self.lock_cs_set = lock_cs_set
        self.cs_number = cs_number

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.settings = QtCore.QSettings("MyCompany", "MyApp")  # 使用 QSettings
        self.initUI()
        self.load_settings()  # 加载设置

    def initUI(self):
        self.setWindowTitle('LAs EZ2OSU')
        self.setGeometry(100, 100, 800, 600)
        
        # 设置窗口图标和背景图片
        set_window_icon(self)
        set_background_image(self)

        main_layout = QtWidgets.QVBoxLayout(self)

        # 输入文件夹路径
        input_layout = QtWidgets.QHBoxLayout()
        self.input_path = DropLineEdit(self, "input")
        self.input_path.setPlaceholderText("输入文件夹路径")
        input_button = QtWidgets.QPushButton("设置输入")
        input_button.clicked.connect(self.select_input)
        input_layout.addWidget(self.input_path)
        input_layout.addWidget(input_button)
        main_layout.addLayout(input_layout)
        
        # 输出文件夹路径
        output_layout = QtWidgets.QHBoxLayout()
        self.output_path = DropLineEdit(self, "output")
        self.output_path.setPlaceholderText("输出文件夹路径")
        output_button = QtWidgets.QPushButton("设置输出")
        output_button.clicked.connect(self.select_output)
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(output_button)
        main_layout.addLayout(output_layout)
        
        # 开始转换按钮
        self.start_button = QtWidgets.QPushButton("开始转换")
        self.start_button.clicked.connect(self.start_conversion)
        main_layout.addWidget(self.start_button)
        
        # 复选框
        checkbox_layout = QtWidgets.QHBoxLayout()
        self.include_audio = QtWidgets.QCheckBox("包含音频文件")
        self.include_audio.setChecked(True)  # 默认勾选
        self.include_images = QtWidgets.QCheckBox("包含图片文件")
        self.include_images.setChecked(True)  # 默认勾选
        self.remove_empty_columns = QtWidgets.QCheckBox("去除原谱空列")
        self.remove_empty_columns.setChecked(True)  # 默认勾选
        self.lock_cs_set = QtWidgets.QCheckBox("去除空列时锁定CS数")
        self.lock_cs_set.setChecked(True)  # 默认勾选
        checkbox_layout.addWidget(self.include_audio)
        checkbox_layout.addWidget(self.include_images)  
        checkbox_layout.addWidget(self.remove_empty_columns)
        checkbox_layout.addWidget(self.lock_cs_set)
        main_layout.addLayout(checkbox_layout)

        # 添加下拉栏
        cs_number_layout = QtWidgets.QHBoxLayout()
        cs_number_layout.addStretch()  # 添加弹性空间以确保右对齐
        self.cs_number_label = QtWidgets.QLabel("选择锁定的CS数:")
        self.cs_number_label.setStyleSheet("color: black;")
        self.cs_number_combobox = QtWidgets.QComboBox()
        self.cs_number_combobox.addItems(["14", "16", "10", "8"])  # 添加可选的CS数
        # 锁定下拉栏宽度
        self.cs_number_combobox.setFixedWidth(50)  # 你可以根据需要调整宽度值
        cs_number_layout.addWidget(self.cs_number_label)
        cs_number_layout.addWidget(self.cs_number_combobox)
        main_layout.addLayout(cs_number_layout)

        # 标签页
        self.tabs = QtWidgets.QTabWidget()
        self.home_tab = HomeTab(self)
        self.tabs.addTab(self.home_tab, "Home")
        self.clm_tab = ClmTab(self)
        self.tabs.addTab(self.clm_tab, "Clm")

        # 未来可以在这里添加其他标签页
        # self.other_tab = OtherTab(self)
        # self.tabs.addTab(self.other_tab, "Other")
        
        # 应用外发光效果
        apply_glow_effect(self.start_button)
        apply_glow_effect(input_button)
        apply_glow_effect(output_button)

        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)

    def select_input(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择输入文件夹")
        if path:
            self.input_path.setText(path)
            self.home_tab.input_tree.populate_tree(pathlib.Path(path))

    def select_output(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if path:
            self.output_path.setText(path)
            self.home_tab.output_tree.populate_tree(pathlib.Path(path))

    def start_conversion(self):
        input_path = pathlib.Path(self.input_path.text())
        output_path = pathlib.Path(self.output_path.text())
        
        # 获取复选框和下拉框的值
        settings = ConversionSettings(
            include_audio=self.include_audio.isChecked(),
            include_images=self.include_images.isChecked(),
            remove_empty_columns=self.remove_empty_columns.isChecked(),
            lock_cs_set=self.lock_cs_set.isChecked(),
            cs_number=self.cs_number_combobox.currentText()
        )
        
        for bmson_file in input_path.glob("**/*.bmson"):
            # 在输出路径中创建对应的子目录
            relative_path = bmson_file.relative_to(input_path)
            target_dir = output_path / relative_path.parent
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # 处理文件并保存到对应的子目录
            self.names_obj = process_file(bmson_file, target_dir, settings)

        # 更新文件树
        self.home_tab.input_tree.populate_tree(input_path)
        self.home_tab.output_tree.populate_tree(output_path)

    def closeEvent(self, event):
        self.save_settings()
        event.accept()

    def save_settings(self):
        self.settings.setValue("input_path", self.input_path.text())
        self.settings.setValue("output_path", self.output_path.text())
        self.settings.setValue("include_audio", self.include_audio.isChecked())
        self.settings.setValue("include_images", self.include_images.isChecked())
        self.settings.setValue("remove_empty_columns", self.remove_empty_columns.isChecked())
        self.settings.setValue("lock_cs_set", self.lock_cs_set.isChecked())
        self.settings.setValue("cs_number", self.cs_number_combobox.currentText())

    def load_settings(self):
        self.input_path.setText(self.settings.value("input_path", ""))
        self.output_path.setText(self.settings.value("output_path", ""))
        self.include_audio.setChecked(self.settings.value("include_audio", True, type=bool))
        self.include_images.setChecked(self.settings.value("include_images", True, type=bool))
        self.remove_empty_columns.setChecked(self.settings.value("remove_empty_columns", True, type=bool))
        self.lock_cs_set.setChecked(self.settings.value("lock_cs_set", True, type=bool))
        self.cs_number_combobox.setCurrentText(self.settings.value("cs_number", "14"))

        # 加载文件树
        input_path = pathlib.Path(self.input_path.text())
        output_path = pathlib.Path(self.output_path.text())
        if input_path.exists():
            self.home_tab.input_tree.populate_tree(input_path)
        if output_path.exists():
            self.home_tab.output_tree.populate_tree(output_path)

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
