import asyncio
import json
import re
from pathlib import Path

import aiofiles

from bin.Dispatch_data import dispatch
from bin.utils import setup_custom_logger

logger = setup_custom_logger(__name__)
BATCH_SIZE = 2000
semaphore = asyncio.Semaphore(5000)

async def process_file(bmson_file, output_folder, settings, error_list):
    try:
        bmson_file = Path(bmson_file)

        async with aiofiles.open(bmson_file, 'r', encoding='utf-8') as file:
            content = await file.read()
            data = json.loads(content)  # 尝试解析 JSON
            data['input_file_path'] = str(bmson_file)

        osu_content, info, audio_data = await dispatch(data, settings)
        logger.info(f"Main audio: {audio_data.main_audio}")

        # 检查文件夹名称是否带后缀
        parent_name_suffix = extract_parent_name_suffix(bmson_file.parent.name)
        if parent_name_suffix:
            # 如果存在后缀，则将其添加到 info.new_folder 后面
            info.new_folder += parent_name_suffix

        song_folder = Path(output_folder / info.new_folder )
        song_folder.mkdir(parents=True, exist_ok=True)
        sub_folder = Path(song_folder / info.sub_folder)
        sub_folder.mkdir(parents=True, exist_ok=True)

        osu_file_path = Path(song_folder / f"{info.osu_filename}.osu")

        async with aiofiles.open(osu_file_path, 'w', encoding='utf-8') as file:
            await file.write(osu_content)

        # 获取目标文件夹中的所有文件名
        existing_file_names_song = await get_existing_file_names(song_folder)
        existing_file_names_sub = await get_existing_file_names(sub_folder)

        files = await scan_folder(bmson_file.parent)
        await process_batches(files, existing_file_names_song, existing_file_names_sub, settings, song_folder, sub_folder, info, audio_data)

        return info

    except Exception as e:
        error_list.append((bmson_file, str(e)))
        return None

    # finally:
    #     # 确保文件句柄关闭
    #     if 'file' in locals():
    #         await file.close()

async def process_batches(files, existing_file_names_song, existing_file_names_sub, settings, song_folder,
                          sub_folder, info, audio_data):
    for i in range(0, len(files), BATCH_SIZE):
        batch = files[i:i + BATCH_SIZE]
        tasks = []
        for file_path in batch:
            file_path = Path(file_path)
            if settings.include_images and file_path.suffix in {'.jpg', '.png'} and file_path.stem == Path(info.image).stem:
                 await copy_if_not_exists(file_path, song_folder / f"{info.img_filename}", existing_file_names_song)

            if settings.include_audio:
                if file_path.suffix in {'.mp3', '.wav', '.ogg'} and file_path.stem == Path(audio_data.main_audio).stem:
                    logger.info(f"匹配的主音频: {file_path}")
                    tasks.append(
                        copy_if_not_exists(file_path, song_folder / f"{info.song}", existing_file_names_song))
                    tasks.append(
                        copy_if_not_exists(file_path, sub_folder / file_path.name, existing_file_names_sub))
                elif file_path.suffix in {'.mp3', '.wav', '.ogg'} and file_path.stem != Path(audio_data.main_audio).stem:
                    if not await compare_file_names(existing_file_names_sub, (sub_folder / file_path.name).name):
                        await copy_if_not_exists(file_path, sub_folder / file_path.name, existing_file_names_sub)
                elif file_path.suffix in {'.wmv', '.mp4', '.avi'} and file_path.stem == Path(info.vdo).stem:
                    tasks.append(
                        copy_if_not_exists(file_path, song_folder / f"{info.vdo}", existing_file_names_song))

        await asyncio.gather(*tasks)


        # 先进行所有文件的对比和忽略操作
        # for file_path in files:
        #     file_path = Path(file_path)
        #     if settings.include_images and file_path.suffix in {'.jpg', '.png'} and file_path.stem == Path(info.image).stem:
        #         tasks.append(copy_if_not_exists(file_path, song_folder / f"{info.img_filename}", existing_file_names_song))
        #
        #     if settings.include_audio:
        #         if file_path.suffix in {'.mp3', '.wav', '.ogg'} and file_path.stem == Path(audio_data.main_audio).stem:
        #             tasks.append(copy_if_not_exists(file_path, song_folder / f"{info.song}", existing_file_names_song))
        #             tasks.append(copy_if_not_exists(file_path, sub_folder / file_path.name, existing_file_names_sub))
        #         elif file_path.suffix in {'.mp3', '.wav', '.ogg'} and file_path.stem != Path(audio_data.main_audio).stem:
        #             if not await compare_file_names(existing_file_names_sub, (sub_folder / file_path.name).name):
        #                 tasks.append(copy_if_not_exists(file_path, sub_folder / file_path.name, existing_file_names_sub))
        #         elif file_path.suffix in {'.wmv', '.mp4', '.avi'} and file_path.stem == Path(info.vdo).stem:
        #             tasks.append(copy_if_not_exists(file_path, song_folder / f"{info.vdo}", existing_file_names_song))
        #
async def copy_if_not_exists(file_path, destination_path, existing_file_names):
    async with semaphore:
        if not await compare_file_names(existing_file_names, destination_path.name):
            await copy_file(file_path, destination_path)
        else:
            logger.info(f"文件 {destination_path} 已存在，跳过复制")

async def copy_file(file_path, destination_path):
    try:
        async with aiofiles.open(file_path, 'rb') as src, aiofiles.open(destination_path, 'wb') as dst:
            await dst.write(await src.read())
        logger.info(f"文件 {file_path} 成功复制到 {destination_path}")
    except Exception as e:
        logger.error(f"复制文件 {file_path} 到 {destination_path} 时出错: {e}")

async def get_existing_file_names(folder_path):
    return {file.name for file in folder_path.iterdir() if file.is_file()}

async def compare_file_names(existing_file_names, file_name):
    return file_name in existing_file_names

async def scan_folder(folder_path):
    folder_path = Path(folder_path)
    files = [str(file) for file in folder_path.rglob('*') if file.is_file()]
    return files

def extract_parent_name_suffix(parent_name):
    # 使用正则表达式查找 '_数字' 形式的后缀
    match = re.search(r'_\d+$', parent_name)
    return match.group(0) if match else ''

def sanitize_folder_name(name):
    return re.sub(r'[^\w\-_.?]', '_', name)

def add_long_path_prefix(path):
    return r"r{}".format(path)