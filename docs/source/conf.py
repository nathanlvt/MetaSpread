import sys
import os

sys.path.insert(0, os.path.abspath('../..'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'MetaSpread'
copyright = '2024, Alfredo Hernandez-Inostroza'
author = 'Alfredo Hernandez-Inostroza'
release = '2024.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc', 
    'sphinx.ext.autosummary',
    'sphinxcontrib.bibtex',
    'sphinx.ext.mathjax',
    'sphinx_search.extension',
   ]

bibtex_bibfiles = ['refs.bib']
autosummary_generate = True  # Turn on sphinx.ext.autosummary
# autodoc_mock_imports = ["matplotlib","Mesa","numpy","pandas","pynput","opencv_python"]


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


#math

mathjax_path = 'https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS-MML_HTMLorMML'

#figure numbers
numfig = True


#math equations numbers
math_numfig = True