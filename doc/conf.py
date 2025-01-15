# SPDX-License-Identifier: MIT

"""
Configuration file for the Sphinx documentation builder.
"""

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "facere-sensum"  # pylint: disable=invalid-name
copyright = "2023-2025 Serge Lunev. All Rights Reserved."  # pylint: disable=invalid-name,redefined-builtin
author = "Serge Lunev"  # pylint: disable=invalid-name

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"  # pylint: disable=invalid-name
html_static_path = ["_static"]
