#config.py
import configparser
import os
import sys

class Config:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.default_config = {
            'Creator': 'SK_la',
            'HP': '8.5',
            'OD': '7',
            'Source': '',
            'Tags': '',
            'noS': 'N',
            'noP': 'N',
            'Packset': 'N'
        }
        self.config = configparser.ConfigParser()
        self._check_and_create_config()
        self._load_config()

    def _check_and_create_config(self):
        if not os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'w') as configfile:
                    # 写入注释和对应的配置项
                    configfile.write("# Mapper\n")
                    configfile.write("Creator = SK_la's MAPTool\n")
                    configfile.write("# Health Points\n")
                    configfile.write("HP = 8.5\n")
                    configfile.write("# Overall Difficulty\n")
                    configfile.write("OD = 7\n")
                    configfile.write("# Source of the map\n")
                    configfile.write("Source = SK_la's Tool\n")
                    configfile.write("# Add tags\n")
                    configfile.write("Tags = \n")
                    configfile.write("# NO Scratch?\n")
                    configfile.write("noS = N\n")
                    configfile.write("# NO PANEL?\n")
                    configfile.write("noP = N\n")
                    configfile.write("# Package in <mapper's APCK - Source> format?\n")
                    configfile.write("Packset = N\n")
                print(f"Configuration file '{self.config_file}' created with default values and comments.")
            except Exception as e:
                print(f"Failed to create configuration file: {e}")
                sys.exit(1)
        else:
            self.config.read(self.config_file)

    def _load_config(self):
        self.creator = self.config.get('DEFAULT', 'Creator')
        self.HP = self._format_float(self.config.getfloat('DEFAULT', 'HP'))
        self.OD = self._format_float(self.config.getfloat('DEFAULT', 'OD'))
        self.source = self.config.get('DEFAULT', 'Source').replace(':', "_")
        self.tags = self.config.get('DEFAULT', 'Tags')
        self.noS = self.config.get('DEFAULT', 'noS')
        self.noP = self.config.get('DEFAULT', 'noP')
        self.packset = self.config.get('DEFAULT', 'Packset')

    def _format_float(self, value):
        if value.is_integer():
            return int(value)
        return value

# 单例模式实现
_config_instance = None

def get_config():
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance

config = get_config()
print(f"Creator: {config.creator}")
print(f"HP: {config.HP}")
print(f"OD: {config.OD}")
print(f"Source: {config.source}")
print(f"Tags: {config.tags}")
print(f"noS: {config.noS}")
print(f"noP: {config.noP}")
print(f"Packset: {config.packset}")
