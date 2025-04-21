# peltak:
#   about: Run all checks (types, pep8, code style)
#   options:
#     - name: ['--fix']
#       is_flag: true
#       about: Attempt to fix some of the failed checks (like isort).
#   files:
#     paths:
#       - src/mappr
#       - tests
#     include: '*.py'
#     use_gitignore: true
#   use:
#     - cprint
#     - header

# The weird {{ files | wrap_paths }} notation means the files will be collected
# by the script command and passed onto the 3rd party tool. This allows use
# to use the same command implementation for 'peltak check' and
# 'peltak run check-commit'.

echo "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

{% if not files %}
  cprint "<90>No relevant staged files - skipping lint..."
  exit 0
{% endif %}


header 'ruff'
time ruff check
ruff_ret=$?



header 'isort'
if type colordiff &> /dev/null; then
  # Prettify the isord diff with colordiff if it is installed.
  isort --check-only --diff src tests | colordiff
  isort_ret=$?
else
  isort --check-only --diff src tests
  isort_ret=$?
fi

header 'mypy'
dmypy status &> /dev/null
if [[ $? -ne 0 ]]; then
  echo "\x1b[90mStarting mypy daemon, as it is not running..."
  echo "This will take some time, but consecutive runs will be almost instant.\x1b[0m"

  time dmypy run
  mypy_ret=$?
else
  time dmypy check {{ files | wrap_paths }}
  mypy_ret=$?
fi


header 'done'

# Run everything first so we can see all errors on 1 run. Fail if any of the checks
# failed
if [[ $mypy_ret -ne 0 || $ruff_ret -ne 0 || $isort_ret -ne 0 ]]; then
  cprint "<91>FAILED"
  echo "\n"
  exit 1
else
  cprint "<92>SUCCESS"
  echo "\n"
fi



# {% if files %}
#   {{ 'mypy' | header }}
#   time mypy --config-file=ops/tools/mypy.ini {{ files | wrap_paths }}
#   mypy_ret=$?
#
#   {{ 'pycodestyle' | header }}
#   time pycodestyle  --config=ops/tools/pycodestyle.ini {{ files | wrap_paths }};
#   pycodestyle_ret=$?
#
#   {{ 'flake8' | header }}
#   time flake8 --config=ops/tools/flake8.ini {{ files | wrap_paths }}
#   flake8_ret=$?
#
#   {{ 'isort' | header }}
#   isort_log=$(time isort \
#   --settings-file=ops/tools/isort.ini \
#   {% if not opts.fix %} --check-only --diff \{% endif %} \
#   {{ files | wrap_paths }} \
#   )
#   isort_ret=$?
#
#   echo "$isort_log" {%if not opts.fix %} | colordiff{% endif %}
#
#   {{ 'done' | header }}
#
#   # Run everything first so we can see all errors on 1 run. Fail if any of the checks
#   # failed
#   if [[ $mypy_ret -ne 0 || $pycodestyle_ret -ne 0 || $flake8_ret -ne 0 || $isort_ret -ne 0 ]]; then
#   echo "\x1b[91mFAILED\x1b[0m"
#   exit 1
#   else
#   echo "\x1b[92mSUCCESS\x1b[0m"
#   fi
#
# {% else %}
#   {{ '<90>No relevant staged files - skipping lint...' | cprint }}
# {% endif %}
#
