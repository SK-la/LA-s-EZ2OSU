#Dispatch_file.py
import shutil
import json
import logging
import pathlib
from Dispatch_data import dispatch, scan_folder

def get_unique_filename(existing_path):
    base, extension = existing_path.stem, existing_path.suffix
    counter = 1
    while existing_path.exists():
        existing_path = existing_path.with_name(f"{base}_old_{counter}{extension}")
        counter += 1
    return existing_path

def process_file(bmson_file, output_folder, settings):

    try:
        output_folder = pathlib.Path(output_folder)
        
        with bmson_file.open('r', encoding='utf-8') as file:
            data = json.load(file)
        
        osu_content, info, main_audio = dispatch(data, settings)

        # 创建歌曲文件夹和子文件夹
        if settings.auto_create_output_folder:
            song_folder = output_folder / info.new_folder
            song_folder.mkdir(parents=True, exist_ok=True)
            sub_folder = song_folder / info.sub_folder
            sub_folder.mkdir(parents=True, exist_ok=True)
            output_folder = song_folder
        else:
            song_folder = output_folder / info.new_folder
            song_folder.mkdir(parents=True, exist_ok=True)
            sub_folder = song_folder / info.sub_folder
            sub_folder.mkdir(parents=True, exist_ok=True)
            output_folder = song_folder
            output_folder.mkdir(parents=True, exist_ok=True)

        files = scan_folder(bmson_file.parent)
        for file_path in files:
            file_path = pathlib.Path(file_path)
            if (settings.include_audio and file_path.suffix in {'.mp3', '.wav', '.ogg', '.wmv', '.mp4', '.avi'}) or \
       (settings.include_images and file_path.suffix in {'.jpg', '.png'} and file_path.stem == pathlib.Path(info.image).stem):

                if file_path.suffix in {'.jpg', '.png'} and file_path.stem == pathlib.Path(info.image).stem:
                    mda_new_name = f"{info.img_filename}"

                elif file_path.suffix in {'.wav', '.ogg'} and file_path.stem == pathlib.Path(main_audio).stem:
                    mda_new_name = f"{info.song}"

                elif file_path.suffix in {'.wmv', '.mp4', '.avi'} and file_path.stem == pathlib.Path(info.vdo).stem:
                    mda_new_name = f"{info.vdo}"

                else:
                    sub_folder_path = output_folder / info.sub_folder
                    if not sub_folder_path.exists():
                        sub_folder_path.mkdir(parents=True, exist_ok=True)
                    mda_new_name = sub_folder_path / file_path.name

                destination_path = output_folder / mda_new_name
                if not destination_path.exists():
                    shutil.copy(file_path, destination_path)

        osu_file_path = output_folder / f"{info.osu_filename}.osu"
        with osu_file_path.open('w', encoding='utf-8') as file:
            file.write(osu_content)

        return info

    except Exception as e:
        logging.error(f"Error process_file: {e}")
        return None
