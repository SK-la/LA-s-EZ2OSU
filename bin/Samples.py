#Samples.py
from bin.custom_log import setup_custom_logger

logger = setup_custom_logger(__name__)

def get_samples(data, info, settings):
    def calculate_pulse_time(y):
        return round(y * info.MpB )

    main_audio = None
    samples = []
    all_notes = []

    for channel in data['sound_channels']:
        for note in channel['notes']:
            all_notes.append(note)
            if note['x'] == 0 and main_audio is None:
                main_audio = channel['name']

    # 按 y 值排序
    all_notes.sort(key=lambda note: note['y'])

    y_start = all_notes[0]['y'] if all_notes else 0
    y_end = all_notes[-1]['y'] if all_notes else 0

    song_lg = round((y_end - y_start) * info.MpB)

    valid_notes = []
    for channel in data['sound_channels']:
        hs = channel['name'].replace("sound\\", f"{info.sub_folder}/")
        for note in channel['notes']:
            if 1 <= note['x'] <= 16:
                valid_notes.append((note['y'], hs))

    # 按 y 值排序
    valid_notes.sort(key=lambda notes: notes[0])
    y_min = valid_notes[0][0] if valid_notes else y_start
    offset = round((y_min - y_start) * info.MpB)

    if settings.convert_sample_bg:
        # 重置 y 值从 0 开始
        valid_notes = [(y - y_min, hs) for y, hs in valid_notes]

        for y, hs in valid_notes:
            note_time = calculate_pulse_time(y) + offset
            samples.append(f"5,{note_time},0,\"{hs}\"")

    print(f"脉冲: Start: {y_start}, End: {y_end}, Song Length: {song_lg}, Offset: {offset}")
    logger.info(f"脉冲: Start: {y_start}, End: {y_end}, Song Length: {song_lg}, Offset: {offset}")
    return samples,  main_audio, offset, song_lg

