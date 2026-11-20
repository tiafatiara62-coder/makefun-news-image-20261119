#!/usr/bin/env python3
"""The World Today — v2 entry for news-image-20261119.

Copies the pre-drawn broadsheet (33 verified stories from Thursday
19 November 2026) to the output directory as entry.png.
Stdlib only; deterministic: the same bytes every run.
"""
import hashlib
import os
import shutil

MAX_BYTES = 1048576


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
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")

    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != size:
        raise SystemExit(f"copy incomplete: {dst} is not {size} bytes")

    digest = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    print(f"wrote {dst} ({size} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
