import aiofiles
import asyncio
import datetime
import pathlib
from bin.Dispatch_file import process_file
from bin.utils import setup_custom_logger
from concurrent.futures import ThreadPoolExecutor

logger = setup_custom_logger(__name__)
semaphore = asyncio.Semaphore(5000)  # 限制并发任务数量
executor = ThreadPoolExecutor(max_workers=8)  # 设置线程池

async def process_folder(folder_path, output_folder_path, settings, error_list, cache_folder):
    for bmson_file in folder_path.glob("*.bmson"):
        async with semaphore:
            try:
                await asyncio.get_event_loop().run_in_executor(
                    executor, process_file, bmson_file, output_folder_path, settings, error_list, cache_folder
                )
            except Exception as e:
                error_list.append((bmson_file, str(e)))
                logger.error(f"Error processing file {bmson_file}: {e}")


async def start_conversion(input_folder_path, output_folder_path, settings, cache_folder):
    input_folder_path = pathlib.Path(input_folder_path)
    output_folder_path = pathlib.Path(output_folder_path)
    error_list = []

    tasks = []
    for folder in input_folder_path.iterdir():
        if folder.is_dir():
            tasks.append(process_folder(folder, output_folder_path, settings, error_list, cache_folder))

    await asyncio.gather(*tasks)

    # 汇总出错的文件或文件夹
    if error_list:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_folder = pathlib.Path("log")
        log_folder.mkdir(exist_ok=True)  # 确保 log 文件夹存在
        error_log_file = log_folder / f"error_log_{timestamp}_conversion.txt"

        async with aiofiles.open(error_log_file, 'w', encoding='utf-8') as file:
            await file.write("以下文件或文件夹处理时出错：\n")
            for folder, error in error_list:
                await file.write(f"{folder}: {error}\n")
        logger.error(f"错误日志已保存到 {error_log_file}")
