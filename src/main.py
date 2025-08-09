import shutil
import os

from config import WORKING_DIR


def handle_delete_error():
    print("failed to delete destination dir")
    os.exit(1)


def main():
    abs_path = os.path.abspath(WORKING_DIR)
    dist = os.path.join(abs_path, "public")
    src = os.path.join(abs_path, "static")

    if not os.path.exists(src):
        print("cannot find static directory")
        os.exit(1)

    if os.path.exists(dist):
        print(f"found path: {dist}")
        print(f"started to delete contents of {dist}")
        shutil.rmtree(path=dist, ignore_errors=False, onerror=handle_delete_error)

    print(f"making empty dir: {dist}")
    os.mkdir(dist)
    print(f"started copying from {src} to {dist}")
    shutil.copytree(src, dist, dirs_exist_ok=True)
    print("finished copying contents")


if __name__ == "__main__":
    main()
