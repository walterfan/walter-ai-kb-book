"""Sphinx configuration for the book.

"Use AI to build a knowledge base for a software project"

Kept deliberately minimal and self-contained so that the book builds from a
clean Python venv with only the packages listed in pyproject.toml.

Language strategy: the Markdown source is written directly in Chinese
(with English technical terms retained). A single Sphinx build produces
the Chinese HTML output.
"""

from __future__ import annotations

import datetime
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "_tools"))

# -- Project information -----------------------------------------------------

project = "Use AI to build a knowledge base for a software project"
author = "Walter Fan"
copyright_year = datetime.datetime.now().year
project_copyright = f"AI 辅助创作 {copyright_year}, {author}"
copyright = project_copyright  # noqa: A001 — Sphinx requires this name
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
    "_tools",
]

language = "zh_CN"

# -- Bibliography (sphinxcontrib-bibtex) -------------------------------------

bibtex_bibfiles = ["references.bib"]
bibtex_default_style = "plain"
bibtex_reference_style = "author_year"

# -- HTML output -------------------------------------------------------------

html_theme = "sphinx_book_theme"
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
