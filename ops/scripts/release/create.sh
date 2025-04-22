# peltak:
#   root_cli: true
#   about: Create a version bump commit and tag it as release.
#   options:
#     - name: ['-t', '--type']
#       about: "Type of release to make: patch|minor|major. Defaults to 'patch'."
#       type: str
#       default: patch
#     - name: ['--no-push']
#       about: Push the release to GitHub.
#       is_flag: True
#   use:
#     - cprint
#     - header

echo "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

header "Creating <33>{{ opts.type }}<95> release"

uv run peltak version bump {{ opts.type }}
uv sync

header "Adding changed files to commit"
git add pyproject.toml uv.lock src/mappr/__init__.py


header "Creating the release message"
uv run peltak changelog > .RELEASE_CHANGELOG
echo "Release: v$(peltak version --porcelain)\n" > .RELEASE_COMMIT_MSG
uv run peltak changelog --title "" >> .RELEASE_COMMIT_MSG

header "Committing changes"
git commit -F .RELEASE_COMMIT_MSG

header "Tagging the release"
uv run  peltak git tag "v$(peltak version --porcelain)" -m "$(cat .RELEASE_CHANGELOG)"

{% if not opts.no_push %}
  header "Pushing to GitHub"
  git push origin master
  git push origin v$(peltak version --porcelain)
{% endif %}

header "Cleaning temporary files"
rm .RELEASE_CHANGELOG .RELEASE_COMMIT_MSG

cprint "<95>DONE"
echo "\n"
