import pathlib

def get_unique_filename(existing_path):
    base, extension = existing_path.stem, existing_path.suffix
    counter = 1
    while existing_path.exists():
        existing_path = existing_path.with_name(f"{base}_old_{counter}{extension}")
        counter += 1
    return existing_path

# 测试代码
test_path = pathlib.Path("test_file.txt")
# 模拟文件存在
test_path.touch()
print(get_unique_filename(test_path))  # 应该输出 test_file_old_1.txt

# 创建多个文件以测试
for i in range(1, 5):
    new_test_path = pathlib.Path(f"test_file_old_{i}.txt")
    new_test_path.touch()

print(get_unique_filename(test_path))  # 应该输出 test_file_old_5.txt
