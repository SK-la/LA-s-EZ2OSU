#bin/io_utils.py
import aiofiles
import asyncio
import datetime
import hashlib
import json
import logging
import pathlib
import traceback
from typing import Any, Dict


async def find_duplicate_files(folder_path):
    file_dict = {}
    duplicate_files = []

    for file_path in pathlib.Path(folder_path).rglob('*'):
        if file_path.is_file():
            file_name = file_path.name
            if file_name in file_dict:
                duplicate_files.append((file_dict[file_name], file_path))
            else:
                file_dict[file_name] = file_path

    return duplicate_files

async def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    async with aiofiles.open(file_path, 'rb') as f:
        while chunk := await f.read(8192):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

async def load_hash_cache(cache_folder):
    hash_cache = {}
    if cache_folder.exists():
        async with aiofiles.open(cache_folder / 'hash_cache.json', 'r', encoding='utf-8') as file:
            hash_cache = json.loads(await file.read())
    return hash_cache

async def save_hash_cache(cache_folder, hash_cache):
    cache_folder.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(cache_folder / 'hash_cache.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(hash_cache))



class CustomFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, 'pastime'):
            record.pastime = 'N/A'
        return super().format(record)

def setup_custom_logger(name):
    formatter = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pastime)s')

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)  # 只显示 WARNING 及以上级别的日志

    # 文件处理器
    log_folder = pathlib.Path("log")
    log_folder.mkdir(exist_ok=True)  # 确保 log 文件夹存在
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_handler = logging.FileHandler(log_folder / f"true_log_{timestamp}.txt", encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)  # 记录所有级别的日志

    logger = logging.getLogger(name)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger

def handle_exception(context: Dict[str, Any]) -> None:
    # 获取异常信息
    exception = context.get("exception")
    message = context.get("message", "Unhandled exception")

    # 获取堆栈跟踪信息
    stack_trace = ''.join(traceback.format_exception(None, exception, exception.__traceback__)) if exception else "No stack trace available"

    # 记录异常信息
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    error_log_file = pathlib.Path(f"log/error_log_{timestamp}_exception.txt")
    with open(error_log_file, 'a', encoding='utf-8') as file:
        file.write(f"{timestamp} - {message}\n")
        file.write(f"{timestamp} - {stack_trace}\n")

    # 打印异常信息到控制台
    logging.error(f"{timestamp} - {message}")
    logging.error(f"{timestamp} - {stack_trace}")

# 设置全局异常处理器
loop = asyncio.get_event_loop()
loop.set_exception_handler(lambda loops, context: handle_exception(context))
