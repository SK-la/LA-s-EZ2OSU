# conv_bmson.py

def bms(data, info, audio_data):
    cs = info.CS
    def cal_notex(base_cs, set_x):
        set_x = int((set_x - 1) * 512 / base_cs) + int(256 / base_cs)
        return set_x

    def calculate_pulse_time(note_y):
        return round(note_y * info.MpB)
    
    # 初始化变量
    hit_sound = 0
    normal_set = 0
    addition_set = 0
    ks_index = 0
    volume = 100
    note_x = 8
    notes_obj = []
    valid_notes = []

    for channel in data['sound_channels']:
        notes = channel['notes']
        ks_filename = channel['name'].replace("sound\\", f"{info.sub_folder}/")
        hit_sample = f"{normal_set}:{addition_set}:{ks_index}:{volume}:{ks_filename}"
        
        for note in notes:
            x = note['x']
            y = note['y']
            l = note['l']
            #c = note['c']

            if 1 <= x <= 16:
                valid_notes.append((x, y, l, hit_sample))
    # 按 y 值排序，重新计算
    valid_notes.sort(key=lambda notey: notey[1])
    # 重置y值从0开始
    min_y = valid_notes[0][1] if valid_notes else 0
    valid_notes = [(x, y - min_y, L, hitSample) for x, y, L, hitSample in valid_notes]

    for x, y, l, hit_sample in valid_notes:
        if x == 8:
            bms_type = "1PnoteS"
            note_x = cal_notex(cs, 1)
        elif 1 <= x <= 7:
            bms_type = "1Pnote"
            x = x + 1
            note_x = cal_notex(cs, x)
        elif 9 <= x <= 15:
            bms_type = "2Pnote"
            note_x = cal_notex(cs, x)
        elif x == 16:
            bms_type = "2PnoteS"
            note_x = cal_notex(cs, x)

        note_time = calculate_pulse_time(y) + audio_data.offset
        note_type = 128 if l > 0 else 1
        note_end = f"{calculate_pulse_time(y + l) + audio_data.offset}:" if l > 0 else ''

        notes_obj.append(f"{note_x},192,{note_time},{note_type},{hit_sound},{note_end}{hit_sample}")

    # # 进行时间检查和修正
    # for i, note in enumerate(notes_obj):
    #     note_parts = note.split(',')
    #     note_time = float(note_parts[2])

    print(f"转换Notes总数: {len(notes_obj)}\n")

    return notes_obj, cs

