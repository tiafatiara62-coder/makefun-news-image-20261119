#!/usr/bin/env python3
"""Copy the pre-drawn entry image to the make.fun output directory.

The newspaper image is drawn at build time and committed to this repo as
entry.png. This script does no drawing at all and needs no third-party
packages: it only copies the bundled PNG into the output directory, after
checking the 1 MiB size limit, the PNG magic bytes, and that the copy is
complete. That keeps the grade run working in a minimal Python image with
no fonts and no image libraries installed.
"""

import hashlib
import os
import shutil
import sys

MAX_BYTES = 1_048_576  # 1 MiB
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(source):
        return fail(f"entry.png not found next to main.py: {source}")

    size = os.path.getsize(source)
    if size > MAX_BYTES:
        return fail(f"entry.png is {size} bytes, over the {MAX_BYTES} byte limit")

    with open(source, "rb") as handle:
        magic = handle.read(len(PNG_MAGIC))
    if magic != PNG_MAGIC:
        return fail("entry.png does not start with the PNG magic bytes")

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, dest)

    copied = os.path.getsize(dest)
    if copied != size:
        return fail(f"copy incomplete: wrote {copied} of {size} bytes")

    source_digest = sha256_of(source)
    dest_digest = sha256_of(dest)
    if dest_digest != source_digest:
        return fail(f"copy corrupted: sha256 {dest_digest} != source {source_digest}")

    print(f"wrote {dest} ({copied} bytes, sha256 {dest_digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
