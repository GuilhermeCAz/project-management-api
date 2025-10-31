# Makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Custom targets for convenience
.PHONY: clean html livehtml

clean:
	rm -rf $(BUILDDIR)/*
	@echo "Build directory cleaned."

html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo ""
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

# Live reload with sphinx-autobuild (optional, requires sphinx-autobuild)
livehtml:
	@command -v sphinx-autobuild >/dev/null 2>&1 || { \
		echo >&2 "sphinx-autobuild is not installed. Install it with: pip install sphinx-autobuild"; \
		exit 1; \
	}
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

# Quick build and open in browser (Linux/macOS)
view: html
	@if command -v xdg-open >/dev/null 2>&1; then \
		xdg-open $(BUILDDIR)/html/index.html; \
	elif command -v open >/dev/null 2>&1; then \
		open $(BUILDDIR)/html/index.html; \
	else \
		echo "Please open $(BUILDDIR)/html/index.html in your browser"; \
	fi
