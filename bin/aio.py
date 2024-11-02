import asyncio, aiofiles
import datetime, pathlib
from bin.Dispatch_file import process_file
from bin.custom_log import setup_custom_logger
from bin.io_utils import find_duplicate_files

logger = setup_custom_logger(__name__)
cache_lock = asyncio.Lock()
semaphore = asyncio.Semaphore(4000)  # 限制并发任务数量

async def process_folder(folder_path, output_folder_path, settings, error_list):
    try:
        for bmson_file in folder_path.glob("*.bmson"):
            async with semaphore:
                try:
                    await process_file(bmson_file, output_folder_path, settings, error_list)
                except Exception as e:
                    error_list.append((bmson_file, str(e)))
                    logger.error(f"Error processing file {bmson_file}: {e}")
    except Exception as e:
        error_list.append((folder_path, str(e)))
        logger.error(f"Error processing folder {folder_path}: {e}")

async def start_conversion(input_folder_path, output_folder_path, settings):
    input_folder_path = pathlib.Path(input_folder_path)
    output_folder_path = pathlib.Path(output_folder_path)
    error_list = []

    # 查找重复文件
    duplicates = await find_duplicate_files(input_folder_path)
    if duplicates:
        logger.info("Found duplicate files:")
        for original, duplicate in duplicates:
            logger.info(f"Original: {original}, Duplicate: {duplicate}")

    tasks = []
    for folder in input_folder_path.iterdir():
        if folder.is_dir():
            tasks.append(process_folder(folder, output_folder_path, settings, error_list))

    await asyncio.gather(*tasks)

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