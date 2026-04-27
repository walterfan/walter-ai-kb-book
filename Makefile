.PHONY: help setup check check-redaction build serve clean pdf \
        html refresh-excerpts check-excerpts \
        book-setup book-check book-check-redaction book-build book-serve \
        book-clean book-pdf book-html \
        book-refresh-excerpts book-check-excerpts

# ── Layout ───────────────────────────────────────────────────────────
#
# The book sources live under ./source/ (self-contained Sphinx project:
# conf.py, references.bib, _tools/, _templates/, _static/).
# All build artifacts go to ./source/_build/.

BOOK_DIR       := source
BOOK_BUILD_DIR := $(BOOK_DIR)/_build
BOOK_PORT      ?= 8800

# Poetry drives the Sphinx toolchain. Override with e.g. `make build POETRY=poetry2`.
# Unexport any stale VIRTUAL_ENV the caller's shell may leak in (leftover
# `source .venv/bin/activate` from a different project would otherwise confuse
# Poetry).
unexport VIRTUAL_ENV
unexport VIRTUAL_ENV_PROMPT
unexport POETRY_ACTIVE

POETRY         ?= poetry
POETRY_RUN     := $(POETRY) run
PYTHON         ?= $(POETRY_RUN) python
# Prefer module invocation over console-script wrappers so a moved/renamed repo
# does not keep stale shebangs inside .venv/bin/.
SPHINXBUILD    ?= $(PYTHON) -m sphinx

# Redaction scan (keeps internal-URL / product / ticket / private-project
# invariants out of the public book). See README for the rationale.
REDACTION_EXCLUDE := -g '!**/_tools/**' -g '!**/_build/**' \
                     -g '!**/sources/**' -g '!**/.venv/**'

# ── Setup ────────────────────────────────────────────────────────────

setup: ## Install the Sphinx toolchain via Poetry (MyST, bibtex, mermaid)
	$(POETRY) install --no-root

# ── Content checks ───────────────────────────────────────────────────

check: ## Validate frontmatter, blog-quote, and PKB-skill non-copy policies
	$(PYTHON) $(BOOK_DIR)/_tools/check_frontmatter.py
	$(PYTHON) $(BOOK_DIR)/_tools/check_blog_quotes.py
	$(PYTHON) $(BOOK_DIR)/_tools/check_pkb_quotes.py

check-redaction: ## Scan source+references.bib for internal URLs / product / ticket / private project-name leaks
	@echo "→ internal URL / product / CLI scan"
	@! rg -i -n $(REDACTION_EXCLUDE) "(docs\.zoom\.us|dg01docs\.zoom\.us|git\.zoom\.us|git\.ops\.corp\.zoom\.us|qa\.zoomdev\.us|jenkins\.zoom\.us|jenkins\.client\.corp\.zoom\.us|artifacts\.corp\.zoom\.us|eng\.corp\.zoom\.com|new-dayone\.zoomdev\.us|zoomvideo\.atlassian\.net|AgentBox|agentbox\.yaml|DayOne|TestZoom|Async MQ|Async Pilot|AI Hub|DevHelper|zcp-cli|mirrord-zcp|csms_tool|/PKB-|PKB_ROOT|zoom-dev-skills)" $(BOOK_DIR) || (echo "FAIL: internal reference leaked in source/" && exit 1)
	@echo "→ employer email domain scan"
	@! rg -i -n $(REDACTION_EXCLUDE) "[a-z0-9._+-]+@(zoom|corp\.zoom)\.(us|com)" $(BOOK_DIR) || (echo "FAIL: employer email leaked in source/" && exit 1)
	@echo "→ internal Jira ticket-key scan"
	@! rg -n $(REDACTION_EXCLUDE) "\b(ZOOM|ZCP|SEC|ZMS|SDK)-[0-9]{3,}" $(BOOK_DIR) || (echo "FAIL: internal Jira ticket leaked in source/" && exit 1)
	@echo "→ author's private project-name scan"
	@# Note: lazy-kb-wiki is the renamed prose-layer reference impl and is now
	@# allowed in source/ (it's intentionally a neutral, public name). Only the
	@# unreleased code-layer impl (lazy-ai-coder / internal/codekg) is still
	@# considered private and must not appear in source/.
	@! rg -n $(REDACTION_EXCLUDE) "(lazy-ai-coder|internal/codekg|\bCODEKG_[A-Z_]+)" $(BOOK_DIR) || (echo "FAIL: author's private project name leaked in source/ (use 'the code-layer reference implementation' instead)" && exit 1)
	@echo "OK — no redaction invariants triggered."

# ── Build ────────────────────────────────────────────────────────────

build: html ## Build the book to HTML (Chinese, under source/_build/html/)

html: check check-redaction ## Build Chinese HTML (source/_build/html/)
	$(SPHINXBUILD) -b html --keep-going \
	    $(BOOK_DIR) $(BOOK_BUILD_DIR)/html

serve: ## Serve the built book on http://localhost:$(BOOK_PORT)
	@if [ ! -d $(BOOK_BUILD_DIR)/html ]; then \
	  echo "No HTML build found. Run 'make build' first."; exit 1; \
	fi
	@echo "Serving book on http://localhost:$(BOOK_PORT) — Ctrl-C to stop"
	cd $(BOOK_BUILD_DIR)/html && $(PYTHON) -m http.server $(BOOK_PORT)

pdf: check ## Build the book to PDF via xelatex (requires a TeX distribution)
	$(SPHINXBUILD) -b latex $(BOOK_DIR) $(BOOK_BUILD_DIR)/latex
	$(MAKE) -C $(BOOK_BUILD_DIR)/latex all-pdf LATEXMKOPTS="-xelatex"
	@echo "PDF built: $(BOOK_BUILD_DIR)/latex/ai-kb-for-software.pdf"

# ── Excerpts ─────────────────────────────────────────────────────────

refresh-excerpts: ## Re-capture vendored code excerpts with fresh commit SHAs and provenance headers
	$(PYTHON) $(BOOK_DIR)/_tools/refresh_excerpts.py

check-excerpts: ## Fail if any vendored excerpt is out-of-date (used in CI)
	$(PYTHON) $(BOOK_DIR)/_tools/refresh_excerpts.py --check

# ── Clean ────────────────────────────────────────────────────────────

clean: ## Remove book build artifacts (keeps source/)
	rm -rf $(BOOK_BUILD_DIR)

# ── Back-compat aliases ──────────────────────────────────────────────
#
# The previous repo (lazy-kb-wiki, fka lazy-rabbit-wiki) exposed the same
# targets prefixed with `book-*`. Keep the aliases so muscle memory + existing
# CI snippets keep working. New docs and scripts should use the short names
# above.

book-setup:            setup
book-check:            check
book-check-redaction:  check-redaction
book-build:            build
book-serve:            serve
book-clean:            clean
book-pdf:              pdf
book-html:             html
book-refresh-excerpts: refresh-excerpts
book-check-excerpts:   check-excerpts

# ── Help ─────────────────────────────────────────────────────────────

help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
