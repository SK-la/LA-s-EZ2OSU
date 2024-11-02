#Samples.py
from bin.utils import setup_custom_logger

logger = setup_custom_logger(__name__)

class AudioData:
    def __init__(self, samples, main_audio, offset, song_lg):
        self.samples = samples
        self.main_audio = main_audio
        self.offset = offset
        self.song_lg = song_lg

def get_samples(data, info, settings):
    y_start, y_end, y_min, all_notes = get_y_values(data)
    main_audio = get_main_audio(data, y_start)

    song_lg = round((y_end - y_start) * info.MpB)
    offset = round((y_min - y_start) * info.MpB)

    samples = []
    if hasattr(settings, 'convert_sample_bg') and settings.convert_sample_bg:
        invalid_notes = [note for note in all_notes if not (1 <= note['x'] <= 16)]
        invalid_notes.sort(key=lambda note: note['y'])
        reset_invalid_notes = [
            {'x': note['x'], 'y': note['y'] - invalid_notes[0]['y'], 'name': note.get('name', 'unknown')} for note in
            invalid_notes]

        for note in reset_invalid_notes:
            hs = note['name'].replace("sound\\", f"{info.sub_folder}/")
            note_time = calculate_pulse_time(note['y'], info) + offset
            samples.append(f"5,{note_time},0,\"{hs}\"")

    audioData = AudioData(
        samples=samples,
        main_audio=main_audio,
        offset=offset,
        song_lg=song_lg,
    )


    print(f"脉冲: Start: {y_start}, End: {y_end}, Song Length: {song_lg}, Offset: {offset}")
    logger.info(f"脉冲: Start: {y_start}, End: {y_end}, Song Length: {song_lg}, Offset: {offset}")
    return audioData



def calculate_pulse_time(y, info):
    return round(y * info.MpB)

def get_y_values(data):
    all_notes = []
    valid_notes = []

    for channel in data['sound_channels']:
        for note in channel['notes']:
            if 'x' in note and 'y' in note:
                all_notes.append(note)
                if 1 <= note['x'] <= 16:
                    valid_notes.append(note)

    all_notes.sort(key=lambda note: note['y'])
    valid_notes.sort(key=lambda note: note['y'])

    y_start = all_notes[0]['y'] if all_notes else 0
    y_end = all_notes[-1]['y'] if all_notes else 0
    y_min = valid_notes[0]['y'] if valid_notes else y_start

    return y_start, y_end, y_min, all_notes


def get_main_audio(data, y_start):
    for channel in data['sound_channels']:
        for note in channel['notes']:
            if 'y' in note and note['y'] == y_start:
                return channel.get('name', 'unknown')
    return 'unknown'