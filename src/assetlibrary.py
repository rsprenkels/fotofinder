import hashlib
import logging
import os
import pickle
import shutil
from pathlib import Path

import numpy


def compute_file_hash(file_path, algorithm="sha256"):
    """Compute the hash of a file using the specified algorithm."""
    hash_func = hashlib.new(algorithm)

    with open(file_path, "rb") as file:
        # Read the file in chunks of 8192 bytes
        while chunk := file.read(8192):
            hash_func.update(chunk)

    return hash_func.hexdigest()


def want_this(file) -> bool:
    filename, file_extension = os.path.splitext(file)
    return file_extension[1:].lower() in ["jpg", "png", "heic", "mp4", "mov"]


class AssetLibrary:
    def __init__(self, asset_root_dir: str):
        self.logger = logging.getLogger(__name__)
        self.root_dir = asset_root_dir
        Path(self.root_dir).mkdir(parents=True, exist_ok=True)
        self.library_state_file = Path(self.root_dir, "_library_state_file.pkl")
        if self.library_state_file.is_file():
            with open(self.library_state_file.as_posix(), "rb") as f:
                state = pickle.load(f)
                self.assets = state["assets"]
                self.sequence_number = state["sequence_number"]
                self.logger.info(f"read pickle file")
        else:
            self.assets = dict()
            self.sequence_number = 0
            self.logger.info(f"empty library created")
        self.logger.info(
            f"AssetLibrary instantiated {self.sequence_number} {len(self.assets)}"
        )

    def close(self):
        self.logger.info(f"closing library {self.library_state_file}")
        pass
        with open(self.library_state_file.as_posix(), "wb") as f:
            state = dict()
            state["assets"] = self.assets
            state["sequence_number"] = self.sequence_number
            pickle.dump(state, f)
        self.logger.info(f"AssetLibrary destroyed")

    def contains(self, hash_value: str) -> bool:
        return hash_value in self.assets.keys()

    def add(
        self,
        root: str,
        file: str,
        hash_value: str,
    ):
        seq_nr = numpy.base_repr(self.sequence_number, base=36, padding=4)[-4:]
        self.assets[hash_value] = (root, file, self.sequence_number)
        self.sequence_number += 1
        filename, file_extension = os.path.splitext(file)
        shutil.copyfile(
            f"{root}//{file}",
            f"{self.root_dir}/{filename}_{seq_nr}{file_extension}",
        )

    def get_all_assets(self, starting_dir: str):
        self.logger.info(f"getting all from {starting_dir}")
        for root, dirs, files in os.walk(starting_dir):
            path = root.split(os.sep)
            # print(f"root:{root}  path:{path}  dirs:{dirs}  files:{files}")
            # print((len(path) - 1) * "---", os.path.basename(root))
            for file in files:
                if want_this(file):
                    file_hash = compute_file_hash(Path(root, file).as_posix())
                    if not self.contains(file_hash):
                        self.logger.info(f"adding {file} with hash {file_hash}")
                        self.add(root, file, file_hash)
                    else:
                        self.logger.info(
                            f"already available {file} with hash {file_hash}"
                        )


def test_001():
    asset_lib_path = r"C:\Users\RonSprenkels\IdeaProjects\fotofinder\foto_library"
    shutil.rmtree(asset_lib_path)
    f = AssetLibrary(asset_lib_path)
    assert f.sequence_number == 0
    starting_dir = r"C:\Users\RonSprenkels\IdeaProjects\fotofinder\test_data"
    f.get_all_assets(Path(starting_dir, "b1").as_posix())
    assert f.sequence_number == 2
    f.get_all_assets(Path(starting_dir, "b2").as_posix())
    assert f.sequence_number == 3
    f.get_all_assets(Path(starting_dir, "b3").as_posix())
    f.close()
