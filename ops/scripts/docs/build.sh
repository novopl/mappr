#!/bin/bash
# peltak:
#   about: Build documentation
set -e

DOCS_DIST_DIR="dist"

mkdocs build -f docs/mkdocs.yaml --site-dir ${DOCS_DIST_DIR}
