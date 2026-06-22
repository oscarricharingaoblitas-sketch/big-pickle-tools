import os, re, sys

def bulk_rename(directory, pattern, replacement, dry_run=True):
    changes = []
    for filename in os.listdir(directory):
        new_name = re.sub(pattern, replacement, filename)
        if new_name != filename:
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_name)
            changes.append((filename, new_name))
            if not dry_run:
                os.rename(old_path, new_path)
    return changes

def number_files(directory, prefix="file_", start=1, padding=3, dry_run=True):
    changes = []
    for i, filename in enumerate(sorted(os.listdir(directory))):
        ext = os.path.splitext(filename)[1]
        new_name = f"{prefix}{str(start + i).zfill(padding)}{ext}"
        if new_name != filename:
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_name)
            changes.append((filename, new_name))
            if not dry_run:
                os.rename(old_path, new_path)
    return changes

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Bulk rename files with regex or numbering")
    parser.add_argument("directory", help="Target directory")
    parser.add_argument("--pattern", help="Regex pattern to match")
    parser.add_argument("--replacement", help="Replacement string")
    parser.add_argument("--prefix", default="file_", help="Prefix for numbering mode")
    parser.add_argument("--start", type=int, default=1, help="Start number")
    parser.add_argument("--padding", type=int, default=3, help="Zero padding")
    parser.add_argument("--number", action="store_true", help="Use numbering mode")
    parser.add_argument("--execute", action="store_true", help="Actually rename (default: dry-run)")
    args = parser.parse_args()

    if args.number:
        changes = number_files(args.directory, args.prefix, args.start, args.padding, not args.execute)
    else:
        changes = bulk_rename(args.directory, args.pattern, args.replacement, not args.execute)

    if not changes:
        print("No files to rename.")
        return
    print(f"{'Would rename' if not args.execute else 'Renamed'} {len(changes)} files:")
    for old, new in changes:
        print(f"  {old} -> {new}")
