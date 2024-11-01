#osu_path
import pathlib
import winreg

def get_osu_install_path():
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\osu!")
        install_path, _ = winreg.QueryValueEx(registry_key, "InstallLocation")
        winreg.CloseKey(registry_key)
        return pathlib.Path(install_path)
    except FileNotFoundError:
        return pathlib.Path("E:\Game\MUG OSU\OSU!")  # 默认路径或提示用户设置路径


    

# 示例使用
#print(osu_songs_path)
