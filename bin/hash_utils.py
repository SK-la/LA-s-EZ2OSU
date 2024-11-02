#bin/io_utils.py
import hashlib, aiofiles, pathlib, json

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
