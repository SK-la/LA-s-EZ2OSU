#get_info.py
import os
from config import get_config

config = get_config()

class Info:
    def __init__(self, title, artist, bpm, image, resolution, ln_type, lv, ver, diff, song, tags, CS, EZmode, img, vdo):
        self.title = title
        self.artist = artist
        self.bpm = bpm
        self.image = image
        self.resolution = resolution
        self.ln_type = ln_type
        self.lv = lv
        self.ver = ver
        self.diff = diff
        self.song = song
        self.tags = tags
        self.CS = CS
        self.EZmode = EZmode
        self.img = img
        self.vdo = vdo


def get_info(data, config):

    mode_hint = data['info'].get('mode_hint', '').split('-')[-1]
    CS = {'5k': 7, '7k': 8, '9k': 9, '10k': 12, '14k': 16}.get(mode_hint, None)
    if CS is None:
        return 18  # 忽略此文件
    
    mode = {5: '5k',8: '7k1s', 12: '10k2s', 14: '10k2s1p',16: '10k4e2s'}.get(CS, '')
    level_value = data['info'].get('level', 1)
    level = f"LV.{level_value}" if level_value != 1 else ''


    chart_name = data['info'].get('chart_name', '').split('1p')
    EZmode = chart_name[0].strip().upper() if len(chart_name) > 0 else ''
    chart = chart_name[1].strip().upper() if len(chart_name) > 1 else ''
    if not chart:
        chart = 'NM'

    if config.packset in 'Y':
        artist = f"{config.creator}'s PACK"
        title = config.source
    else:
        artist = data['info'].get('artist', '')
        title = data['info'].get('title', '')

    tags = f"{config.creator} {config.source} {mode} {EZmode} {artist} {title}"
    image_ext = os.path.splitext(data['info'].get('eyecatch_image', ''))[1]

    # 处理 bga 数据
    bga_header = data.get('bga', {}).get('bga_header', [])
    bga_name = ''
    if bga_header:
        bga_name = bga_header[0].get('name')

    # 分组信息
    info_obj = Info(
        artist=artist,
        title=title,
        bpm=data['info'].get('init_bpm', 120.0),
        resolution=int(data['info'].get('resolution', 240)),
        ln_type=data['info'].get('ln_type', 1),
        lv=level,
        ver = f"[{EZmode}] {chart}" if not level else f"[{EZmode}] {chart} {level}",
        diff=chart,
        song=f"{artist} - {title}.wav",
        image=data['info'].get('eyecatch_image', ''),
        tags=tags,
        CS=CS,
        EZmode=EZmode,
        img=f"{artist} - {title}{image_ext}" if chart == 'NM' else f"{artist} - {title}_{chart}{image_ext}",
        vdo=bga_name
    )

    return info_obj

class Names:
    def __init__(self, new_folder_name, sub_folder_name, osu_filename, img_filename):
        self.new_folder = new_folder_name
        self.sub_folder = sub_folder_name
        self.osu_filename = osu_filename
        self.img_filename = img_filename

def get_names(info_obj, config):
    sub_folder_name = f"sound_{info_obj.title}"
    new_folder_name = f"{info_obj.song}".replace('.wav','')

    osu_filename = f"{new_folder_name} ({config.creator}) [{info_obj.ver}]"
    if config.packset == 'Y':
        osu_filename += '_pack'

    names_obj = Names(
        new_folder_name=new_folder_name,
        sub_folder_name=sub_folder_name,
        osu_filename=osu_filename,
        img_filename=info_obj.img
    )

    return names_obj


# 假设 info 是全局变量
#info = get_info()

# def load_info_from_file(data):
#     global info
#     info = Info(
#         title=data['title'],
#         artist=data['artist'],
#         bpm=data['bpm'],
#         image=data['image'],
#         resolution=data['resolution'],
#         ln_type=data['ln_type'],
#         lv=data['lv'],
#         ver=data['ver'],
#         diff=data['diff'],
#         song=data['song'],
#         tags=data['tags'],
#         CS=data['CS'],
#         EZmode=data['EZmode'],
#         img=data['img'],
#         offset=data.get('offset', 0)
#     )

# def find_related_tags(query, tags_file):
#     with open(tags_file, 'r', encoding='utf-8') as file:
#         tags_data = json.load(file)
#         related_tags = [tag for tag in tags_data if query in tag]
#         return related_tags