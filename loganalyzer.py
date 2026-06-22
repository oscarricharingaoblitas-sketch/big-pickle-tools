#!/usr/bin/env python3
"""Log File Analyzer — Parse, analyze, and summarize log files."""
import sys, re, os
from collections import Counter
from datetime import datetime
from pathlib import Path

PATTERNS = {
    "ERROR": r"(?i)\berror\b",
    "WARN": r"(?i)\bwarn(ing)?\b",
    "INFO": r"(?i)\binfo\b",
    "DEBUG": r"(?i)\bdebug\b",
    "TRACE": r"(?i)\btrace\b",
    "FATAL": r"(?i)\bfatal\b",
    "IP": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    "TIMESTAMP": r"\d{4}[-/]\d{2}[-/]\d{2}[T ]\d{2}:\d{2}",
    "EMAIL": r"\b[\w.-]+@[\w.-]+\.\w+\b",
    "URL": r"https?://[^\s\"'>]+",
    "STATUS_4XX": r"\b(40[0-9]|41[0-9])\b",
    "STATUS_5XX": r"\b(50[0-9])\b",
}

def analyze(filepath):
    path = Path(filepath)
    if not path.exists(): sys.exit(f"File not found: {filepath}")
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    total = len(lines)
    print(f"{'='*55}")
    print(f"  Log File Analyzer — {path.name}")
    print(f"{'='*55}")
    print(f"  File:      {path.resolve()}")
    print(f"  Size:      {path.stat().st_size / 1024:.1f} KB")
    print(f"  Lines:     {total}")
    print(f"{'='*55}")
    counts = {}
    for label, pattern in PATTERNS.items():
        matches = [l for l in lines if re.search(pattern, l)]
        if matches:
            counts[label] = len(matches)
            print(f"  {label:12s} {len(matches):6d} ({len(matches)/total*100:5.1f}%)")
    print(f"{'='*55}")
    if counts.get("ERROR") or counts.get("FATAL"):
        print("  SAMPLE ERRORS (last 5):")
        err_lines = [l for l in lines if re.search(r"(?i)\berror\b", l) or re.search(r"(?i)\bfatal\b", l)]
        for l in err_lines[-5:]:
            print(f"    > {l[:120]}")
        print(f"{'='*55}")
    print(f"  Report: {total} lines, {len(counts)} categories found")
    print(f"{'='*55}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python loganalyzer.py <logfile>")
        sys.exit(1)
    analyze(sys.argv[1])
