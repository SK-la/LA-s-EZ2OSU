# osu.py

def generate_osu_file(config, info_obj, events, Samples, SongLg, notes_obj, new_CS):
    if info_obj.vdo:
        vdo=f'\nVideo,0,"{info_obj.vdo}"'
    osu_content = f"""osu file format v14

[General]
AudioFilename: {info_obj.song}
AudioLeadIn: 0
PreviewTime: {int(SongLg * 0.4)}
Countdown: 0
SampleSet: Normal
StackLeniency: 0.7
Mode: 3
LetterboxInBreaks: 0
StoryFireInFront: 0
SpecialStyle: 0
WidescreenStoryboard: 0
SamplesMatchPlaybackRate: 1

[Editor]
Bookmarks: 0
DistanceSpacing: 1
BeatDivisor: 4
GridSize: 4
TimelineZoom: 1

[Metadata]
Title:{info_obj.title}
TitleUnicode:{info_obj.title}
Artist:{info_obj.artist}
ArtistUnicode:{info_obj.artist}
Creator:{config.creator}
Version:{info_obj.ver}
Source:{config.source}
Tags:{info_obj.tags}{config.tags}
BeatmapID:0
BeatmapSetID:-1

[Difficulty]
HPDrainRate:{config.HP}
CircleSize:{new_CS}
OverallDifficulty:{config.OD}
ApproachRate:5
SliderMultiplier:1
SliderTickRate:1

[Events]
//Background and Video events
0,0,"{info_obj.img}",0,0{vdo}
//Break Periods
//Storyboard Layer 0 (Background)
//Storyboard Layer 1 (Fail)
//Storyboard Layer 2 (Pass)
//Storyboard Layer 3 (Foreground)
//Storyboard Layer 4 (Overlay)
//Storyboard Sound Samples
"""
    # 将 Samples 列表转换为字符串，每个样本信息占一行
    if Samples:
        print("Samples 有效")  # 调试信息
        samples_str = '\n'.join([str(sample) for sample in Samples])
    else:
        samples_str = ""
        print("Samples 为空")  # 调试信息

    osu_content += samples_str

    osu_content += "\n[TimingPoints]\n"
    if events.Rline:
        print("红线 有效")  # 调试信息
        osu_content += events.Rline
    else:
        print("红线 无效")  # 调试信息

    osu_content += "\n\n[HitObjects]\n"

    # # 将 notes_obj 列表转换为字符串，每个音符信息占一行
    # current_group = ""
    for i, note in enumerate(notes_obj):
        osu_content += note + '\n'
    #     current_group += note + '\n'
    # #     # 每写入100行打印一次
    # #     if (i + 1) % 100 == 0:
    # #         print(f"已写入 {i + 1} 行:\n{current_group}")
    # #         current_group = ""  # 重置 current_group

    # # # 检查是否有剩余的未打印的数据
    # # if current_group:
    # #     print(f"最后一组写入的内容:\n{current_group}")
    
    return osu_content

