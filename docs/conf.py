# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from pathlib import Path

import django

sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"

django.setup()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Pelican frontend"
copyright = "2020, Open Contracting Partnership"
author = "Open Contracting Partnership"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
# Georg Leonhart Huth, George Edwards, Mark Catesby & Johann Michael Seligmann,
# "Recueil de divers oiseaux étrangers et peu communs" (1771-1772).
# Digitized by the Biodiversity Heritage Library (https://doi.org/10.5962/bhl.title.65000),
# courtesy of Smithsonian Libraries and Archives. Public domain. https://flic.kr/p/2k38JRw
html_logo = "_static/logo.jpg"
html_additional_pages = {
    "reference/redoc": "redoc.html",
    "reference/swagger-ui": "swagger-ui.html",
}

# -- Extension configuration -------------------------------------------------

autodoc_default_options = {
    "members": None,
    "member-order": "bysource",
}
autodoc_typehints = "description"

extlinks = {
    "issue": ("https://github.com/open-contracting/pelican-frontend/issues/%s", "#%s"),
    "commit": ("https://github.com/open-contracting/pelican-frontend/commit/%s", "%s"),
    "compare": ("https://github.com/open-contracting/pelican-frontend/compare/%s", "%s"),
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
