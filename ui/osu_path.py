#osu_path.py
import pathlib
import winreg
from PyQt5.QtWidgets import QFileDialog, QMessageBox

def get_osu_install_path(parent=None):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\osu!")
        install_path, _ = winreg.QueryValueEx(registry_key, "InstallLocation")
        winreg.CloseKey(registry_key)
        return pathlib.Path(install_path)
    except FileNotFoundError:
        # 弹出对话框让用户选择路径
        install_path = QFileDialog.getExistingDirectory(parent, "选择 osu! 安装路径")
        if install_path:
            return pathlib.Path(install_path)
        else:
            QMessageBox.warning(parent, "错误", "未选择 osu! 安装路径，请手动设置输出文件夹。")
            return None

# 示例使用
# osu_install_path = get_osu_install_path()
# print(osu_install_path)
