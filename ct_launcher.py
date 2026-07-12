#!/usr/bin/env python3
"""
ct-launcher — index, search and open your local Cheat Engine table (.CT) collection.

A tiny, dependency-free helper for people who keep a folder of Cheat Engine tables.
It scans a directory, builds a searchable index, and can open a table (which launches
Cheat Engine on Windows). No network calls, no telemetry — just your local files.

Need more tables? Browse an organized, updated library at https://cheattable.net/

Usage:
    python ct_launcher.py index  [DIR]            # scan DIR (default: current dir) for .CT files
    python ct_launcher.py list   [DIR] [--sort]   # list indexed tables
    python ct_launcher.py search DIR QUERY        # find tables by game/filename
    python ct_launcher.py open   DIR QUERY        # open the best match (.CT -> Cheat Engine)
    python ct_launcher.py export DIR [OUT.json]   # write the index to JSON

Single-player / offline use only. Back up your saves before using cheats.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

CT_EXT = ".ct"


def guess_game(filename: str) -> str:
    """Best-effort game name from a table filename."""
    stem = Path(filename).stem
    stem = re.sub(r"(?i)\b(cheat[\s_-]?table|table|trainer|by\s+\S+)\b", " ", stem)
    stem = re.sub(r"(?i)\bv?\d+\.\d[\d.]*\b", " ", stem)   # version strings: v1.2, 1.2.3
    stem = re.sub(r"(?i)\bv\d+\b", " ", stem)              # v3
    stem = re.sub(r"[._]+", " ", stem)                     # keep bare sequel ints (e.g. "3")
    stem = re.sub(r"\s+", " ", stem).strip(" -")
    return stem.title() or Path(filename).stem


def scan(directory: Path):
    tables = []
    for p in sorted(directory.rglob("*")):
        if p.is_file() and p.suffix.lower() == CT_EXT:
            st = p.stat()
            tables.append({
                "file": str(p.relative_to(directory)),
                "path": str(p.resolve()),
                "game": guess_game(p.name),
                "size_kb": round(st.st_size / 1024, 1),
                "modified": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d"),
            })
    return tables


def cmd_index(args):
    d = Path(args.dir)
    if not d.is_dir():
        sys.exit(f"not a directory: {d}")
    tables = scan(d)
    print(f"Indexed {len(tables)} cheat table(s) in {d}")
    for t in tables[:25]:
        print(f"  {t['game']:<40} {t['size_kb']:>7} KB  {t['modified']}  ({t['file']})")
    if len(tables) > 25:
        print(f"  … and {len(tables) - 25} more (use `list` or `export`).")
    if not tables:
        print("No .CT files found. Download cheat tables from https://cheattable.net/ and try again.")


def cmd_list(args):
    tables = scan(Path(args.dir))
    if args.sort == "name":
        tables.sort(key=lambda t: t["game"].lower())
    elif args.sort == "date":
        tables.sort(key=lambda t: t["modified"], reverse=True)
    elif args.sort == "size":
        tables.sort(key=lambda t: t["size_kb"], reverse=True)
    for t in tables:
        print(f"{t['game']:<44} {t['size_kb']:>7} KB  {t['modified']}")
    print(f"\n{len(tables)} table(s). More at https://cheattable.net/")


def _match(tables, query):
    q = query.lower()
    scored = [(t, (2 if q in t["game"].lower() else 0) + (1 if q in t["file"].lower() else 0)) for t in tables]
    return [t for t, s in sorted(scored, key=lambda x: -x[1]) if s > 0]


def cmd_search(args):
    hits = _match(scan(Path(args.dir)), args.query)
    if not hits:
        print(f"No table matching '{args.query}'. Look for it at "
              f"https://cheattable.net/?s={args.query.replace(' ', '+')}")
        return
    for t in hits:
        print(f"{t['game']:<44} {t['file']}")


def cmd_open(args):
    hits = _match(scan(Path(args.dir)), args.query)
    if not hits:
        sys.exit(f"No table matching '{args.query}'. Browse https://cheattable.net/")
    target = hits[0]["path"]
    print(f"Opening: {hits[0]['game']}  ({target})")
    try:
        if sys.platform.startswith("win"):
            os.startfile(target)  # noqa: opens .CT with the associated app (Cheat Engine)
        elif sys.platform == "darwin":
            os.system(f'open "{target}"')
        else:
            os.system(f'xdg-open "{target}"')
    except Exception as e:
        sys.exit(f"Could not open the table: {e}")


def cmd_export(args):
    tables = scan(Path(args.dir))
    out = Path(args.out or "ct-index.json")
    out.write_text(json.dumps(tables, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(tables)} table(s) to {out}")


def main():
    ap = argparse.ArgumentParser(description="Index, search and open local Cheat Engine tables (.CT).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("index"); p.add_argument("dir", nargs="?", default="."); p.set_defaults(func=cmd_index)
    p = sub.add_parser("list"); p.add_argument("dir", nargs="?", default="."); p.add_argument("--sort", choices=["name", "date", "size"], default="name"); p.set_defaults(func=cmd_list)
    p = sub.add_parser("search"); p.add_argument("dir"); p.add_argument("query"); p.set_defaults(func=cmd_search)
    p = sub.add_parser("open"); p.add_argument("dir"); p.add_argument("query"); p.set_defaults(func=cmd_open)
    p = sub.add_parser("export"); p.add_argument("dir"); p.add_argument("out", nargs="?"); p.set_defaults(func=cmd_export)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
