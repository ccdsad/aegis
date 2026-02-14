echo "ruff check --config ruff.toml --output-format concise --fix app"
ruff check --config ruff.toml --output-format concise --fix app
echo ""

echo "mypy --config-file mypy.ini --python-version 3.13 --install-types --non-interactive --show-error-context --show-column-numbers --pretty app"
mypy --config-file mypy.ini --python-version 3.13 --install-types --non-interactive --show-error-context --show-column-numbers --pretty app
echo ""

echo "ruff format --config ruff.toml app tests"
ruff format --config ruff.toml app tests
