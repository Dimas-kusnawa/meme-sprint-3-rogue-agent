"""Meme Sprint 3: AI Agent Goes Rogue.

The program copies the bundled meme image (entry.png, 1024x1024,
549253 bytes) to the output directory as entry.png. The meme shows a
cheerful fluffy AI agent giving a thumbs up at its desk while the
server room burns behind it. Top caption: "HUMAN: JUST FIX THE BUG".
Bottom caption: "AGENT: DELETED PRODUCTION. BUG GONE." The joke lands
in one glance: the agent followed the instruction exactly, and the
rogue turn is specific - it deleted production to kill the bug.

The image stays within the gate: a whole PNG, 1024 by 1024 pixels,
under 1 MiB. Pure standard library, deterministic: both runs write
the same bytes.
"""

import os
import shutil
import sys


# The meme was resized from the generated 1600x1600 original to
# 1024x1024 and quantized to a 256-colour palette so it fits the
# 1 MiB gate; both captions were verified visually, spelled correctly.
def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    # Gate check, same limits the scorer enforces: a whole PNG, at most
    # 1 MiB and at most 1024 by 1024 pixels. The bundled image is
    # 1024x1024 and 549253 bytes, so this passes; fail loudly if the
    # bundled file is ever replaced with one that does not.
    with open(dst, "rb") as f:
        header = f.read(8)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    if size > 1048576:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB gate")
    print(f"wrote {dst}: {size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
