# ui/settings_tab.py
from PyQt6 import QtWidgets

class SettingsTab(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.creator_label = None
        self.creator_input = None
        self.hp_label = None
        self.hp_input = None
        self.od_label = None
        self.od_input = None
        self.source_label = None
        self.source_input = None
        self.tags_label = None
        self.tags_input = None
        self.noS_checkbox = None
        self.noP_checkbox = None
        self.packset_checkbox = None
        self.specific_numbers_label = None
        self.specific_numbers_input = None
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        self.noS_checkbox = QtWidgets.QCheckBox("No Scratch")
        self.noS_checkbox.setChecked(self.main_window.config.noS == 'Y')

        self.noP_checkbox = QtWidgets.QCheckBox("No Panel")
        self.noP_checkbox.setChecked(self.main_window.config.noP == 'Y')

        self.packset_checkbox = QtWidgets.QCheckBox("Packset")
        self.packset_checkbox.setChecked(self.main_window.config.packset == 'Y')

        self.creator_label = QtWidgets.QLabel("Creator:")
        self.creator_input = QtWidgets.QLineEdit()
        self.creator_input.setText(self.main_window.config.creator)

        self.hp_label = QtWidgets.QLabel("HP:")
        self.hp_input = QtWidgets.QLineEdit()
        self.hp_input.setText(str(self.main_window.config.HP))

        self.od_label = QtWidgets.QLabel("OD:")
        self.od_input = QtWidgets.QLineEdit()
        self.od_input.setText(str(self.main_window.config.OD))

        self.source_label = QtWidgets.QLabel("Source:")
        self.source_input = QtWidgets.QLineEdit()
        self.source_input.setText(self.main_window.config.source)

        self.tags_label = QtWidgets.QLabel("Tags:")
        self.tags_input = QtWidgets.QLineEdit()
        self.tags_input.setText(self.main_window.config.tags)

        self.specific_numbers_label = QtWidgets.QLabel("N to N key button:")
        self.specific_numbers_input = QtWidgets.QLineEdit()
        self.specific_numbers_input.setText(','.join(self.main_window.config.specific_numbers))

        save_button = QtWidgets.QPushButton("保存设置")
        save_button.clicked.connect(self.save_settings)

        layout.addWidget(self.noS_checkbox)
        layout.addWidget(self.noP_checkbox)
        layout.addWidget(self.packset_checkbox)
        layout.addWidget(self.source_label)
        layout.addWidget(self.source_input)
        layout.addWidget(self.creator_label)
        layout.addWidget(self.creator_input)
        layout.addWidget(self.hp_label)
        layout.addWidget(self.hp_input)
        layout.addWidget(self.od_label)
        layout.addWidget(self.od_input)
        layout.addWidget(self.tags_label)
        layout.addWidget(self.tags_input)
        layout.addWidget(self.specific_numbers_label)
        layout.addWidget(self.specific_numbers_input)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_settings(self):
        self.main_window.config.creator = self.creator_input.text()
        self.main_window.config.HP = float(self.hp_input.text())
        self.main_window.config.OD = float(self.od_input.text())
        self.main_window.config.source = self.source_input.text()
        self.main_window.config.tags = self.tags_input.text()
        self.main_window.config.noS = 'Y' if self.noS_checkbox.isChecked() else 'N'
        self.main_window.config.noP = 'Y' if self.noP_checkbox.isChecked() else 'N'
        self.main_window.config.packset = 'Y' if self.packset_checkbox.isChecked() else 'N'
        self.main_window.config.specific_numbers = self.specific_numbers_input.text().split(',')
        # 保存输入输出路径和复选框状态
        self.main_window.settings.setValue("input_path", self.main_window.input_path.text())
        self.main_window.settings.setValue("output_path", self.main_window.output_path.text())
        self.main_window.settings.setValue("include_audio", self.main_window.include_audio.isChecked())
        self.main_window.settings.setValue("include_images", self.main_window.include_images.isChecked())
        self.main_window.settings.setValue("remove_empty_columns", self.main_window.remove_empty_columns.isChecked())
        self.main_window.settings.setValue("lock_cs_set", self.main_window.lock_cs_set.isChecked())
        self.main_window.settings.setValue("lock_cs_num", self.main_window.lock_cs_num_combobox.currentText())
        self.main_window.settings.setValue("convert_sv", self.main_window.convert_sv.isChecked())
        self.main_window.settings.setValue("convert_sample_bg", self.main_window.convert_sample_bg.isChecked())
        self.main_window.settings.setValue("auto_create_output_folder",
                                           self.main_window.auto_create_output_folder.isChecked())
        self.main_window.settings.setValue("source", self.source_input.text())
        self.main_window.settings.setValue("noS", self.main_window.config.noS)
        self.main_window.settings.setValue("noP", self.main_window.config.noP)
        self.main_window.settings.setValue("packset", self.main_window.config.packset)

        self.main_window.config.save_config({
            'creator': self.creator_input.text(),
            'HP': self.hp_input.text(),
            'OD': self.od_input.text(),
            'source': self.source_input.text(),
            'tags': self.tags_input.text(),
            'noS': self.main_window.config.noS,
            'noP': self.main_window.config.noP,
            'packset': self.main_window.config.packset,
            'specific_numbers': self.specific_numbers_input.text().split(','),
        })
        self.main_window.show_notification("Settings saved successfully!")
