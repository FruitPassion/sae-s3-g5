#!/bin/bash

set -e

BASE_DIR="app"
css_files=$(find $BASE_DIR -type f -name "*.css")
js_files=$(find $BASE_DIR -type f -name "*.js")
html_files=$(find $BASE_DIR -type f -name "*.html")

: "${VIRTUAL_ENV?Python virtual env must be active}"

echo "Executing black..." && black $BASE_DIR
echo "Executing isort..." && isort $BASE_DIR
echo "Executing flake8..." && flake8 $BASE_DIR --exclude "app/tests/*","app/migrations/*"
echo "Executing DjangoLinter..." && djlint $html_files --lint
echo "Executing JS-Beautifier..." && js-beautify $js_files
echo "Executing CSS-Beautifier..." && css-beautify -r $css_files
echo "Executing DJFormater..." && djlint $html_files --quiet --reformat