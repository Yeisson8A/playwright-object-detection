import json
import os
from pathlib import Path
import shutil
import aiohttp

def create_download_folder():
    download_dir = Path("data")

    # Borrar directorio y su contenido
    if download_dir.exists() and download_dir.is_dir():
        shutil.rmtree(download_dir)

    # Crear directorio para archivos a descargar
    download_dir.mkdir(exist_ok=True)
    return download_dir

def generate_report_json(data, download_dir, filename):
    full_path = os.path.join(download_dir, filename)

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

async def download_image(url, path):

    async with aiohttp.ClientSession() as session:

        async with session.get(url) as resp:

            if resp.status == 200:

                data = await resp.read()

                with open(path, "wb") as f:
                    f.write(data)