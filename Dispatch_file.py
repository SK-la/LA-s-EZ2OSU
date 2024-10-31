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
        
        osu_content, info_obj, names_obj, main_audio = dispatch(data, settings)

        output_folder.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created output folder: {output_folder}")

        files = scan_folder(bmson_file.parent)
        for file_path in files:
            file_path = pathlib.Path(file_path)
            if (settings.include_audio and file_path.suffix in {'.mp3', '.wav', '.ogg', '.wmv', '.mp4', '.avi'}) or \
               (settings.include_images and file_path.suffix in {'.jpg', '.png'} and file_path.stem == pathlib.Path(info_obj.image).stem):

                if file_path.suffix in {'.jpg', '.png'} and file_path.stem == pathlib.Path(info_obj.image).stem:
                    mda_new_name = f"{names_obj.img_filename}"

                elif file_path.suffix in {'.wav', '.ogg'} and file_path.stem == pathlib.Path(main_audio).stem:
                    mda_new_name = f"{info_obj.song}"

                elif file_path.suffix in {'.wmv', '.mp4', '.avi'} and file_path.stem == pathlib.Path(info_obj.vdo).stem:
                    mda_new_name = f"{info_obj.vdo}"

                else:
                    sub_folder_path = output_folder / names_obj.sub_folder
                    sub_folder_path.mkdir(parents=True, exist_ok=True)
                    mda_new_name = sub_folder_path / file_path.name

                destination_path = output_folder / mda_new_name
                shutil.copy(file_path, destination_path)

        osu_file_path = output_folder / f"{names_obj.osu_filename}.osu"
        with osu_file_path.open('w', encoding='utf-8') as file:
            file.write(osu_content)

        return names_obj

    except Exception as e:
        logging.error(f"Error process_file: {e}")
        return None
