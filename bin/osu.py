# osu.py

def generate_osu_file(config, info, sv, offset, samples, song_lg, notes_obj, new_cs):
    vdo= '' if info.vdo == '' else f'\nVideo,0,"{info.vdo}"'

    osu_content = f"""osu file format v14

[General]
AudioFilename: {info.song}
AudioLeadIn: 0
PreviewTime: {int(song_lg * 0.4)}
Countdown: 0
SampleSet: Normal
StackLeniency: 0.7
Mode: {info.osumode}
LetterboxInBreaks: 0
StoryFireInFront: 0
SpecialStyle: 0
WidescreenStoryboard: 0

[Editor]
Bookmarks: 0
DistanceSpacing: 1
BeatDivisor: 4
GridSize: 4
TimelineZoom: 1

[Metadata]
Title:{info.title}
TitleUnicode:{info.title}
Artist:{info.artist}
ArtistUnicode:{info.artist}
Creator:{config.creator}
Version:{info.ver}
Source:{config.source}
Tags:{info.tags}{config.tags}
BeatmapID:0
BeatmapSetID:-1

[Difficulty]
HPDrainRate:{config.HP}
CircleSize:{new_cs}
OverallDifficulty:{config.OD}
ApproachRate:5
SliderMultiplier:1
SliderTickRate:1

[Events]
//Background and Video events
0,0,"{info.img}",0,0{vdo}
//Break Periods
//Storyboard Layer 0 (Background)
//Storyboard Layer 1 (Fail)
//Storyboard Layer 2 (Pass)
//Storyboard Layer 3 (Foreground)
//Storyboard Layer 4 (Overlay)
//Storyboard Sound Samples
"""
    # 将 Samples 列表转换为字符串，每个样本信息占一行
    samples_str = '\n'.join([str(sample) for sample in samples]) if samples else ""

    osu_content += samples_str

    osu_content += "\n[TimingPoints]\n"
    osu_content += f"{offset},{info.bpms},4,1,1,100,1,0\n"
    osu_content += sv if sv else ""

    osu_content += "\n\n[HitObjects]\n"

    for i, note in enumerate(notes_obj):
        osu_content += note + '\n'

    
    return osu_content

