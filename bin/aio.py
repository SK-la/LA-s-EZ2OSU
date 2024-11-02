#bin/aio.py
import asyncio
import pathlib
import json
import os
import aiofiles
import shutil
import datetime
from bin.Dispatch_file import process_file
from bin.custom_log import setup_custom_logger

logger = setup_custom_logger(__name__)
cache_lock = asyncio.Lock()
semaphore = asyncio.Semaphore(10)  # 限制并发任务数量

async def load_cache(cache_file_path):
    if os.path.exists(cache_file_path):
        async with aiofiles.open(cache_file_path, 'r', encoding='utf-8') as file:
            return json.loads(await file.read())
    return {}

async def save_cache(cache_file_path, cache_data):
    async with aiofiles.open(cache_file_path, 'w', encoding='utf-8') as file:
        await file.write(json.dumps(cache_data))

async def copy_file_with_cache(file_path, destination_path, cache):
    async with cache_lock:
        if str(file_path) in cache:
            return  # 跳过已处理的文件
        cache[str(file_path)] = True  # 更新缓存
    shutil.copy(file_path, destination_path)

async def process_sound_folder(sound_folder, output_folder, cache):
    for sound_file in sound_folder.glob("*.*"):
        destination_path = output_folder / sound_file.name
        await copy_file_with_cache(sound_file, destination_path, cache)

async def process_folder(folder_path, output_folder_path, settings, cache, error_list):
    try:
        sound_folder = folder_path / "sound"
        if sound_folder.exists():
            await process_sound_folder(sound_folder, output_folder_path, cache)

        for bmson_file in folder_path.glob("*.bmson"):
            async with semaphore:
                await process_file(bmson_file, output_folder_path, settings, cache, error_list)
    except Exception as e:
        error_list.append((folder_path, str(e)))

async def start_conversion(input_folder_path, output_folder_path, settings, cache_file_path):
    input_folder_path = pathlib.Path(input_folder_path)
    output_folder_path = pathlib.Path(output_folder_path)
    cache = await load_cache(cache_file_path)
    error_list = []

    tasks = []
    for folder in input_folder_path.iterdir():
        if folder.is_dir():
            tasks.append(process_folder(folder, output_folder_path, settings, cache, error_list))

    await asyncio.gather(*tasks)
    await save_cache(cache_file_path, cache)

    # 汇总出错的文件或文件夹
    if error_list:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_folder = pathlib.Path("log")
        log_folder.mkdir(exist_ok=True)  # 确保 log 文件夹存在
        error_log_file = log_folder / f"error_log_{timestamp}.txt"

        async with aiofiles.open(error_log_file, 'w', encoding='utf-8') as file:
            await file.write("以下文件或文件夹处理时出错：\n")
            for folder, error in error_list:
                await file.write(f"{folder}: {error}\n")
        logger.error(f"错误日志已保存到 {error_log_file}")

