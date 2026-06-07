#!/usr/bin/env python3

import os
import shutil
import sys
from pathlib import Path

SKEL_DIR = "/etc/skel"
HOME_DIR = Path.home()


def confirm():
    answer = input(
        f"This will overwrite files in {HOME_DIR} with those from {SKEL_DIR}.\n"
        "Are you sure you want to continue? (yes/no): "
    ).strip().lower()
    return answer in ("yes", "y")


def copy_skel(src, dst):
    for root, dirs, files in os.walk(src):
        rel_path = os.path.relpath(root, src)
        target_dir = os.path.join(dst, rel_path) if rel_path != "." else dst

        # Create directories if they don't exist
        os.makedirs(target_dir, exist_ok=True)

        # Copy files
        for file_name in files:
            src_file = os.path.join(root, file_name)
            dst_file = os.path.join(target_dir, file_name)

            try:
                shutil.copy2(src_file, dst_file)  # preserves metadata
                print(f"Copied: {dst_file}")
            except Exception as e:
                print(f"Error copying {src_file} -> {dst_file}: {e}")


def main():
    if not os.path.isdir(SKEL_DIR):
        print(f"Error: {SKEL_DIR} does not exist.")
        sys.exit(1)

    if not confirm():
        print("Operation cancelled.")
        sys.exit(0)

    print("Resetting home directory...")
    copy_skel(SKEL_DIR, HOME_DIR)
    print("Done.")


if __name__ == "__main__":
    main()