#ui/translations.py
import json
import os

def load_translations(language_code):
    file_path = os.path.join(os.path.dirname(__file__), 'locales', f'{language_code}.json')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def get_system_language():
    import locale
    system_language, _ = locale.getdefaultlocale()
    return system_language
