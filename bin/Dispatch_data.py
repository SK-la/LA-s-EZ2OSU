#bin/Dispatch_data.py
from bin.Samples import get_samples
from bin.config import get_config
from bin.conv_bmson import bms
from bin.get_info import get_info
from bin.osu import generate_osu_file
from bin.utils import setup_custom_logger
from mod.SV import get_sv
from mod.clm_no_empty import remove_empty_columns
from mod.lock_cs import lock_cs

logger = setup_custom_logger(__name__)

async def dispatch(data, settings):
    config = get_config()
    info = get_info(data, config)
    audio_data, y_start = get_samples(data, info, settings)
    notes_obj, cs = bms(data, info, audio_data)
    new_cs = cs
    if info.osumode == 3:
        if settings.lock_cs_set:
            notes_obj = lock_cs(notes_obj, cs, int(settings.lock_cs_num))
        if settings.remove_empty_columns:
            notes_obj, new_cs = remove_empty_columns(notes_obj, cs)
    sv = get_sv(data, audio_data, info, y_start) if settings.convert_sv else ''

    osu_content = generate_osu_file(config, info, sv, audio_data, notes_obj, new_cs)

    logger.info(f"New Folder Name: {info.new_folder}")
    logger.info(f"Sub Folder Name: {info.sub_folder}")
    logger.info(f"Osu Filename: {info.osu_filename}")
    logger.info(f"Img Filename: {info.img_filename}")
    logger.info(f"Img Filename: {audio_data.main_audio}")
    print(f"Osu Filename: {info.osu_filename}")
    return osu_content, info, audio_data



