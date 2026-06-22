#!/usr/bin/env python3
"""Duplicate File Finder — Find and manage duplicate files by content hash."""
import os, sys, hashlib, json
from pathlib import Path
from collections import defaultdict

BLOCK_SIZE = 65536

def hash_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(BLOCK_SIZE):
            h.update(chunk)
    return h.hexdigest()

def scan(root, min_size=1, exclude_dirs=None):
    exclude = set(exclude_dirs or [])
    hashes = defaultdict(list)
    total = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in exclude]
        for fn in filenames:
            fp = Path(dirpath) / fn
            try:
                if fp.stat().st_size >= min_size:
                    h = hash_file(fp)
                    hashes[h].append(str(fp))
                    total += 1
            except (PermissionError, OSError):
                pass
    dupes = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return dupes, total

def format_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024: return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"Scanning {root} ...")
    dupes, total = scan(root, exclude_dirs={"$Recycle.Bin", "System Volume Information", "node_modules", ".git", "__pycache__", "venv"})
    wasted = 0
    for h, paths in sorted(dupes.items(), key=lambda x: -os.path.getsize(x[1][0])):
        size = os.path.getsize(paths[0])
        wasted += size * (len(paths) - 1)
        print(f"\n{format_size(size)} — {len(paths)} copies")
        for p in paths[:5]:
            print(f"  {p}")
        if len(paths) > 5: print(f"  ... and {len(paths)-5} more")
    print(f"\n{'='*50}")
    print(f"  Files scanned: {total}")
    print(f"  Duplicate sets: {len(dupes)}")
    print(f"  Wasted space: {format_size(wasted)}")
    print(f"{'='*50}")
