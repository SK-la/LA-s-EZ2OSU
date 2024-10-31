# process_data.py
import os
from events import get_events
from get_info import get_info, get_names



def process_data(data):
    # 调用 get_info 函数
    info_obj = get_info(data)

    # 调用 get_names 函数
    names_obj = get_names(info_obj)

    # 调用 get_events 函数
    events_obj = get_events(data)

    # 假设 notes 函数存在
    notes = notes(data, info_obj, names_obj)

    return info_obj, events_obj, names_obj

def ext():
    img_ext = ('.jpg', '.png', '.gif', '.bmp')
    sod_ext = ('.mp3', '.wav')
    anm_ext = ('.mp4', '.avi', '.wmv')
    return img_ext, sod_ext, anm_ext

""" #test
if __name__ == "__main__":
    # 示例数据
    data = {


} """





