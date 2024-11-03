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

    main_audio = ''
    for note in all_notes:
        if note['y'] == y_start and not (1 <= note['x'] <= 16):
            main_audio = note['name']
            break

    song_lg = round((y_end - y_start) * info.MpB)
    offset = round((y_min - y_start) * info.MpB)

    samples = []
    if settings.convert_sample_bg:
        reset_notes = [{'x': note['x'], 'y': note['y'] - all_notes[0]['y'], 'name': note.get('name', '')} for note in all_notes]
        invalid_notes = [note for note in reset_notes if not (1 <= note['x'] <= 16)]
        for note in invalid_notes:
            hs = note['name'].replace("sound\\", f"{info.sub_folder}/")
            if note['name'] != main_audio:
                note_time = calculate_pulse_time(note['y'], info)
                samples.append(f"5,{note_time},0,\"{hs}\"")

    audio_data = AudioData(
        samples=samples,
        main_audio=main_audio,
        offset=offset,
        song_lg=song_lg,
    )

    print(f"main_audio: {audio_data.main_audio}, pulses: Start {y_start}, End {y_end}, Total duration {song_lg} ms, Offset {offset} ms")
    logger.info(f"main_audio: {audio_data.main_audio}, pulses: Start {y_start}, End {y_end}, Total duration {song_lg} ms, Offset {offset} ms")
    return audio_data


def calculate_pulse_time(y, info):
    return round(y * info.MpB)

def get_y_values(data):
    all_notes = []
    valid_notes = []

    for channel in data['sound_channels']:
        channel_name = channel.get('name', '')
        for note in channel['notes']:
            note['name'] = channel_name  # 将 channel 的 name 属性添加到 note 中
            all_notes.append(note)
            if 1 <= note['x'] <= 16:
                valid_notes.append(note)
            logger.debug(f"Processed note: {note}")

    all_notes.sort(key=lambda notes: notes['y'])
    valid_notes.sort(key=lambda notes: notes['y'])

    y_start = all_notes[0]['y'] if all_notes else 0
    y_end = all_notes[-1]['y'] if all_notes else 0
    y_min = valid_notes[0]['y'] if valid_notes else y_start

    return y_start, y_end, y_min, all_notes
