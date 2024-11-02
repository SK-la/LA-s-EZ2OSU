#Dispatch_data.py
from config import get_config
from get_info import get_info
from conv_bmson import bms
from SV import get_sv
from Samples import get_samples
from osu import generate_osu_file
import os
import logging
import json
import pathlib
from mod.clm_no_empty import remove_empty_columns
from mod.lock_cs import lock_cs


def dispatch(data, settings):
    config = get_config()
    info = get_info(data, config)
    samples,  main_audio, offset, song_lg = get_samples(data, info, settings)
    notes_obj, cs = bms(data, info, offset)
    #print("bms 函数返回的 notes_obj 内容:", notes_obj)
    new_cs = cs
    if info.osumode == 3:
        #mod
        if settings.lock_cs_set:
            notes_obj = lock_cs(notes_obj, cs, int(settings.lock_cs_num))
        if settings.remove_empty_columns:
            notes_obj, new_cs = remove_empty_columns(notes_obj, cs)

    sv = get_sv(data, offset, info, settings) if settings.convert_sv else ''
    #print("c e c 返回的 notes_obj 类型:", type(notes_obj))
    osu_content = generate_osu_file(config, info, sv, offset, samples, song_lg, notes_obj, new_cs)



    # Output all query values
    # print('\n'"[Object]")
    # print(f"Title: {info.title}")
    # print(f"Artist: {info.artist}")
    # print(f"BPM: {info.bpm}")
    # print(f"Image: {info.image}")
    # print(f"Resolution: {info.resolution}")
    # print(f"LN Type: {info.ln_type}")
    #print(f"Level: {info.lv}")
    #print(f"Tags: {info.tags}")
    # print(f"Version: {info.ver}")
    # print(f"Difficulty: {info.diff}")
    #print(f"Song: {info.song}")
    # print(f"CS: {info.CS}")
    # print(f"Mode Hint: {info.ez_mode}")

    print(f"New Folder Name: {info.new_folder}")
    print(f"Sub Folder Name: {info.sub_folder}")
    print(f"Osu Filename: {info.osu_filename}")
    print(f"Img: {info.img_filename}")

    #print(f"Main Audio: {main_audio}")
    #print(f"Offset: {offset}")
    #print(osu_content)

    print("\n调度转换完成")

    return osu_content, info, main_audio


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
        format='%(pastime)s - %(name)s - %(levelness)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )

# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(pastime)s - %(levelness)s - %(message)s')
