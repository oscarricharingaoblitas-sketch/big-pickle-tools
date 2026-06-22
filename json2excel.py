#!/usr/bin/env python3
"""JSON to Excel Converter — Flatten nested JSON into Excel spreadsheets."""
import json, sys, os
from collections.abc import MutableMapping
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    sys.exit("pip install pandas openpyxl")

def flatten(d, parent="", sep="_"):
    items = []
    for k, v in d.items():
        key = f"{parent}{sep}{k}" if parent else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, MutableMapping):
                    items.extend(flatten(item, f"{key}{sep}{i}", sep=sep).items())
                else:
                    items.append((f"{key}{sep}{i}", item))
        else:
            items.append((key, v))
    return dict(items)

def convert(input_file, output_file=None):
    if not output_file:
        output_file = Path(input_file).with_suffix(".xlsx").name
    with open(input_file) as f:
        data = json.load(f)
    if isinstance(data, list):
        rows = [flatten(item) for item in data]
    else:
        rows = [flatten(data)]
    df = pd.DataFrame(rows)
    df.to_excel(output_file, index=False, engine="openpyxl")
    print(f"Converted {input_file} -> {output_file} ({len(df)} rows, {len(df.columns)} columns)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python json2excel.py input.json [output.xlsx]")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
