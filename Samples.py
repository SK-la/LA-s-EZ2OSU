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
    Samples = []
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

    SongLg = round((y_end - y_start) * info.MpB)
    offset = round((y_start * info.MpB / (info.resolution * 4)) - 2) * (info.resolution * 4)
    if settings.convert_sample_bg:
        valid_notes = []
        for channel in data['sound_channels']:
            hs = channel['name'].replace("sound\\", f"{info.sub_folder}/")
            for note in channel['notes']:
                if note['x'] == 0 and note not in zero_x_notes:
                    valid_notes.append((note['y'], hs))

        # 按 y 值排序并重置 y 值从 0 开始
        valid_notes.sort(key=lambda note: note[0])
        min_y = valid_notes[0][0] if valid_notes else 0
        valid_notes = [(y - min_y, hs) for y, hs in valid_notes]

        for y, hs in valid_notes:
            note_time = calculate_pulse_time(y) + offset
            Samples.append(f"5,{note_time},0,\"{hs}\"")
            
    print(f"\n脉冲: Start: {y_start}, End: {y_end}, Song Length: {SongLg}, Offset: {offset}")
    return Samples,  main_audio, offset, SongLg



# # test
# import json
# from pathlib import Path

# # 从指定的文件路径加载测试数据
# file_path = Path(r"E:\BASE CODE\GitHub\LAs-EZ2OSU\bk\test\testdata.bmson")
# if not file_path.exists():
#     raise FileNotFoundError(f"文件 {file_path} 不存在，请检查路径和文件名是否正确。")

# with file_path.open('r', encoding='utf-8') as file:
#     data = json.load(file)

# # 定义一个简单的类来模拟 info 对象
# class Info:
#     def __init__(self, MpB, resolution, sub_folder):
#         self.MpB = MpB
#         self.resolution = resolution
#         self.sub_folder = sub_folder

# # 创建 info 对象
# info = Info(
#     MpB=8,  # 示例值，请替换为实际数据
#     resolution=48,  # 示例值，请替换为实际数据
#     sub_folder="subfolder_name"  # 示例值，请替换为实际数据
# )

# # 调用原始脚本中的 get_samples 函数
# from Samples import get_samples

# # 使用测试数据运行函数
# samples, main_audio, offset, song_lg = get_samples(data, info)

# # 打印结果

# print("Main Audio:", main_audio)
# print("Offset:", offset)
# print("Song Length:", song_lg)
# #print("Samples:", samples)