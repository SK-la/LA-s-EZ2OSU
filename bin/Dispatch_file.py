#bin/Dispatch_file.py
import shutil
import json
import pathlib
import urllib.parse
import asyncio
import aiofiles
from bin.Dispatch_data import dispatch, scan_folder
from bin.custom_log import setup_custom_logger

logger = setup_custom_logger(__name__)
cache_lock = asyncio.Lock()
semaphore = asyncio.Semaphore(100)  # 限制并发任务数量

def encode_filename(filename):
    return urllib.parse.quote(filename, safe='')

def decode_filename(encoded_filename):
    return urllib.parse.unquote(encoded_filename)

def get_unique_filename(existing_path):
    base, extension = existing_path.stem, existing_path.suffix
    counter = 1
    while existing_path.exists():
        existing_path = existing_path.with_name(f"{base}_old_{counter}{extension}")
        counter += 1
    return existing_path

async def copy_file_with_cache(file_path, destination_path, cache):
    async with cache_lock:
        if str(file_path) in cache:
            return  # 跳过已处理的文件
        cache[str(file_path)] = True  # 更新缓存
    shutil.copy(file_path, destination_path)

async def process_file(bmson_file, output_folder, settings, cache, error_list):
    try:
        output_folder = pathlib.Path(output_folder)
        async with aiofiles.open(bmson_file, 'r', encoding='utf-8') as file:
            data = json.loads(await file.read())

        osu_content, info, main_audio = dispatch(data, settings)

        # 使用原始名称创建文件夹
        song_folder = output_folder / info.new_folder
        song_folder.mkdir(parents=True, exist_ok=True)
        sub_folder = song_folder / info.sub_folder
        sub_folder.mkdir(parents=True, exist_ok=True)
        output_folder = song_folder

        files = scan_folder(bmson_file.parent)
        for file_path in files:
            file_path = pathlib.Path(file_path)
            if settings.include_audio and file_path.suffix in {'.mp3', '.wav', '.ogg', '.wmv', '.mp4', '.avi'}:
                destination_path = output_folder / file_path.name
                if not destination_path.exists():
                    await copy_file_with_cache(file_path, destination_path, cache)
            elif settings.include_images and file_path.suffix in {'.jpg', '.png'} and file_path.stem == pathlib.Path(info.image).stem:
                destination_path = output_folder / file_path.name
                shutil.copy(file_path, destination_path)
            elif file_path.suffix in {'.wmv', '.mp4', '.avi'} and file_path.stem == pathlib.Path(info.vdo).stem:
                destination_path = output_folder / file_path.name
                shutil.copy(file_path, destination_path)
            else:
                sub_folder_path = output_folder / info.sub_folder
                if not sub_folder_path.exists():
                    sub_folder_path.mkdir(parents=True, exist_ok=True)
                destination_path = sub_folder_path / file_path.name
                shutil.copy(file_path, destination_path)

        osu_file_path = output_folder / f"{info.osu_filename}.osu"
        async with aiofiles.open(osu_file_path, 'w', encoding='utf-8') as file:
            await file.write(osu_content)
        return info

    except Exception as e:
        error_list.append((bmson_file, str(e)))
        return None

# def get_unique_filename(existing_path):
#     base, extension = existing_path.stem, existing_path.suffix
#     counter = 1
#     while existing_path.exists():
#         existing_path = existing_path.with_name(f"{base}_old_{counter}{extension}")
#         counter += 1
#     return existing_path