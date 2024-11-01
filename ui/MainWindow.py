# MainWindow.py
import pathlib
from PyQt5 import QtWidgets, QtGui, QtCore
from Dispatch_file import process_file
from ui.styling import set_window_icon, set_background_image
from ui.elements import setup_combobox, setup_checkboxes, setup_tabs
from ui.osu_path import get_osu_install_path
from config import config
class ConversionSettings:
    def __init__(self, include_audio, include_images, remove_empty_columns, lock_cs_set, lock_cs_num, convert_sv, convert_sample_bg, auto_create_output_folder):
        self.include_audio = include_audio
        self.include_images = include_images
        self.remove_empty_columns = remove_empty_columns
        self.lock_cs_set = lock_cs_set
        self.lock_cs_num = lock_cs_num
        self.convert_sv = convert_sv
        self.convert_sample_bg = convert_sample_bg
        self.auto_create_output_folder = auto_create_output_folder

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
        
        set_window_icon(self)
        set_background_image(self)

        main_layout = QtWidgets.QVBoxLayout(self)

        input_layout = QtWidgets.QHBoxLayout()
        self.input_path = DropLineEdit(self, "input")
        self.input_path.setPlaceholderText("输入文件夹路径")
        input_button = QtWidgets.QPushButton("设置输入")
        input_button.clicked.connect(self.select_input)
        input_layout.addWidget(self.input_path)
        input_layout.addWidget(input_button)
        main_layout.addLayout(input_layout)
        
        output_layout = QtWidgets.QHBoxLayout()
        self.output_path = DropLineEdit(self, "output")
        self.output_path.setPlaceholderText("输出文件夹路径")
        output_button = QtWidgets.QPushButton("设置输出")
        output_button.clicked.connect(self.select_output)
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(output_button)
        main_layout.addLayout(output_layout)
        
        self.start_button = QtWidgets.QPushButton("开始转换")
        self.start_button.clicked.connect(self.start_conversion)
        main_layout.addWidget(self.start_button)
        
        checkbox_layout = setup_checkboxes(self)
        main_layout.addLayout(checkbox_layout)

        lock_cs_num_layout = setup_combobox(self)
        main_layout.addLayout(lock_cs_num_layout)

        tabs = setup_tabs(self)
        main_layout.addWidget(tabs)

        # 应用外发光效果
        apply_glow_effect(self.start_button)
        apply_glow_effect(input_button)
        apply_glow_effect(output_button)

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
            lock_cs_num=self.lock_cs_num_combobox.currentText(),
            convert_sv=self.convert_sv.isChecked(),
            convert_sample_bg=self.convert_sample_bg.isChecked(),
            auto_create_output_folder=self.auto_create_output_folder.isChecked(),
        )
        # 自动创建输出文件夹
        if self.auto_create_output_folder.isChecked():
            osu_install_path = get_osu_install_path()
            if osu_install_path:
                osu_songs_path = osu_install_path / "Songs"
                config_source_folder = osu_songs_path / config.source
                config_source_folder.mkdir(parents=True, exist_ok=True)
                output_path = config_source_folder
                self.output_path.setText(str(output_path))
            else:
                QtWidgets.QMessageBox.warning(self, "错误", "无法找到 osu! 安装路径，请手动设置输出文件夹。")


        for bmson_file in input_path.glob("**/*.bmson"):
            # 处理文件并保存到对应的子目录
            self.names_obj = process_file(bmson_file, output_path, settings)

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
        self.settings.setValue("lock_cs_num", self.lock_cs_num_combobox.currentText())
        self.settings.setValue("convert_sv", self.convert_sv.isChecked())
        self.settings.setValue("convert_sample_bg", self.convert_sample_bg.isChecked())
        self.settings.setValue("auto_create_output_folder", self.auto_create_output_folder.isChecked())

    def load_settings(self):
        self.input_path.setText(self.settings.value("input_path", ""))
        self.output_path.setText(self.settings.value("output_path", ""))
        self.include_audio.setChecked(self.settings.value("include_audio", True, type=bool))
        self.include_images.setChecked(self.settings.value("include_images", True, type=bool))
        self.remove_empty_columns.setChecked(self.settings.value("remove_empty_columns", True, type=bool))
        self.lock_cs_set.setChecked(self.settings.value("lock_cs_set", True, type=bool))
        self.lock_cs_num_combobox.setCurrentText(self.settings.value("lock_cs_num", "14"))
        self.convert_sv.setChecked(self.settings.value("convert_sv", True, type=bool))
        self.convert_sample_bg.setChecked(self.settings.value("convert_sample_bg", True, type=bool))
        self.auto_create_output_folder.setChecked(self.settings.value("auto_create_output_folder", False, type=bool))

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
