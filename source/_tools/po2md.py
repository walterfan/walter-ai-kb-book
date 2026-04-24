#!/usr/bin/env python3
"""
Rebuild markdown files using translations from .po files.

Strategy: parse .po to get (line_number, msgid, msgstr) triples.
For each .md file, walk through it and replace English paragraphs
with their Chinese translations from the .po file, preserving
Sphinx directives, code blocks, frontmatter, and mermaid diagrams.

Usage:
    python3 po2md.py [--dry-run]
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


def parse_po_entries(po_path):
    """Parse a .po file, return list of (line_num, msgid, msgstr) sorted by line_num."""
    with open(po_path, "r", encoding="utf-8") as f:
        content = f.read()

    entries = []
    blocks = re.split(r"\n\n+", content)

    for block in blocks:
        lines = block.strip().split("\n")
        if not lines:
            continue

        line_num = None
        msgid_parts = []
        msgstr_parts = []
        current = None

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("#:") and line_num is None:
                m = re.search(r"\.md:(\d+)", stripped)
                if m:
                    line_num = int(m.group(1))
            if stripped.startswith("#"):
                continue
            if stripped.startswith("msgid "):
                current = "id"
                val = stripped[len("msgid "):]
                msgid_parts.append(val)
            elif stripped.startswith("msgstr "):
                current = "str"
                val = stripped[len("msgstr "):]
                msgstr_parts.append(val)
            elif stripped.startswith('"') and current == "id":
                msgid_parts.append(stripped)
            elif stripped.startswith('"') and current == "str":
                msgstr_parts.append(stripped)

        if msgid_parts and msgstr_parts and line_num is not None:
            msgid = "".join(s.strip('"') for s in msgid_parts)
            msgstr = "".join(s.strip('"') for s in msgstr_parts)
            msgid = msgid.replace("\\n", "\n").replace('\\"', '"').replace("\\\\", "\\")
            msgstr = msgstr.replace("\\n", "\n").replace('\\"', '"').replace("\\\\", "\\")
            if msgid.strip() and msgstr.strip():
                entries.append((line_num, msgid.strip(), msgstr.strip()))

    entries.sort(key=lambda x: x[0])
    return entries


def normalize_text(text):
    """Normalize whitespace for comparison."""
    return re.sub(r'\s+', ' ', text).strip()


def rebuild_md(md_path, entries, dry_run=False):
    """Rebuild a markdown file using .po translations."""
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Build a lookup: normalized_msgid -> msgstr
    lookup = {}
    for line_num, msgid, msgstr in entries:
        key = normalize_text(msgid)
        lookup[key] = msgstr

    result = []
    i = 0
    in_frontmatter = False
    in_code_block = False
    in_directive = False
    replaced = 0
    total_entries = len(entries)

    while i < len(lines):
        line = lines[i]

        # Handle frontmatter: translate title field
        if i == 0 and line.strip() == "---":
            in_frontmatter = True
            result.append(line)
            i += 1
            while i < len(lines):
                line = lines[i]
                if line.strip() == "---" and in_frontmatter:
                    in_frontmatter = False
                    result.append(line)
                    i += 1
                    break
                # Translate title in frontmatter
                if line.startswith("title:"):
                    title_val = line.split(":", 1)[1].strip().strip('"').strip("'")
                    norm_title = normalize_text(title_val)
                    if norm_title in lookup:
                        result.append(f'title: "{lookup[norm_title]}"\n')
                        replaced += 1
                    else:
                        result.append(line)
                else:
                    result.append(line)
                i += 1
            continue

        # Handle code blocks (``` ... ```)
        if line.strip().startswith("```") and not in_code_block:
            in_code_block = True
            result.append(line)
            i += 1
            while i < len(lines):
                result.append(lines[i])
                if lines[i].strip().startswith("```") and lines[i].strip() != line.strip():
                    in_code_block = False
                    i += 1
                    break
                if lines[i].strip() == "```":
                    in_code_block = False
                    i += 1
                    break
                i += 1
            continue

        # Handle Sphinx directives (literalinclude, bibliography, toctree, etc.)
        if re.match(r'\s*```\{', line):
            result.append(line)
            i += 1
            # Find end of directive block
            while i < len(lines):
                result.append(lines[i])
                if lines[i].strip() == "```":
                    i += 1
                    break
                i += 1
            continue

        # Handle markdown headings
        heading_match = re.match(r'^(#+)\s+(.+)$', line.strip())
        if heading_match:
            level = heading_match.group(1)
            heading_text = heading_match.group(2).strip()
            norm_heading = normalize_text(heading_text)
            if norm_heading in lookup:
                result.append(f"{level} {lookup[norm_heading]}\n")
                replaced += 1
            else:
                result.append(line)
            i += 1
            continue

        # Handle table lines (|...|...|)
        if line.strip().startswith("|"):
            # Try to match the whole line
            cell_texts = [c.strip() for c in line.strip().strip("|").split("|")]
            any_translated = False
            new_cells = []
            for cell in cell_texts:
                norm_cell = normalize_text(cell)
                if norm_cell in lookup:
                    new_cells.append(lookup[norm_cell])
                    any_translated = True
                else:
                    new_cells.append(cell)
            if any_translated:
                result.append("| " + " | ".join(new_cells) + " |\n")
                replaced += 1
            else:
                result.append(line)
            i += 1
            continue

        # Handle blank lines
        if line.strip() == "":
            result.append(line)
            i += 1
            continue

        # Handle regular paragraphs: collect consecutive non-blank, non-special lines
        para_lines = []
        para_start = i
        while i < len(lines):
            l = lines[i]
            if l.strip() == "":
                break
            if l.strip().startswith("#"):
                break
            if l.strip().startswith("```"):
                break
            if l.strip().startswith("|") and para_lines:
                break
            if re.match(r'^\d+\.\s+', l.strip()) and not para_lines:
                pass  # start of numbered list item
            if l.strip().startswith("- ") and not para_lines:
                pass  # start of list item
            para_lines.append(l)
            i += 1

        if para_lines:
            para_text = "".join(para_lines)
            norm_para = normalize_text(para_text)

            if norm_para in lookup:
                result.append(lookup[norm_para] + "\n")
                replaced += 1
            else:
                # Try to match individual list items
                matched_any = False
                for pl in para_lines:
                    pl_text = pl.strip()
                    # Strip leading list markers for lookup
                    stripped_item = re.sub(r'^[\d]+\.\s+', '', pl_text)
                    stripped_item = re.sub(r'^[-*]\s+', '', stripped_item)
                    norm_item = normalize_text(stripped_item)

                    if norm_item in lookup:
                        # Preserve the list marker
                        marker_match = re.match(r'^(\s*(?:[\d]+\.\s+|[-*]\s+))', pl)
                        marker = marker_match.group(1) if marker_match else ""
                        result.append(f"{marker}{lookup[norm_item]}\n")
                        replaced += 1
                        matched_any = True
                    else:
                        result.append(pl)
                if not matched_any:
                    pass  # already appended original lines

    if dry_run:
        print(f"  [DRY-RUN] Would replace {replaced}/{total_entries} segments")
    else:
        with open(md_path, "w", encoding="utf-8") as f:
            f.writelines(result)
        print(f"  Replaced {replaced}/{total_entries} translated segments")

    return replaced


def main():
    dry_run = "--dry-run" in sys.argv
    total_replaced = 0
    total_entries = 0

    for part in PARTS:
        po_dir = os.path.join(LOCALE_DIR, part)
        md_dir = os.path.join(SOURCE_DIR, part)

        if not os.path.isdir(po_dir):
            continue

        for po_file in sorted(glob.glob(os.path.join(po_dir, "*.po"))):
            basename = os.path.basename(po_file).replace(".po", ".md")
            md_file = os.path.join(md_dir, basename)

            if not os.path.isfile(md_file):
                continue

            print(f"\n{part}/{basename}:")
            entries = parse_po_entries(po_file)
            total_entries += len(entries)
            print(f"  {len(entries)} translated entries in .po")

            count = rebuild_md(md_file, entries, dry_run)
            total_replaced += count

    print(f"\n{'[DRY-RUN] ' if dry_run else ''}Total: {total_replaced}/{total_entries} segments applied")


if __name__ == "__main__":
    main()
