# test_script.py

def cal_notex(CS, x):
    note_x = int((x - 1) * 512 / CS) + int(256 / CS)
    return note_x

def remove_empty_columns(notes_obj, CS, valid_CS_values):
    # 找出所有有音符的列
    columns_with_notes = set()
    for note in notes_obj:
        note_x = int(note.split(',')[0])
        # 将映射坐标转换回原始列号
        original_column = (note_x - int(256 / CS)) * CS // 512 + 1
        columns_with_notes.add(original_column)

    # 创建一个映射，将旧列号映射到新列号
    column_mapping = {}
    new_column = 1
    for old_column in range(1, CS + 1):
        if old_column in columns_with_notes:
            column_mapping[old_column] = new_column
            new_column += 1

    # 更新 notes_obj 中的列号
    new_notes_obj = []
    for note in notes_obj:
        parts = note.split(',')
        note_x = int(parts[0])
        # 将映射坐标转换回原始列号
        old_column = (note_x - int(256 / CS)) * CS // 512 + 1
        if old_column in column_mapping:
            # 重新计算映射坐标
            new_note_x = cal_notex(CS, column_mapping[old_column])
            parts[0] = str(new_note_x)
            new_notes_obj.append(','.join(parts))

    # 计算非空列数
    non_empty_columns = len(columns_with_notes)

    # 找到最近的合理值
    new_CS = min([value for value in valid_CS_values if value >= non_empty_columns], default=max(valid_CS_values))

    # 如果新的 CS 大于非空列数，添加空列
    if new_CS > non_empty_columns:
        for i in range(non_empty_columns + 1, new_CS + 1):
            new_note_x = cal_notex(CS, i)
            new_notes_obj.append(f"{new_note_x},0")

    return new_notes_obj, new_CS

# 测试函数
def test_remove_empty_columns():
    notes_obj = [
        "48,192,1680,1,0,0:0:0:0:",
        "112,192,1680,1,0,0:0:0:0:",
        "144,192,1680,1,0,0:0:0:0:",
        "176,192,1680,1,0,0:0:0:0:",
        "208,192,1680,1,0,0:0:0:0:",
        "240,192,1680,1,0,0:0:0:0:",
        "272,192,1680,1,0,0:0:0:0:",
        "304,192,1680,1,0,0:0:0:0:",
        "336,192,1680,1,0,0:0:0:0:",
        "368,192,1680,1,0,0:0:0:0:",
        "400,192,1680,1,0,0:0:0:0:",
        "432,192,1680,1,0,0:0:0:0:",
        "464,192,1680,1,0,0:0:0:0:",
        "496,192,1680,1,0,0:0:0:0:"
    ]
    CS = 16
    valid_CS_values = [4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18]

    # 去除空列并获取新的CS值
    notes_obj, new_CS = remove_empty_columns(notes_obj, CS, valid_CS_values)
    
    print("Updated notes_obj:")
    for note in notes_obj:
        print(note)
    
    print("\nNew CS value:", new_CS)

if __name__ == "__main__":
    test_remove_empty_columns()
