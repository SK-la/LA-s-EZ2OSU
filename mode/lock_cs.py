import math


def lock_cs(notes_obj, original_cs, locked_cs):
    # 计算新的 note_x 值
    new_notes_obj = []
    for note in notes_obj:
        parts = note.split(',')
        old_column = int(parts[0])
        new_column = math.ceil(old_column * locked_cs / original_cs)
        parts[0] = str(new_column)
        new_notes_obj.append(','.join(parts))

    return new_notes_obj

