#ui/settings.py
import asyncio

from PyQt6.QtCore import pyqtSignal, QObject

from bin.aio import start_conversion

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

    def save_settings(self, settings):
        settings.setValue("include_audio", self.include_audio)
        settings.setValue("include_images", self.include_images)
        settings.setValue("remove_empty_columns", self.remove_empty_columns)
        settings.setValue("lock_cs_set", self.lock_cs_set)
        settings.setValue("lock_cs_num", self.lock_cs_num)
        settings.setValue("convert_sv", self.convert_sv)
        settings.setValue("convert_sample_bg", self.convert_sample_bg)
        settings.setValue("auto_create_output_folder", self.auto_create_output_folder)

    @classmethod
    def load_settings(cls, settings):
        include_audio = settings.value("include_audio", True, type=bool)
        include_images = settings.value("include_images", True, type=bool)
        remove_empty_columns = settings.value("remove_empty_columns", True, type=bool)
        lock_cs_set = settings.value("lock_cs_set", True, type=bool)
        lock_cs_num = settings.value("lock_cs_num", "14")
        convert_sv = settings.value("convert_sv", True, type=bool)
        convert_sample_bg = settings.value("convert_sample_bg", True, type=bool)
        auto_create_output_folder = settings.value("auto_create_output_folder", False, type=bool)
        return cls(include_audio, include_images, remove_empty_columns, lock_cs_set, lock_cs_num, convert_sv,
                   convert_sample_bg, auto_create_output_folder)

class ConversionWorker(QObject):
    conversion_finished = pyqtSignal()

    def __init__(self, input_path, output_path, settings, cache_folder):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.settings = settings
        self.cache_folder = cache_folder

    def run_conversion(self):
        asyncio.run(self._run_conversion())

    async def _run_conversion(self):
        await start_conversion(self.input_path, self.output_path, self.settings, self.cache_folder)
        self.conversion_finished.emit()
