#!/bin/bash

set -e

BASE_DIR="."
css_files=$(find . -type f -name "*.css" -not -path ".venv/*")
js_files=$(find . -type f -name "*.js" -not -path ".venv/*")
html_files=$(find . -type f -name "*.html" -not -path ".venv/*")

: "${VIRTUAL_ENV?Python virtual env must be active}"

echo "Executing black..." && black $BASE_DIR
echo "Executing isort..." && isort $BASE_DIR
echo "Executing flake8..." && flake8 $BASE_DIR --exclude ".venv/*","tests/*"
echo "Executing DjangoLinter..." && djlint $html_files --lint
echo "Executing JS-Beautifier..." && js-beautify $js_files
echo "Executing CSS-Beautifier..." && css-beautify -r $css_files
echo "Executing DJFormater..." && djlint $html_files --quiet --reformat