import shutil, json, pathlib
import asyncio, aiofiles
from bin.Dispatch_data import dispatch, scan_folder
from bin.custom_log import setup_custom_logger

logger = setup_custom_logger(__name__)

async def process_file(bmson_file, output_folder, settings, error_list):
    try:
        output_folder = pathlib.Path(output_folder)
        async with aiofiles.open(bmson_file, 'r', encoding='utf-8') as file:
            data = json.loads(await file.read())
            data['input_file_path'] = str(bmson_file)  # 添加文件路径到数据中

        osu_content, info, main_audio = dispatch(data, settings)

        # 使用原始名称创建文件夹
        song_folder = output_folder / info.new_folder
        song_folder.mkdir(parents=True, exist_ok=True)
        sub_folder = song_folder / info.sub_folder
        sub_folder.mkdir(parents=True, exist_ok=True)

        osu_file_path = song_folder / f"{info.osu_filename}.osu"
        async with aiofiles.open(osu_file_path, 'w', encoding='utf-8') as file:
            await file.write(osu_content)

        # 获取目标文件夹中的所有文件名
        existing_file_names_song = await get_existing_file_names(song_folder)
        existing_file_names_sub = await get_existing_file_names(sub_folder)
        tasks = {
            "large": [],
            "small": []
        }

        files = scan_folder(bmson_file.parent)

        # 先进行所有文件的对比和忽略操作
        for file_path in files:
            file_path = pathlib.Path(file_path)
            if settings.include_images and file_path.suffix in {'.jpg', '.png'} and file_path.stem == pathlib.Path(
                    info.image).stem:
                tasks["small"].append(copy_if_not_exists(file_path, song_folder / f"{info.img_filename}", existing_file_names_song))

            if settings.include_audio:
                if file_path.suffix in {'.mp3', '.wav', '.ogg'} and file_path.stem == pathlib.Path(main_audio).stem:
                    tasks["large"].append(copy_if_not_exists(file_path, song_folder / f"{info.song}", existing_file_names_song))
                elif file_path.suffix in {'.wmv', '.mp4', '.avi'} and file_path.stem == pathlib.Path(info.vdo).stem:
                    tasks["large"].append(copy_if_not_exists(file_path, song_folder / f"{info.vdo}", existing_file_names_song))
                elif file_path.suffix in {'.mp3', '.wav', '.ogg'} and file_path.stem != pathlib.Path(main_audio).stem:
                    if not await compare_file_names(existing_file_names_sub, (sub_folder / file_path.name).name):
                        tasks["small"].append(copy_if_not_exists(file_path, sub_folder / file_path.name, existing_file_names_sub))
        # 批量执行所有任务
        await asyncio.gather(*tasks["small"])
        await asyncio.gather(*tasks["large"])
        return info

    except Exception as e:
        error_list.append((bmson_file, str(e)))
        return None

async def copy_if_not_exists(file_path, destination_path, existing_file_names):
    if not await compare_file_names(existing_file_names, destination_path.name):
        await copy_file(file_path, destination_path)
    else:
        logger.info(f"文件 {destination_path} 已存在，跳过复制")

async def copy_file(file_path, destination_path):
    try:
        shutil.copy(file_path, destination_path)
        logger.info(f"文件 {file_path} 成功复制到 {destination_path}")
    except Exception as e:
        logger.error(f"复制文件 {file_path} 到 {destination_path} 时出错: {e}")

async def get_existing_file_names(folder_path):
    return {file.name for file in folder_path.iterdir() if file.is_file()}

async def compare_file_names(existing_file_names, file_name):
    return file_name in existing_file_names