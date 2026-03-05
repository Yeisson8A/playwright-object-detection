import json
import os
from pathlib import Path
import shutil
import requests

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

def download_image(url, path):
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        with open(path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)