import pathlib, asyncio, urllib.parse
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QStatusBar
from qasync import asyncSlot
from ui.styling import set_window_icon, set_background_image
from ui.layouts import setup_main_layout
from ui.translations import load_translations, get_system_language
from ui.osu_path import get_osu_songs_path
from ui.settings import ConversionSettings
from bin.config import get_config
from bin.aio import start_conversion

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.settings = QtCore.QSettings("LAZ", "EZ2OSU")
        self.config = get_config()
        system_language = get_system_language()
        self.translations = load_translations(system_language)
        self.status_bar = QStatusBar()

        self.initUI()
        self.update_language()
        self.load_settings()
        self.restore_window_position()

    def initUI(self):
        self.setWindowTitle('LAs EZ2OSU')
        self.setGeometry(100, 100, 800, 600)
        set_window_icon(self)
        set_background_image(self)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        setup_main_layout(central_widget, self)

        self.auto_create_output_folder.stateChanged.connect(self.handle_auto_create_output_folder)
        self.setStatusBar(self.status_bar)  # 添加状态栏

    def show_notification(self, message):
        self.status_bar.showMessage(message, 3000)  # 显示消息3秒

    def update_language(self):
        # 更新界面语言的逻辑
        self.start_button.setText(self.translations.get('start_conversion', '开始转换'))
        self.input_path.setPlaceholderText(self.translations.get('input_folder_path', '输入文件夹路径'))
        self.output_path.setPlaceholderText(self.translations.get('output_folder_path', '输出文件夹路径'))
        # 更新其他需要翻译的控件文本

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
        if state == QtCore.Qt.CheckState.Checked:
            osu_songs_path = self.settings.value("osu_songs_path", None)
            if not osu_songs_path:
                osu_songs_path = get_osu_songs_path(self)
                if osu_songs_path:
                    self.settings.setValue("osu_songs_path", osu_songs_path)
                else:
                    QMessageBox.warning(self, "错误", "未选择 osu! 安装路径，请手动设置输出文件夹。")
                    self.auto_create_output_folder.setChecked(False)

    @asyncSlot()
    async def start_conversion(self):
        input_path = urllib.parse.unquote_plus(self.input_path.text())
        output_path = self.output_path.text()
        settings = self.get_conversion_settings()
        self.update_file_trees(pathlib.Path(input_path), pathlib.Path(output_path))

        # 自动创建输出文件夹
        if self.auto_create_output_folder.isChecked():
            osu_songs_path = pathlib.Path(self.settings.value("osu_songs_path"))
            output_path = self.create_output_folder(osu_songs_path)
            self.output_path.setText(str(output_path))
        else:
            output_path = self.create_output_folder(pathlib.Path(output_path))
        # 定义哈希缓存的基础文件夹
        cache_folder = pathlib.Path("hash_cache")
        # 调用异步处理脚本
        await start_conversion(input_path, output_path, settings, cache_folder)
        self.update_file_trees(pathlib.Path(input_path), pathlib.Path(output_path))

    def create_output_folder(self, base_path):
        set_output_folder = base_path / self.config.source
        set_output_folder.mkdir(parents=True, exist_ok=True)
        return set_output_folder

    def update_file_trees(self, input_path, output_path):
        self.home_tab.input_tree.populate_tree(input_path)
        self.home_tab.output_tree.populate_tree(output_path)

    def restore_window_position(self):
        pos = self.settings.value("window_position", None)
        if pos:
            self.move(pos)

    def closeEvent(self, event):
        self.save_window_position()
        self.save_settings()
        loop = asyncio.get_event_loop()
        for task in asyncio.all_tasks(loop):
            task.cancel()
        loop.stop()
        event.accept()

    def save_window_position(self):
        self.settings.setValue("window_position", self.pos())

    def save_settings(self):
        self.settings.setValue("input_path", self.input_path.text())
        self.settings.setValue("output_path", self.output_path.text())
        self.settings.setValue("source", self.config.source)
        self.get_conversion_settings().save_settings(self.settings)
        self.show_notification("Settings saved successfully!")

    def load_settings(self):
        self.input_path.setText(self.settings.value("input_path", ""))
        self.output_path.setText(self.settings.value("output_path", ""))
        self.config.source = self.settings.value("source", "")
        settings = ConversionSettings.load_settings(self.settings)
        self.include_audio.setChecked(settings.include_audio)
        self.include_images.setChecked(settings.include_images)
        self.remove_empty_columns.setChecked(settings.remove_empty_columns)
        self.lock_cs_set.setChecked(settings.lock_cs_set)
        self.lock_cs_num_combobox.setCurrentText(settings.lock_cs_num)
        self.convert_sv.setChecked(settings.convert_sv)
        self.convert_sample_bg.setChecked(settings.convert_sample_bg)
        self.auto_create_output_folder.setChecked(settings.auto_create_output_folder)

        # 加载文件树
        input_path = pathlib.Path(self.input_path.text())
        output_path = pathlib.Path(self.output_path.text())
        if input_path.exists():
            self.home_tab.input_tree.populate_tree(input_path)
        if output_path.exists():
            self.home_tab.output_tree.populate_tree(output_path)

    def get_conversion_settings(self):
        # 获取转换设置的逻辑
        settings = ConversionSettings(
            include_audio=self.include_audio.isChecked(),
            include_images=self.include_images.isChecked(),
            remove_empty_columns=self.remove_empty_columns.isChecked(),
            lock_cs_set=self.lock_cs_set.isChecked(),
            lock_cs_num=self.lock_cs_num_combobox.currentText(),
            convert_sv=self.convert_sv.isChecked(),
            convert_sample_bg=self.convert_sample_bg.isChecked(),
            auto_create_output_folder=self.auto_create_output_folder.isChecked()
        )
        return settings