#bin/config.py
import configparser
import pathlib

class Config:
    def __init__(self, config_file='config.ini'):
        # 使用绝对路径确保配置文件在程序的根目录下
        self.config_file = pathlib.Path(config_file).resolve()
        self.config = configparser.ConfigParser()
        self._check_and_create_config()
        self._load_config()

    def _check_and_create_config(self):
        if not self.config_file.exists():
            self.config['DEFAULT'] = {
                'Creator': 'SK_la',
                'HP': '8',
                'OD': '7',
                'Source': 'LA\'s EZ2OSU',
                'Tags': '',
                'noS': 'N',
                'noP': 'N',
                'Packset': 'N',
                'SpecificNumbers': '1,2,3,4,5,6,7,8,9,10,12,14,16,18',
            }
            with open(self.config_file, 'w', encoding='utf-8') as configfile:
                self.config.write(configfile)

    def _load_config(self):
        self.config.read(self.config_file)
        self.creator = self.config.get('DEFAULT', 'Creator')
        self.HP = self.config.get('DEFAULT', 'HP')
        self.OD = self.config.get('DEFAULT', 'OD')
        self.source = self.config.get('DEFAULT', 'Source')
        self.tags = self.config.get('DEFAULT', 'Tags')
        self.noS = self.config.get('DEFAULT', 'noS')
        self.noP = self.config.get('DEFAULT', 'noP')
        self.packset = self.config.get('DEFAULT', 'Packset')
        self.specific_numbers = self.config.get('DEFAULT', 'SpecificNumbers').split(',')

    def save_config(self, settings):
        self.config['DEFAULT'] = {
            'Creator': settings['creator'],
            'HP': settings['HP'],
            'OD': settings['OD'],
            'Source': settings['source'],
            'Tags': settings['tags'],
            'noS': settings['noS'],
            'noP': settings['noP'],
            'Packset': settings['packset'],
            'SpecificNumbers': ','.join(settings['specific_numbers'])
        }
        with open(self.config_file, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)

# 单例模式实现
_config_instance = None

def get_config():
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance

config = get_config()
