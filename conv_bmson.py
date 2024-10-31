# converter_bmson.py
from mode.clm_no_empty import remove_empty_columns
from mode.lock_cs import lock_cs


def bms(data, info_obj, names_obj, settings):
    CS = info_obj.CS
    def cal_notex(CS, x):
        note_x = int(( x - 1 ) * 512 / CS) + int(256/CS)
        return note_x

    # 计算每拍的毫秒数
    ms_per_beat = 60000 / info_obj.bpm
    resolution = int(info_obj.resolution*4)
    def calculate_pulse_time(y):
        return round(((y - resolution) / info_obj.resolution) * ms_per_beat )
    
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
    in_range_count = 0
    out_of_range_count = 0

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

    SongLg = round((y_end - y_start) * ms_per_beat / info_obj.resolution)
    offset = round(int((y_start * ms_per_beat / resolution / info_obj.resolution) - 2) * resolution)

    for channel in data['sound_channels']:
        notes = channel['notes']
        ksfilename = channel['name'].replace("sound\\", f"{names_obj.sub_folder}/")
        hitSample = f"{normalSet}:{additionSet}:{ksindex}:{volume}:{ksfilename}"
        
        for note in notes:
            x = note['x']
            y = note['y']
            L = note['l']
            #c = note['c']

            if 1 <= x <= 16:
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

            else:
                out_of_range_count += 1

    # 对 notes_obj 进行排序
    notes_obj.sort(key=lambda x: float(x.split(',')[2]))

    # 进行时间检查和修正
    for i, note in enumerate(notes_obj):
        note_parts = note.split(',')
        note_time = float(note_parts[2])

        # 检查音符时间是否在合理范围内
        if note_time < 0 or note_time > (SongLg + offset):
            print(f"警告: 音符时间超出范围: {note_time} ms")
            continue
    #print("bms 函数返回的 notes_obj 内容:", notes_obj)
    #print("bms修正时间后返回的 notes_obj 类型:", type(notes_obj))
    new_CS = None
    if settings.remove_empty_columns:
        notes_obj, new_CS = remove_empty_columns(notes_obj, CS)

    #print("bms 函数返回的 notes_obj 内容:", notes_obj)
    #print("c e c 返回的 notes_obj 类型:", type(notes_obj))

    # 锁定CS数
    if settings.lock_cs_set:
        notes_obj = lock_cs(notes_obj, CS, int(settings.cs_number))

    # 调试信息
    print(f"\n音频概况:\n主音频: {main_audio}, Start: {y_start}, End: {y_end}, Song Length: {SongLg}, Offset: {offset}")
    print(f"转换Notes总数: {len(notes_obj)}, 处理{in_range_count}, 忽略{out_of_range_count}\n")

    return notes_obj, main_audio, offset, SongLg, new_CS





    # # 输出拆分的结果
    # for note in notes_obj:
    #     try:
    #         note_time = note.split(',')[2]
    #         #print(f"拆分结果: {note_time}")
    #     except ValueError:
    #         logging.error(f"无效的 note_time: {note}")

    # # 输出排序的结果并写入缓存文件
    # try:
    #     with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
    #         notes_obj.sort(key=lambda x: int(x.split(',')[2]))
    #         for note in notes_obj:
    #             temp_file.write(note + '\n')
    #         temp_file_path = temp_file.name
    # except ValueError as e:
    #     logging.error(f"整理音符数据出错: {e}")
    #     for note in notes_obj:
    #         try:
    #             note_time = note.split(',')[2]
    #         except ValueError:
    #             logging.error(f"note时间无效: {note}")

    # # 假设 notes_obj 已经排序完毕
    # if notes_obj:
    #     # 检查第一行
    #     first_note = notes_obj[0].split(',')
    #     if first_note[3] == '1':
    #         first_note[3] = '5'
    #     notes_obj[0] = ','.join(first_note)

    #     # 检查最后一行
    #     last_note = notes_obj[-1].split(',')
    #     if last_note[3] == '1':
    #         last_note[3] = '5'
    #     notes_obj[-1] = ','.join(last_note)


# class Obj:
#     Samples = []  # 假设 Samples 是从某个函数获取的样本列表
#     Points = []  # 假设 Points 是从某个函数获取的 timing points 列表

#     obj = Obj()

#     return