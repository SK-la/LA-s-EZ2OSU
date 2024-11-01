#ui/settings.py
class ConversionSettings:
    def __init__(self, include_audio, include_images, remove_empty_columns, lock_cs_set, lock_cs_num, convert_sv, convert_sample_bg, auto_create_output_folder, source):
        self.include_audio = include_audio
        self.include_images = include_images
        self.remove_empty_columns = remove_empty_columns
        self.lock_cs_set = lock_cs_set
        self.lock_cs_num = lock_cs_num
        self.convert_sv = convert_sv
        self.convert_sample_bg = convert_sample_bg
        self.auto_create_output_folder = auto_create_output_folder
        self.source = source
