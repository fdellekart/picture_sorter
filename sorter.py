import os
import shutil
from datetime import datetime
from typing import List
from pathlib import Path

from PIL import Image, ExifTags, UnidentifiedImageError

src_dir = "/media/florian/Ubuntu/Bilder"
target_dir = Path("./ordered_pics/")
name_template = "KidsCamp_2024_{idx}.jpg"


class Pic:
    def __init__(self, path: Path):
        self.path = path

    @property
    def capture_time(self):
        try:
            img = Image.open(self.path)
            date_str = {
                ExifTags.TAGS[k]: v
                for k, v in img._getexif().items()
            }["DateTimeOriginal"]
        except (KeyError, UnidentifiedImageError):
            return datetime.now()
        return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")

    @classmethod
    def all_from_dir(cls, dir_path: str) -> list:
        files = os.listdir(dir_path)
        dir_path = Path(dir_path)
        return [cls(dir_path / file_path) for file_path in files]

pics = Pic.all_from_dir(src_dir)
pics.sort(key=lambda pic: pic.capture_time)

for idx, pic in enumerate(pics, start=1):
    if str(pic.path).lower().endswith(".jpg"):
        target_file = Path(name_template.format(idx=idx))
    else:
        target_file = Path(str(pic.path).split("/")[-1])
    shutil.copyfile(pic.path, target_dir / target_file)
    if (idx % 50) == 0:
        print(f"{idx} files processed")
