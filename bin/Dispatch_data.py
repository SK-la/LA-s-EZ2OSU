import os
from bin.config import get_config
from bin.get_info import get_info
from bin.conv_bmson import bms
from bin.SV import get_sv
from bin.Samples import get_samples
from bin.osu import generate_osu_file
from mod.clm_no_empty import remove_empty_columns
from mod.lock_cs import lock_cs
from bin.custom_log import setup_custom_logger

logger = setup_custom_logger(__name__)

def dispatch(data, settings):
    config = get_config()
    info = get_info(data, config)
    samples, main_audio, offset, song_lg = get_samples(data, info, settings)
    notes_obj, cs = bms(data, info, offset)
    new_cs = cs
    if info.osumode == 3:
        if settings.lock_cs_set:
            notes_obj = lock_cs(notes_obj, cs, int(settings.lock_cs_num))
        if settings.remove_empty_columns:
            notes_obj, new_cs = remove_empty_columns(notes_obj, cs)

    sv = get_sv(data, offset, info, settings) if settings.convert_sv else ''
    osu_content = generate_osu_file(config, info, sv, offset, samples, song_lg, notes_obj, new_cs)

    logger.info(f"New Folder Name: {info.new_folder}")
    logger.info(f"Sub Folder Name: {info.sub_folder}")
    logger.info(f"Osu Filename: {info.osu_filename}")
    logger.info(f"Img Filename: {info.img_filename}")
    print(f"Osu Filename: {info.osu_filename}")
    return osu_content, info, main_audio

def scan_folder(folder_path):
    files = []
    folder_path = os.path.normpath(folder_path)
    for root, _, filenames in os.walk(folder_path):
        root = os.path.normpath(root)
        for filename in filenames:
            file_path = os.path.join(root, filename)
            file_path = os.path.normpath(file_path)
            if os.path.isfile(file_path):
                files.append(file_path)
    return files

