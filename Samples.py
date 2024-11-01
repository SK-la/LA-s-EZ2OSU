#Samples.py

# class Samples:
#     def __init__(self):
#         self.samples = []

def get_samples(data, info, settings):
    def calculate_pulse_time(y):
        return round(y * info.MpB )

    main_audio = None  
    y_start = 0
    y_end = 0
    samples = []
    zero_x_notes = []

    for channel in data['sound_channels']:
        for note in channel['notes']:
            if note['x'] == 0:
                zero_x_notes.append(note)
                if len(zero_x_notes) == 1:
                    main_audio = channel['name']
                    y_start = note['y']
                elif len(zero_x_notes) == 2:
                    y_end = note['y']
                    break
        if len(zero_x_notes) == 2:
            break
    zero_x_notes = zero_x_notes[:2]

    song_lg = round((y_end - y_start) * info.MpB)
    offset = 0
    if settings.convert_sample_bg:
        valid_notes = []
        for channel in data['sound_channels']:
            hs = channel['name'].replace("sound\\", f"{info.sub_folder}/")
            for note in channel['notes']:
                if note['x'] == 0 and note not in zero_x_notes:
                    valid_notes.append((note['y'], hs))

        # 按 y 值排序
        valid_notes.sort(key=lambda notes: notes[0])
        y_min = valid_notes[0][0] if valid_notes else 0
        offset = round((y_min - y_start) * info.MpB)
        #重置 y 值从 0 开始
        valid_notes = [(y - y_min, hs) for y, hs in valid_notes]

        for y, hs in valid_notes:
            note_time = calculate_pulse_time(y) + offset
            samples.append(f"5,{note_time},0,\"{hs}\"")
            
    print(f"\n脉冲: Start: {y_start}, End: {y_end}, Song Length: {song_lg}, Offset: {offset}")
    return samples,  main_audio, offset, song_lg

