# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
os.environ['_SPHINX'] = "1"
import ckipnlp as __about

def run_apidoc(_):
    from sphinx.ext.apidoc import main
    main(['-feTM', '-o', '_api', '../ckipnlp'])

def setup(app):
    app.connect('builder-inited', run_apidoc)


# -- Project information -----------------------------------------------------

project = __about.__title__
author = __about.__author_name__
copyright = __about.__copyright__

# The short X.Y version.
version = __about.__version__
# The full version, including alpha/beta/rc tags
release = 'v'+__about.__version__

# Master documentation
master_doc = 'index'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_rtype = False
todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_extra_path = ['../LICENSE']

# -- Settings of autodoc:-----------------------------------------------

autodoc_member_order = 'bysource'
