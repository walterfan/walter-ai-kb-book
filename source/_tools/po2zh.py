#!/usr/bin/env python3
"""
Extract translations from .po files and apply them to the source .md files,
producing Chinese markdown files in-place.

For msgid/msgstr pairs where msgstr is non-empty, replace the English text.
For empty msgstr, keep the original English (to be translated manually or by LLM).

Usage:
    python3 po2zh.py [--dry-run]
"""
import re
import os
import sys
import glob

SOURCE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCALE_DIR = os.path.join(SOURCE_DIR, "locale", "zh_CN", "LC_MESSAGES")

PARTS = [
    "part1-foundations",
    "part2-prose-layer",
    "part3-code-layer",
    "part4-operations-lifecycle",
    "part5-hybrid-layer",
    "part6-governance-and-outlook",
]


def parse_po(po_path):
    """Parse a .po file and return a dict of {msgid: msgstr}."""
    with open(po_path, "r", encoding="utf-8") as f:
        content = f.read()

    entries = {}
    # Split on blank-line-separated blocks
    blocks = re.split(r"\n\n+", content)

    for block in blocks:
        lines = block.strip().split("\n")
        if not lines:
            continue

        msgid_parts = []
        msgstr_parts = []
        current = None

        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                continue
            if line.startswith("msgid "):
                current = "id"
                val = line[len("msgid "):]
                msgid_parts.append(val)
            elif line.startswith("msgstr "):
                current = "str"
                val = line[len("msgstr "):]
                msgstr_parts.append(val)
            elif line.startswith('"') and current == "id":
                msgid_parts.append(line)
            elif line.startswith('"') and current == "str":
                msgstr_parts.append(line)

        if msgid_parts and msgstr_parts:
            msgid = "".join(s.strip('"') for s in msgid_parts)
            msgstr = "".join(s.strip('"') for s in msgstr_parts)
            # Unescape
            msgid = msgid.replace("\\n", "\n").replace('\\"', '"')
            msgstr = msgstr.replace("\\n", "\n").replace('\\"', '"')
            if msgid and msgstr:
                entries[msgid.strip()] = msgstr.strip()

    return entries


def apply_translations(md_path, translations, dry_run=False):
    """Apply translations to a markdown file."""
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    replaced_count = 0

    # Sort by length descending to replace longer matches first
    sorted_trans = sorted(translations.items(), key=lambda x: len(x[0]), reverse=True)

    for eng, zh in sorted_trans:
        if eng in content:
            content = content.replace(eng, zh, 1)
            replaced_count += 1

    if replaced_count > 0:
        if dry_run:
            print(f"  [DRY-RUN] Would replace {replaced_count} segments in {md_path}")
        else:
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  Replaced {replaced_count} segments in {md_path}")
    else:
        print(f"  No matches found in {md_path}")

    return replaced_count


def main():
    dry_run = "--dry-run" in sys.argv
    total_replaced = 0

    for part in PARTS:
        po_dir = os.path.join(LOCALE_DIR, part)
        md_dir = os.path.join(SOURCE_DIR, part)

        if not os.path.isdir(po_dir):
            print(f"SKIP: {po_dir} not found")
            continue

        for po_file in sorted(glob.glob(os.path.join(po_dir, "*.po"))):
            basename = os.path.basename(po_file).replace(".po", ".md")
            md_file = os.path.join(md_dir, basename)

            if not os.path.isfile(md_file):
                print(f"SKIP: {md_file} not found for {po_file}")
                continue

            print(f"\nProcessing {basename} in {part}:")
            translations = parse_po(po_file)
            print(f"  Found {len(translations)} translated segments in .po")

            count = apply_translations(md_file, translations, dry_run)
            total_replaced += count

    print(f"\n{'[DRY-RUN] ' if dry_run else ''}Total segments replaced: {total_replaced}")


if __name__ == "__main__":
    main()
