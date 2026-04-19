#!/usr/bin/env python3
"""Apply a Chinese translations dict to a Sphinx gettext .po catalog.

This is the bilingual pipeline's authoring helper. It takes a Python module
that defines a TRANSLATIONS dict mapping msgid -> msgstr, loads the matching
.po file under book/locale/zh_CN/LC_MESSAGES/, writes translations into the
active (non-obsolete) entries, and reports anything missing or extra.

Usage
-----

    poetry run python book/_tools/translate_po.py \\
        book/_tools/translations/ch02-ir-rag-primer.zh.py

The translations module must define:

    TRANSLATIONS: dict[str, str]  # msgid -> msgstr (Chinese)
    PO_PATH:      str             # path relative to book/locale/zh_CN/LC_MESSAGES/

Behaviour
---------

- Only active (non-obsolete) msgids are considered; obsolete entries are
  left untouched.
- msgids not present in TRANSLATIONS are listed on stderr and left
  untranslated; msgstrs in TRANSLATIONS that do not match any msgid are
  listed on stderr as warnings. Neither is a hard error — the helper is
  meant to be run iteratively during translation authoring.
- After writing, the script re-runs the .mo compilation step that
  ``sphinx-intl build`` would perform, so ``make book-html-zh`` picks up
  the new translations on the next build.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

try:
    import polib
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "polib is required. Install with: poetry install\n"
    )
    sys.exit(2)

BOOK_ROOT = Path(__file__).resolve().parent.parent
LOCALE_ROOT = BOOK_ROOT / "locale" / "zh_CN" / "LC_MESSAGES"


def _load_translations_module(module_path: Path):
    spec = importlib.util.spec_from_file_location(
        "translations_module", module_path
    )
    if spec is None or spec.loader is None:  # pragma: no cover
        raise RuntimeError(f"Could not load {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def apply_translations(module_path: Path) -> int:
    module = _load_translations_module(module_path)

    translations: dict[str, str] = getattr(module, "TRANSLATIONS", None)
    po_rel: str = getattr(module, "PO_PATH", None)
    if translations is None or po_rel is None:
        sys.stderr.write(
            f"{module_path}: must define TRANSLATIONS (dict) and PO_PATH (str)\n"
        )
        return 2

    po_path = LOCALE_ROOT / po_rel
    if not po_path.exists():
        sys.stderr.write(f"Catalog not found: {po_path}\n")
        return 2

    po = polib.pofile(str(po_path))

    active = [e for e in po if not e.obsolete]
    active_msgids = {e.msgid for e in active}
    translated = 0
    untranslated: list[str] = []
    for entry in active:
        msgstr = translations.get(entry.msgid)
        if msgstr:
            entry.msgstr = msgstr
            # When sphinx-intl update runs, it may carry over a stale
            # translation from a similar msgid and flag it `fuzzy`.
            # Writing a fresh msgstr means we have reviewed it, so drop
            # the fuzzy flag to promote the entry to "translated".
            if "fuzzy" in entry.flags:
                entry.flags.remove("fuzzy")
            translated += 1
        elif not entry.msgstr:
            untranslated.append(entry.msgid)

    extra = [
        msgid
        for msgid in translations
        if msgid not in active_msgids
    ]

    po.save(str(po_path))

    print(
        f"{po_rel}: translated {translated}/{len(active)} active msgids "
        f"({len(untranslated)} remaining, {len(extra)} stale in dict)"
    )
    if untranslated:
        print("\n  Missing translations (first 10):", file=sys.stderr)
        for msgid in untranslated[:10]:
            preview = msgid.replace("\n", " ")[:100]
            print(f"    - {preview}", file=sys.stderr)
    if extra:
        print("\n  Stale keys in TRANSLATIONS dict (first 10):", file=sys.stderr)
        for msgid in extra[:10]:
            preview = msgid.replace("\n", " ")[:100]
            print(f"    - {preview}", file=sys.stderr)

    mo_path = po_path.with_suffix(".mo")
    po.save_as_mofile(str(mo_path))
    print(f"  Compiled: {mo_path.relative_to(BOOK_ROOT)}")

    return 0


def main() -> int:
    if len(sys.argv) < 2:
        sys.stderr.write(
            "Usage: translate_po.py <translations_module.py> [more_modules...]\n"
        )
        return 2
    exit_code = 0
    for arg in sys.argv[1:]:
        path = Path(arg).resolve()
        rc = apply_translations(path)
        if rc != 0:
            exit_code = rc
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
