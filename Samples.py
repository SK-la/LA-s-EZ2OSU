#Samples.pyg

class Samples:
    def __init__(self):
        self.samples = []

def get_samples(data, info, offset):
    samples = []
    pls = 60000 / (info.resolution * info.bpm)
    resolution = int(info.resolution*4)
    def calculate_pulse_time(y):
        return round((y - resolution) * pls)

    for channel in data['sound_channels']:
        ksfilename = channel['name'].replace("sound\\", f"{info.sub_folder}/")
        for note in channel['notes']:
            if note['x'] >= 16:
                note_time = calculate_pulse_time(note['y']) + offset
                samples.append(f"5,{note_time},0,\"{ksfilename}\"")

    return samples