#!/usr/bin/env python3
"""GitHub Repo Stats CLI — Get detailed stats for any public GitHub repo."""
import json, sys, os, urllib.request, urllib.error
from datetime import datetime

API = "https://api.github.com"

def req(path):
    url = f"{API}{path}"
    try:
        with urllib.request.urlopen(url) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.reason}")

def fmt(n):
    if n >= 1_000_000: return f"{n/1e6:.1f}M"
    if n >= 1_000: return f"{n/1e3:.1f}K"
    return str(n)

def stats(repo):
    d = req(f"/repos/{repo}")
    commits = len(req(f"/repos/{repo}/commits?per_page=1")) or "?"
    rel = req(f"/repos/{repo}/releases?per_page=1")
    print(f"\n{'='*50}")
    print(f"  {d['full_name']}")
    print(f"{'='*50}")
    print(f"  Description:  {d['description'] or 'N/A'}")
    print(f"  Stars:        {fmt(d['stargazers_count'])}")
    print(f"  Forks:        {fmt(d['forks_count'])}")
    print(f"  Issues:       {fmt(d['open_issues_count'])}")
    print(f"  Watchers:     {fmt(d['subscribers_count'])}")
    print(f"  Language:     {d['language'] or 'N/A'}")
    print(f"  License:      {d['license']['spdx_id'] if d.get('license') else 'N/A'}")
    print(f"  Size:         {fmt(d['size'])} KB")
    print(f"  Created:      {d['created_at'][:10]}")
    print(f"  Updated:      {d['updated_at'][:10]}")
    print(f"  Pushed:       {d['pushed_at'][:10]}")
    print(f"  Topics:       {', '.join(d.get('topics', [])[:8]) or 'N/A'}")
    print(f"  Releases:     {len(rel)}")
    print(f"  URL:          {d['html_url']}")
    print(f"{'='*50}\n")
    return d

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ghstats.py owner/repo")
        sys.exit(1)
    stats(sys.argv[1])
