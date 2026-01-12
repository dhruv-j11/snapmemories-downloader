# oversees folders, filenames, and duplicates

import os
import hashlib
from datetime import datetime

def hash_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def build_path(base_dir, date_str, ext):
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S UTC")
    year = str(dt.year)

    folder = os.path.join(base_dir, year)
    os.makedirs(folder, exist_ok=True)

    name = dt.strftime("%Y-%m-%d_%H-%M-%S") + ext
    return os.path.join(folder, name)
