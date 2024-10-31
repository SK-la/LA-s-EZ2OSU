#events.py

class Events:
    def __init__(self, bpm_events, stop_events, bga_events, layer_events, poor_events, video_events, Rline):
        self.bpm_events = bpm_events
        self.stop_events = stop_events
        self.bga_events = bga_events
        self.layer_events = layer_events
        self.poor_events = poor_events
        self.video_events = video_events
        self.Rline = Rline
    
def get_events(data, info_obj, offset):

    beatLength = round( 1 / info_obj.bpm * 60 * 1000 ,12)

    events = Events(
        bpm_events=data.get('bpm_events', []),
        stop_events=data.get('stop_events', []),
        bga_events=data.get('bga', {}).get('bga_events', []),
        layer_events=data.get('bga', {}).get('layer_events', []),
        poor_events=data.get('bga', {}).get('poor_events', []),
        video_events=[],  # 初始化空列表以存储视频事件
        Rline = f"{offset},{beatLength},4,1,1,100,1,0\n",
    )
    


    
    N = 1
    # 计算 Samples 列表
    Samples = ""
    # for event in events.bpm_events:
    #     tmg = event['y']
    #     bpmx = event['bpm'] * N
    #     Samples.append(())
    
    return events, Samples

def process_lines(data):
    lines = data.get('lines', [])
    base_pulse = None
    y_list = []

    for line in lines:
        y = line['y']
        y_list.append(y)
        if y != 0 and base_pulse is None:
            base_pulse = y
        elif base_pulse is not None and y % base_pulse != 0:
            raise ValueError(f"Value {y} is not a multiple of the base pulse {base_pulse}")

    # 处理 lines 数据
    try:
        Lines, base_pulse = process_lines(data)
        for line in lines:
            print(line)
    except ValueError as e:
        return lines


class TP:
    def __init__(self, time, beatLength, meter=4, sampleSet=0, sampleIndex=0, volume=100, uninherited=1, effects=0):
        self.time = time
        self.beatLength = beatLength 
        self.meter = meter
        self.sampleSet = sampleSet
        self.sampleIndex = sampleIndex
        self.volume = volume
        self.uninherited = uninherited
        self.effects = effects

# def calculate_TP0(info_obj, offset):
#     beatLength = 1 / info_obj.bpm * 60 * 1000
#     return 
    
# def get_TP(info_obj, offset):
#     # 处理 timingPoints 数据
#     beatLength = 1 / info_obj.bpm * 60 * 1000
    
#     tp = TP(
#         time=offset,
#         beatLength=beatLength
#         red=f"{offset},{beatLength},4,0,0,100,1,0\n"
#     )

#     return tp
    




