import os
import logging
from pathlib import Path
from assetlibrary import AssetLibrary, compute_file_hash

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("        main")


def main():
    log.info(f"starting")
    f = AssetLibrary(r"C:\Users\RonSprenkels\IdeaProjects\fotofinder\foto_library")

    starting_dir = r"C:\Users\RonSprenkels\IdeaProjects\fotofinder\test_data"
    f.get_all_assets(Path(starting_dir, "b1").as_posix())
    f.close()


if __name__ == "__main__":
    main()
