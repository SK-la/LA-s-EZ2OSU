import os
from config import get_config

config = get_config()

class Info:
    def __init__(self, title, artist, bpm, bpms, image, resolution, MpB, lv, ver, diff, song, tags, CS, EZmode, img, vdo, new_folder, sub_folder, osu_filename, img_filename):
        self.title = title
        self.artist = artist
        self.bpm = bpm
        self.bpms = bpms
        self.image = image
        self.resolution = resolution
        self.MpB = MpB
        self.lv = lv
        self.ver = ver
        self.diff = diff
        self.song = song
        self.tags = tags
        self.CS = CS
        self.EZmode = EZmode
        self.img = img
        self.vdo = vdo
        self.new_folder = new_folder
        self.sub_folder = sub_folder
        self.osu_filename = osu_filename
        self.img_filename = img_filename

def get_info(data, config):
    mode_hint = data['info'].get('mode_hint', '').split('-')[-1]
    CS = {'5k': 7, '7k': 8, '9k': 9, '10k': 12, '14k': 16}.get(mode_hint, 18)
    if CS == 18:
        return None  # 忽略此文件

    mode = {5: '5k', 8: '7k1s', 12: '10k2s', 16: '10k4e2s'}.get(CS, '')
    level_value = data['info'].get('level', 1)
    level = f"LV.{level_value}" if level_value != 1 else ''

    chart_name = data['info'].get('chart_name', '').split('1p')
    EZmode = chart_name[0].strip().upper() if chart_name else ''
    chart = chart_name[1].strip().upper() if len(chart_name) > 1 else 'NM'

    artist = f"{config.creator}'s PACK" if config.packset == 'Y' else data['info'].get('artist', '')
    title = config.source if config.packset == 'Y' else data['info'].get('title', '')

    tags = f"{config.creator} {config.source} {mode} {EZmode} {artist} {title}"
    image_ext = os.path.splitext(data['info'].get('eyecatch_image', ''))[1]

    bga_name = data.get('bga', {}).get('bga_header', [{}])[0].get('name', '')

    new_folder_name = f"{artist} - {title}".replace('.wav', '')
    sub_folder_name = f"sound_{title}"
    ver = f"[{EZmode}] {chart} {level}" if level else f"[{EZmode}] {chart}"
    osu_filename = f"{new_folder_name} ({config.creator}) [{ver}]"
    if config.packset == 'Y':
        osu_filename += '_pack'
    img_filename = f"{artist} - {title}{image_ext}" if chart == 'NM' else f"{artist} - {title}_{chart}{image_ext}"

    bpm=data['info'].get('init_bpm', 120.0)
    resolution=int(data['info'].get('resolution', 240))


    info = Info(
        artist=artist,
        title=title,
        bpm=bpm,
        bpms=round(60000 / bpm, 12),
        resolution=resolution,
        MpB=60000 / (bpm * resolution),
        lv=level,
        ver=ver,
        diff=chart,
        song=f"{artist} - {title}.wav",
        image=data['info'].get('eyecatch_image', ''),
        tags=tags,
        CS=CS,
        EZmode=EZmode,
        img=f"{artist} - {title}{image_ext}" if chart == 'NM' else f"{artist} - {title}_{chart}{image_ext}",
        vdo=bga_name,
        new_folder=new_folder_name,
        sub_folder=sub_folder_name,
        osu_filename=osu_filename,
        img_filename=img_filename
    )

    return info
