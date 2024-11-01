# converter_bmson.py

def bms(data, info_obj):
    CS = info_obj.CS
    def cal_notex(CS, x):
        note_x = int(( x - 1 ) * 512 / CS) + int(256/CS)
        return note_x

    MpB = info_obj.MpB
    resolution = int(info_obj.resolution*4)
    def calculate_pulse_time(y):
        return round(y * MpB )
    
    # 初始化变量
    note_x = 8
    hitSound = 0
    SongLg = 0
    notes_obj = []

    normalSet = 0
    additionSet = 0
    ksindex = 0
    volume = 100

    note_time = None
    main_audio = None  
    y_start = 0
    y_end = 0

    zero_x_notes = []
    for channel in data['sound_channels']:
        notes = channel['notes']
        for note in notes:
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

    SongLg = round((y_end - y_start) * MpB)
    offset = round((y_start * MpB / resolution) - 2) * resolution

    valid_notes = []
    for channel in data['sound_channels']:
        notes = channel['notes']
        ksfilename = channel['name'].replace("sound\\", f"{info_obj.sub_folder}/")
        hitSample = f"{normalSet}:{additionSet}:{ksindex}:{volume}:{ksfilename}"
        
        for note in notes:
            x = note['x']
            y = note['y']
            L = note['l']
            #c = note['c']

            if 1 <= x <= 16:
                valid_notes.append((x, y, L, hitSample))
    # 按 y 值排序，重新计算
    valid_notes.sort(key=lambda note: note[1])
    # 重置y值从0开始
    min_y = valid_notes[0][1] if valid_notes else 0
    valid_notes = [(x, y - min_y, L, hitSample) for x, y, L, hitSample in valid_notes]

    for x, y, L, hitSample in valid_notes:
        if x == 8:
            bms_type = "1PnoteS"
            note_x = cal_notex(CS, 1)
        elif 1 <= x <= 7:
            bms_type = "1Pnote"
            x = x + 1
            note_x = cal_notex(CS, x)
        elif 9 <= x <= 15:
            bms_type = "2Pnote"
            note_x = cal_notex(CS, x)
        elif x == 16:
            bms_type = "2PnoteS"
            note_x = cal_notex(CS, x)

        note_time = calculate_pulse_time(y) + offset
        note_type = 128 if L > 0 else 1
        note_end = f"{calculate_pulse_time(y + L) + offset}:" if L > 0 else ''

        notes_obj.append(f"{note_x},192,{note_time},{note_type},{hitSound},{note_end}{hitSample}")

    # # 进行时间检查和修正
    # for i, note in enumerate(notes_obj):
    #     note_parts = note.split(',')
    #     note_time = float(note_parts[2])

    print(f"\n脉冲: Start: {y_start}, End: {y_end}, Song Length: {SongLg}, Offset: {offset}")
    print(f"转换Notes总数: {len(notes_obj)}\n")

    return notes_obj, main_audio, offset, SongLg, CS

