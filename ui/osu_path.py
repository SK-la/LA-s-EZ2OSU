#osu_path.py
import pathlib
import winreg
from PyQt5.QtWidgets import QFileDialog, QMessageBox

def get_osu_songs_path(parent=None):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\osu!")
        songs_path, _ = winreg.QueryValueEx(registry_key, "SONGS Location")
        winreg.CloseKey(registry_key)
        return pathlib.Path(songs_path)
    except FileNotFoundError:
        # 弹出对话框让用户选择路径
        songs_path = QFileDialog.getExistingDirectory(parent, "选择 osu! songs路径")
        if songs_path:
            return pathlib.Path(songs_path)
        else:
            QMessageBox.warning(parent, "错误", "未选择 songs 路径，请手动设置输出文件夹。")
            return None

# 示例使用
# osu_songs_path = get_osu_songs_path()
# print(osu_songs_path)
