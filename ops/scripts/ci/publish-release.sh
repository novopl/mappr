# peltak:
#   about: Tag current commit and create GitHub release

# Generate release notes (changelog)
poetry run peltak version --porcelain > ./RELEASE_VERSION
git log -1 --pretty=%B | tee ./RELEASE_NOTES

# Build release files and create GitHub release
poetry build
gh release create \
  --repo "novopl/mappr" \
  --title "v$(cat ./RELEASE_VERSION)" \
  --notes "$(cat ./RELEASE_NOTES)" \
  "v$(cat ./RELEASE_VERSION)" \
  dist/mappr-$(cat ./RELEASE_VERSION)-py3-none-any.whl \
  dist/mappr-$(cat ./RELEASE_VERSION).tar.gz

rm RELEASE_NOTES
rm RELEASE_VERSION
rm -rf dist
