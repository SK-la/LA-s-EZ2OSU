from config import get_config
from get_info import get_info, get_names
from conv_bmson import bms
from events import get_events
from osu import generate_osu_file
import json
import os
import logging
import json
import pathlib




def dispatch(data, settings):
    print("dispatch调度处理开始")
    config = get_config()
    info_obj = get_info(data, config)
    names_obj = get_names(info_obj, config)
    notes_obj, main_audio, offset, SongLg, new_CS = bms(data, info_obj, names_obj, settings)
    events, Samples = get_events(data, info_obj, offset)
    osu_content = generate_osu_file(config, info_obj, events, Samples, SongLg, notes_obj, new_CS)

    print("调度处理完成")

    # Output all query values
    # print('\n'"[Object]")
    # print(f"Title: {info_obj.title}")
    # print(f"Artist: {info_obj.artist}")
    # print(f"BPM: {info_obj.bpm}")
    # print(f"Image: {info_obj.image}")
    # print(f"Resolution: {info_obj.resolution}")
    # print(f"LN Type: {info_obj.ln_type}")
    print(f"Level: {info_obj.lv}")
    print(f"Tags: {info_obj.tags}")
    # print(f"Version: {info_obj.ver}")
    # print(f"Difficulty: {info_obj.diff}")
    print(f"Song: {info_obj.song}")
    print(f"Img: {names_obj.img_filename}")

    # print(f"CS: {info_obj.CS}")
    # print(f"Mode Hint: {info_obj.EZmode}")

    #print(f"TP0: {info_obj.TP0}")
    #print(f"PT: {info_obj.PT}")

    print(f"New Folder Name: {names_obj.new_folder}")
    print(f"Sub Folder Name: {names_obj.sub_folder}")
    print(f"Osu Filename: {names_obj.osu_filename}")


    #print(f"Main Audio: {main_audio}")
    #print(f"Offset: {offset}")

    #print(osu_content)

    print("\n调度转换完成")

    return osu_content, info_obj, names_obj, main_audio


def scan_folder(folder_path):
    files = []
    folder_path = os.path.normpath(folder_path)  # 规范化路径
    for root, _, filenames in os.walk(folder_path):
        root = os.path.normpath(root)  # 规范化路径
        for filename in filenames:
            file_path = os.path.join(root, filename)
            file_path = os.path.normpath(file_path)  # 规范化路径
            if os.path.isfile(file_path):
                files.append(file_path)
    return files

def print_collapsed(content, indent=2):
    print(json.dumps(content, indent=indent))

def setup_logging(log_file_path):
    # 确保 test 文件夹存在
    log_file_path = pathlib.Path(log_file_path)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )

# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 检查数据用
def check_lines(lines):
    for line in lines:
        if not line.endswith('.wav'):
            print(line)

