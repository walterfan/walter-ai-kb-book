"""Sphinx configuration for the book.

"Use AI to build a knowledge base for a software project"

Kept deliberately minimal and self-contained so that the book builds from a
clean Python venv with only the packages listed in requirements.txt.

Language strategy: English is the source of truth; zh_CN is maintained via
sphinx-intl gettext catalogs under locale/zh_CN/LC_MESSAGES/.
"""

from __future__ import annotations

import datetime
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "_tools"))

# -- Project information -----------------------------------------------------

project = "Use AI to build a knowledge base for a software project"
author = "Walter (Yamin) Fan"
copyright_year = datetime.datetime.now().year
project_copyright = f"{copyright_year}, {author}"
release = "0.1.0-draft"
version = "0.1"

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",
    "sphinxcontrib.bibtex",
    "sphinxcontrib.mermaid",
    "sphinx.ext.todo",
    "sphinx.ext.githubpages",
]

# MyST feature flags used throughout the book
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]
myst_heading_anchors = 4
myst_linkify_fuzzy_links = False
myst_dmath_double_inline = True

source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

master_doc = "index"

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".venv",
    "sources",
    "examples",
    "locale",
    "_tools",
]

language = os.environ.get("BOOK_LANG", "en")
locale_dirs = ["locale/"]
gettext_compact = False
gettext_uuid = True
gettext_additional_targets = ["image"]

# -- Bibliography (sphinxcontrib-bibtex) -------------------------------------

bibtex_bibfiles = ["references.bib"]
bibtex_default_style = "plain"
bibtex_reference_style = "author_year"

# -- HTML output -------------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = project
html_short_title = "AI + KB for Software"
html_show_sourcelink = False
html_copy_source = False
html_last_updated_fmt = "%Y-%m-%d"

html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
    "titles_only": False,
    "sticky_navigation": True,
    "prev_next_buttons_location": "both",
    "style_external_links": True,
}

# -- Language switcher -------------------------------------------------------
#
# Consumed by _templates/layout.html. Each entry declares:
#   code  : Sphinx language code (matches the ``language`` setting)
#   label : human-readable name rendered in the switcher
#   dir   : per-language output directory under ``_build/html/``
#
# The build is expected to produce ``_build/html/en/`` and ``_build/html/zh/``;
# see the book-html-en / book-html-zh targets in the top-level Makefile.
html_context = {
    "available_languages": [
        {"code": "en", "label": "English", "dir": "en"},
        {"code": "zh_CN", "label": "中文", "dir": "zh"},
    ],
}

# -- LaTeX / PDF output ------------------------------------------------------

latex_engine = "xelatex"
latex_elements = {
    "papersize": "a4paper",
    "pointsize": "11pt",
    "preamble": r"""
\usepackage{fontspec}
\usepackage{xeCJK}
""",
    "figure_align": "H",
}
latex_documents = [
    (
        master_doc,
        "ai-kb-for-software.tex",
        project,
        author,
        "manual",
    ),
]

# -- Mermaid -----------------------------------------------------------------

mermaid_output_format = "raw"

# -- Todo extension ----------------------------------------------------------

todo_include_todos = True

# -- Suppression of noisy warnings during draft phase ------------------------
#
# - myst.header:        we allow non-sequential heading levels in stubs
# - myst.xref_missing:  draft cross-refs will resolve as chapters fill in
# - bibtex.duplicate_*: sphinxcontrib-bibtex re-labels the same keys across
#                       multiple per-chapter ``bibliography`` directives; the
#                       warnings are benign when each chapter uses its own
#                       ``:labelprefix:`` or ``author_year`` style.

suppress_warnings = [
    "myst.header",
    "myst.xref_missing",
    "bibtex.duplicate_label",
    "bibtex.duplicate_citation",
]

# -- MyST H1 translation hook ------------------------------------------------
#
# MyST-parser turns the first ``# Heading`` into a title node that Sphinx's
# gettext i18n transform does not translate — h2 and below translate fine,
# but the page title stays in English. We fix it by consulting the compiled
# gettext catalog at ``doctree-resolved`` time and swapping the title text
# if a translation exists.

from docutils import nodes  # noqa: E402


def _translate_titles(app, doctree, docname):
    if app.config.language in (None, "", "en"):
        return
    try:
        import gettext as _gettext

        translator = _gettext.translation(
            domain=docname,
            localedir=str(HERE / "locale"),
            languages=[app.config.language],
            fallback=True,
        )
    except Exception:
        return

    for title_node in doctree.traverse(nodes.title):
        original = title_node.astext()
        if not original:
            continue
        translated = translator.gettext(original)
        if translated and translated != original:
            title_node.clear()
            title_node += nodes.Text(translated)


def setup(app):
    app.connect("doctree-resolved", _translate_titles)
    return {
        "version": release,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
