def get_sv(data, audio_data, info, y_start):
    bpm = audio_data.bpm
    base_offset = info.offset

    def calculate_pulse_time(y):
        return round(y * info.MpB)

    def calculate_stop_bpms(bpm, duration):
        return (60000 / bpm) * (duration / 100.0)

    sv = []
    bpm_events = data.get('bpm_events', [])
    stop_events = data.get('stop_events', [])

    for event in bpm_events:
        bpm_y = event['y']
        bpm_value = event['bpm']
        sv_offset = calculate_pulse_time(bpm_y - y_start) + base_offset
        sv_bpms = 60000 / bpm_value
        sv.append(f"{sv_offset},{sv_bpms},4,1,1,100,1,0\n")

    for event in stop_events:
        stop_y = event['y']
        stop_duration = event.get('duration', 0)
        sv_offset = calculate_pulse_time(stop_y - y_start) + base_offset
        sv_bpms = calculate_stop_bpms(bpm, stop_duration)
        sv.append(f"{sv_offset},{sv_bpms},4,1,1,100,1,0\n")

    return sv

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

    return lines, base_pulse

def calculate_timing_points(data, current_time, bpm):
    points = {}

    if data.get('bpm_events'):
        time_elapsed = 0.0

        for i, tc in enumerate(data['bpm_events']):
            if i == 0:
                time_elapsed += get_track_duration_given_bpm(bpm, data['MeasureScale']) * (tc['y'] / 100.0)
            stop_time = get_stop_offset(bpm, tc['y'])

            b = tc['bpm']
            if tc.get('IsNegative'):
                b = -tc['bpm']
            points[current_time + stop_time + time_elapsed] = b
            time_elapsed += get_bpm_change_offset(i, data)

    if data.get('stop_events'):
        time_elapsed = 0.0
        for stop_index, stop in enumerate(data['stop_events']):
            if data.get('bpm_events'):
                local_time_elapsed = 0.0
                stop_time = get_stop_offset(bpm, stop['Position'])
                for i, bpm_change in enumerate(data['bpm_events']):
                    if i == 0:
                        local_time_elapsed += get_track_duration_given_bpm(bpm, data['MeasureScale']) * (bpm_change['y'] / 100.0)
                    if (i + 1 < len(data['bpm_events']) and data['bpm_events'][i + 1]['y'] > stop['Position'] and stop['Position'] >= bpm_change['y']):
                        start_at = current_time + local_time_elapsed + stop_time + (get_track_duration_given_bpm(bpm_change['bpm'], data['MeasureScale']) * ((stop['Position'] - bpm_change['y']) / 100.0))
                        end_at = start_at + get_stop_duration(bpm_change['bpm'], stop['Duration'])

                        points[start_at] = 0.0
                        points[end_at] = bpm_change['bpm']
                        break
                    elif i + 1 == len(data['bpm_events']) and stop['Position'] < data['bpm_events'][0]['y']:
                        start_at = current_time + stop_time + (get_track_duration_given_bpm(bpm, data['MeasureScale']) * (stop['Position'] / 100.0))
                        end_at = start_at + get_stop_duration(bpm, stop['Duration'])
                        points[start_at] = 0.0
                        points[end_at] = bpm
                        break
                    local_time_elapsed += get_bpm_change_offset(i, data)
                continue

            if stop_index == 0:
                time_elapsed += get_track_duration_given_bpm(bpm, data['MeasureScale']) * (stop['Position'] / 100.0)

            stop_time = get_stop_offset(bpm, stop['Position'])
            points[current_time + time_elapsed + stop_time] = 0.0
            points[current_time + time_elapsed + stop_time + get_stop_duration(bpm, stop['Duration'])] = bpm
            if stop_index + 1 < len(data['stop_events']):
                time_elapsed += get_track_duration_given_bpm(bpm, data['MeasureScale']) * ((data['stop_events'][stop_index + 1]['Position'] - stop['Position']) / 100.0)
            elif stop_index + 1 == len(data['stop_events']):
                time_elapsed += get_track_duration_given_bpm(bpm, data['MeasureScale']) * ((100.0 - stop['Position']) / 100.0)

    return points

def get_track_duration_given_bpm(bpm, measure_scale):
    return 60000 / (bpm * measure_scale)

def get_stop_offset(bpm, position):
    return (60000 / bpm) * (position / 100.0)

def get_bpm_change_offset(index, data):
    if index + 1 < len(data['bpm_events']):
        current_bpm = data['bpm_events'][index]['bpm']
        next_position = data['bpm_events'][index + 1]['y']
        current_position = data['bpm_events'][index]['y']
        return (60000 / current_bpm) * ((next_position - current_position) / 100.0)
    return 0

def get_stop_duration(bpm, duration):
    return (60000 / bpm) * (duration / 100.0)

def get_offset_start(data, index, message, start_track_with_bpm):
    measure = len(message) / 2
    note_pos = (index / measure) * 100.0

    if not data.get('bpm_events') and not data.get('stop_events'):
        return get_track_duration_given_bpm(start_track_with_bpm, data['MeasureScale']) * (note_pos / 100.0)

    time_to_add = 0.0
    for i, t in enumerate(data['bpm_events']):
        if i == 0:
            if note_pos < t['y']:
                time_to_add += get_track_duration_given_bpm(start_track_with_bpm, data['MeasureScale']) * (note_pos / 100.0)
                break
            else:
                time_to_add += get_track_duration_given_bpm(start_track_with_bpm, data['MeasureScale']) * (t['y'] / 100.0)

        if (i + 1 == len(data['bpm_events']) and note_pos >= t['y']) or (i + 1 < len(data['bpm_events']) and data['bpm_events'][i + 1]['y'] > note_pos and note_pos >= t['y']):
            time_to_add += get_track_duration_given_bpm(t['bpm'], data['MeasureScale']) * ((note_pos - t['y']) / 100.0)
            break
        elif i + 1 < len(data['bpm_events']):
            time_to_add += get_track_duration_given_bpm(t['bpm'], data['MeasureScale']) * ((data['bpm_events'][i + 1]['y'] - t['y']) / 100.0)

    if not data.get('bpm_events'):
        time_to_add += get_track_duration_given_bpm(start_track_with_bpm, data['MeasureScale']) * (note_pos / 100.0)
    if data.get('stop_events'):
        time_to_add += get_stop_offset(start_track_with_bpm, note_pos)
    return time_to_add
