# MainWindow.py
import pathlib
import concurrent.futures
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QStatusBar
from PyQt5.QtGui import QCursor
from config import get_config
from Dispatch_file import process_file
from ui.styling import set_window_icon, set_background_image
from ui.layouts import setup_main_layout
from ui.translations import load_translations, get_system_language
from ui.osu_path import get_osu_songs_path
from ui.settings import ConversionSettings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.settings = QtCore.QSettings("LAZ", "EZ2OSU")
        self.config = get_config()
        system_language = get_system_language()
        self.translations = load_translations(system_language)
        self.initUI()
        self.update_language()  # 更新界面语言
        self.load_settings()  # 加载设置
        self.move_to_cursor()

    def initUI(self):
        self.setWindowTitle('LAs EZ2OSU')
        self.setGeometry(100, 100, 800, 600)
        set_window_icon(self)
        set_background_image(self)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)  # 使用 QMainWindow 的 setCentralWidget 方法
        setup_main_layout(central_widget, self)  # 传递 central_widget 和 MainWindow 实例

        self.auto_create_output_folder.stateChanged.connect(self.handle_auto_create_output_folder)

        # 添加状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def show_notification(self, message):
        self.status_bar.showMessage(message, 3000)  # 显示消息3秒

    def update_language(self):
        # 更新界面语言的逻辑
        self.setWindowTitle(self.translations.get('window_title', 'LAs EZ2OSU'))
        self.start_button.setText(self.translations.get('start_conversion', '开始转换'))
        self.input_path.setPlaceholderText(self.translations.get('input_folder_path', '输入文件夹路径'))
        self.output_path.setPlaceholderText(self.translations.get('output_folder_path', '输出文件夹路径'))
        # 更新其他需要翻译的控件文本

    def move_to_cursor(self):
        cursor_pos = QCursor.pos()
        self.move(cursor_pos.x(), cursor_pos.y())

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

    def handle_auto_create_output_folder(self, state):
        if state == QtCore.Qt.Checked:
            osu_songs_path = self.settings.value("osu_songs_path", None)
            if not osu_songs_path:
                osu_songs_path = get_osu_songs_path(self)
                if osu_songs_path:
                    self.settings.setValue("osu_songs_path", osu_songs_path)
                else:
                    QMessageBox.warning(self, "错误", "未选择 osu! 安装路径，请手动设置输出文件夹。")
                    self.auto_create_output_folder.setChecked(False)

    def process_folder(self, folder_path, output_path, settings):
        for bmson_file in folder_path.glob("**/*.bmson"):
            process_file(bmson_file, output_path, settings)

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
            source=self.config.source,
        )
        # 自动创建输出文件夹
        if self.auto_create_output_folder.isChecked():
            osu_songs_path = pathlib.Path(self.settings.value("osu_songs_path"))
            set_output_folder = osu_songs_path / settings.source
            set_output_folder.mkdir(parents=True, exist_ok=True)
            output_path = set_output_folder
            self.output_path.setText(str(output_path))
        else:
            # 使用用户选择的输出路径
            set_output_folder = output_path / settings.source
            set_output_folder.mkdir(parents=True, exist_ok=True)

        # 使用多线程处理文件夹
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for folder in input_path.iterdir():
                if folder.is_dir():
                    futures.append(executor.submit(self.process_folder, folder, output_path, settings))
            
            # 等待所有线程完成
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error processing folder: {e}")
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
        self.settings.setValue("source", self.config.source)
        self.show_notification("Settings saved successfully!")

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
        self.config.source = self.settings.value("source", "")

        # 加载文件树
        input_path = pathlib.Path(self.input_path.text())
        output_path = pathlib.Path(self.output_path.text())
        if input_path.exists():
            self.home_tab.input_tree.populate_tree(input_path)
        if output_path.exists():
            self.home_tab.output_tree.populate_tree(output_path)


