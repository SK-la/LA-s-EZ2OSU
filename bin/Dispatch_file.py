import aiofiles
import asyncio
import hashlib
import json
import pathlib
import os
from bin.Dispatch_data import dispatch
from bin.utils import setup_custom_logger, load_hash_cache, save_hash_cache


logger = setup_custom_logger(__name__)

async def process_file(bmson_file, output_folder, settings, error_list, cache_folder):
    try:
        output_folder = pathlib.Path(output_folder)
        cache_folder = cache_folder / bmson_file.parent.name
        # 加载哈希缓存
        hash_cache = await load_hash_cache(cache_folder)

        async with aiofiles.open(bmson_file, 'r', encoding='utf-8') as file:
            data = json.loads(await file.read())
            data['input_file_path'] = str(bmson_file)  # 添加文件路径到数据中

        osu_content, info, audio_data = dispatch(data, settings)
        new_md5 = hashlib.md5(osu_content.encode('utf-8')).hexdigest()

        # 使用原始名称创建文件夹
        song_folder = output_folder / info.new_folder
        song_folder.mkdir(parents=True, exist_ok=True)
        sub_folder = song_folder / info.sub_folder
        sub_folder.mkdir(parents=True, exist_ok=True)

        osu_file_path = song_folder / f"{info.osu_filename}.osu"

        # Check if the file already exists and compare content
        if osu_file_path.exists():
            existing_md5 = hash_cache.get(str(osu_file_path))
            if not existing_md5:
                async with aiofiles.open(osu_file_path, 'rb') as f:
                    existing_md5 = hashlib.md5(await f.read()).hexdigest()
                hash_cache[str(osu_file_path)] = existing_md5
            if existing_md5 == new_md5:
                logger.info(f"File {osu_file_path} already exists and is identical. Skipping.")
                return

        async with aiofiles.open(osu_file_path, 'w', encoding='utf-8') as file:
            await file.write(osu_content)

        # 获取目标文件夹中的所有文件名
        existing_file_names_song = await get_existing_file_names(song_folder)
        existing_file_names_sub = await get_existing_file_names(sub_folder)
        tasks = {
            "large": [],
            "small": []
        }

        files = await scan_folder(bmson_file.parent)

        # 先进行所有文件的对比和忽略操作
        for file_path in files:
            file_path = pathlib.Path(file_path)
            if settings.include_images and file_path.suffix in {'.jpg', '.png'} and file_path.stem == pathlib.Path(info.image).stem:
                tasks["small"].append(copy_if_not_exists(file_path, song_folder / f"{info.img_filename}", existing_file_names_song))

            if settings.include_audio:
                if file_path.suffix in {'.mp3', '.wav', '.ogg'} and file_path.stem == pathlib.Path(audio_data.main_audio).stem:
                    tasks["large"].append(copy_if_not_exists(file_path, song_folder / f"{info.song}", existing_file_names_song))
                    tasks["large"].append(copy_if_not_exists(file_path, sub_folder / file_path.name, existing_file_names_sub))
                elif file_path.suffix in {'.mp3', '.wav', '.ogg'} and file_path.stem != pathlib.Path(audio_data.main_audio).stem:
                    if not await compare_file_names(existing_file_names_sub, (sub_folder / file_path.name).name):
                        tasks["small"].append(copy_if_not_exists(file_path, sub_folder / file_path.name, existing_file_names_sub))
                elif file_path.suffix in {'.wmv', '.mp4', '.avi'} and file_path.stem == pathlib.Path(info.vdo).stem:
                    tasks["large"].append(copy_if_not_exists(file_path, song_folder / f"{info.vdo}", existing_file_names_song))

        # 批量执行所有任务
        await asyncio.gather(*[await task for task in tasks["small"]])
        await asyncio.gather(*[await task for task in tasks["large"]])
        # 保存哈希缓存
        await save_hash_cache(cache_folder, hash_cache)
        return info

    except Exception as e:
        error_list.append((bmson_file, str(e)))
        return None

    # finally:
    #     # 确保文件句柄关闭
    #     if 'file' in locals():
    #         await file.close()

async def copy_if_not_exists(file_path, destination_path, existing_file_names):
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
    files = []
    folder_path = os.path.normpath(folder_path)
    for root, _, filenames in os.walk(folder_path):
        root = os.path.normpath(root)
        for filename in filenames:
            file_path = os.path.join(root, filename)
            file_path = os.path.normpath(file_path)
            if os.path.isfile(file_path):
                files.append(file_path)
    return files
