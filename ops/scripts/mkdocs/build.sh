#!/bin/bash
# peltak:
#   about: Build documentation
set -e

DOCS_DIST_DIR="dist"

mkdocs build -f docs-ng/mkdocs.yaml --site-dir ${DOCS_DIST_DIR}
