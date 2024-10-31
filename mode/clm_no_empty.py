#clm_no_empty.py
from config import get_config

config = get_config()

def cal_notex(CS, x):
    note_x = int((x - 1) * 512 / CS) + int(256 / CS)
    return note_x

def remove_empty_columns(notes_obj, CS):
    valid_CS_values = [12, 14, 16, 18]
    columns_with_notes = set()

    for note in notes_obj:
        note_x = int(note.split(',')[0])
        original_column = (note_x - int(256 / CS)) * CS // 512
        columns_with_notes.add(original_column)

    # 如果 noS 为假，将 1PnoteS 和 2PnoteS 列音符当作非空轨
    if not config.noS:
        columns_with_notes.add(0)  # 1PnoteS 列
        columns_with_notes.add(CS - 1)  # 2PnoteS 列

    column_mapping = {}
    new_column = 0
    for old_column in range(CS):
        if old_column in columns_with_notes:
            column_mapping[old_column] = new_column
            new_column += 1

    non_empty_columns = len(columns_with_notes)

    if non_empty_columns > 10:
        new_CS = min([value for value in valid_CS_values if value >= non_empty_columns], default=max(valid_CS_values))
    else:
        new_CS = non_empty_columns

    # 确保 new_CS 始终有一个有效的值
    if new_CS is None or new_CS <= 0:
        new_CS = CS

    new_notes_obj = []
    for note in notes_obj:
        parts = note.split(',')
        note_x = int(parts[0])
        old_column = (note_x - int(256 / CS)) * CS // 512
        if old_column in column_mapping:
            new_note_x = cal_notex(new_CS, column_mapping[old_column] + 1)
            parts[0] = str(new_note_x)
            new_notes_obj.append(','.join(parts))

    print("去空列-前后列号映射:", column_mapping)

    return new_notes_obj, new_CS