import os, re

def sanitize_name(name):
    # 移除不允许的特殊字符
    return re.sub(r'[<>:"/\\|?*]', '_', name)

class Info:
    def __init__(self, title, artist, osumode, bpm, bpms, image, resolution, m_p_b, lv, ver, diff, song, tags, cs, ez_mode, img, vdo, new_folder, sub_folder, osu_filename, img_filename):
        self.title = title
        self.artist = artist
        self.bpm = bpm
        self.bpms = bpms
        self.image = image
        self.resolution = resolution
        self.MpB = m_p_b
        self.lv = lv
        self.ver = ver
        self.diff = diff
        self.song = song
        self.tags = tags
        self.CS = cs
        self.ez_mode = ez_mode
        self.img = img
        self.vdo = vdo
        self.new_folder = new_folder
        self.sub_folder = sub_folder
        self.osu_filename = osu_filename
        self.img_filename = img_filename
        self.osumode = osumode

def get_info(data, config):
    mode_hint = data['info'].get('mode_hint', '').split('-')[-1]
    cs = {'5k': 7, '7k': 8, '9k': 9, '10k': 12, '14k': 16}.get(mode_hint, 18)

    mode = {5: '5k', 8: '7k1s', 12: '10k2s', 16: '10k4e2s'}.get(cs, '')
    level_value = data['info'].get('level', 1)
    level = f"LV.{level_value}" if level_value != 1 else ''

    chart_name = data['info'].get('chart_name', '').split('1p')
    ez_mode = chart_name[0].strip().upper() if chart_name else ''
    osumode = 2 if ez_mode == 'catch' else 3
        
    chart = chart_name[1].strip().upper() if len(chart_name) > 1 and chart_name[1].strip() else 'NM'

    eyecatch_image = data['info'].get('eyecatch_image', '')
    image_ext = os.path.splitext(eyecatch_image)[1]

    # 查找拓展名前5个字符内的最后一个 '_'
    split_index = eyecatch_image.rfind('_', -5 - len(image_ext), -len(image_ext))
    if split_index != -1:
        image_diff = f"_{eyecatch_image[split_index + 1:-len(image_ext)].upper()}{image_ext}"
    else:
        image_diff = image_ext

    artist = f"{config.creator}'s PACK" if config.packset == 'Y' else sanitize_name(data['info'].get('artist', ''))
    title = config.source if config.packset == 'Y' else sanitize_name(data['info'].get('title', ''))

    tags = f"{config.creator} {config.source} {mode} {ez_mode} {artist} {title}"


    bga_name = data.get('bga', {}).get('bga_header', [{}])[0].get('name', '')

    new_folder_name = f"{artist} - {title}".replace('.wav', '')
    sub_folder_name = f"sound" #改
    ver = f"[{ez_mode}] {chart} {level}" if level else f"[{ez_mode}] {chart}"
    osu_filename = f"{artist} - {title} ({config.creator}) [{ver}]"
    if config.packset == 'Y':
        osu_filename += '_pack'
    img_filename = f"{artist} - {title}{image_diff}"

    bpm=data['info'].get('init_bpm', 120.0)
    resolution=int(data['info'].get('resolution', 240))


    info = Info(
        artist=artist,
        title=title,
        osumode=osumode,
        bpm=bpm,
        bpms=round(60000 / bpm, 12),
        resolution=resolution,
        m_p_b=60000 / (bpm * resolution),
        lv=level,
        ver=ver,
        diff=chart,
        song=f"{artist} - {title}.wav",
        image=data['info'].get('eyecatch_image', ''),
        tags=tags,
        cs=cs,
        ez_mode=ez_mode,
        img=img_filename,
        vdo=bga_name,
        new_folder=new_folder_name,
        sub_folder=sub_folder_name,
        osu_filename=osu_filename,
        img_filename=img_filename
    )

    return info
