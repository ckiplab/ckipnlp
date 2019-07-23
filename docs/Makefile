# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXBUILD     = _SPHINX=1 sphinx-build
SPHINXBUILDOPTS =
SPHINXAPI       = sphinx-apidoc
SPHINXAPIOPTS   =

DOCDIR     = .
BUILDDIR   = _build
APIDIR     = _api

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(DOCDIR)" "$(BUILDDIR)" $(SPHINXBUILDOPTS) $(O)

.PHONY: help Makefile api clean run

api:
	@$(SPHINXAPI) -feTM -o "$(APIDIR)" "../ckipnlp" $(SPHINXAPIOPTS)

clean: Makefile
	@$(SPHINXBUILD) -M $@ "$(DOCDIR)" "$(BUILDDIR)" $(SPHINXBUILDOPTS)
	@$(SPHINXBUILD) -M $@ "$(DOCDIR)" "$(APIDIR)"   $(SPHINXBUILDOPTS)

run:
	( cd _build/html/ && python3 -m http.server 8080 )

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXBUILDOPTS).
%: api Makefile
	@$(SPHINXBUILD) -M $@ "$(DOCDIR)" "$(BUILDDIR)" $(SPHINXBUILDOPTS) $(O)
