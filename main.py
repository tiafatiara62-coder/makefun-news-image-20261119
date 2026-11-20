#!/usr/bin/env python3
"""The World Today — v4 entry for news-image-20261119.

Copies the pre-drawn broadsheet (33 verified stories from Thursday
19 November 2026) to the output directory as entry.png.
Python 3.13 standard library only; deterministic: the same bytes
come out on every run.
"""
import hashlib
import os
import shutil

MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")

    size = os.path.getsize(src)
    if size > MAX_BYTES:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB limit")
    with open(src, "rb") as fh:
        head = fh.read(len(PNG_MAGIC))
    if head != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG file")

    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != size:
        raise SystemExit(f"copy incomplete: {dst} is not {size} bytes")

    def digest(path):
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()

    if digest(dst) != digest(src):
        raise SystemExit(f"copy mismatch: {dst} sha256 differs from source")
    print(f"wrote {dst} ({size} bytes, sha256 {digest(dst)})")


if __name__ == "__main__":
    main()
