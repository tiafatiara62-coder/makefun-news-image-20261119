#!/usr/bin/env python3
"""News-image entry: copy the pre-built entry.png to the output directory."""
import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit(f"copy incomplete: {dst} is not the same size as {src}")
    print("wrote", dst)


if __name__ == "__main__":
    main()
