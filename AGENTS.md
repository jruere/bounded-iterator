# AGENTS.md

## Domain Context

Always read the README the first 50 lines of README.rst for high-level context.

## Environment

`devenv` is used to manage the environment, and project "tasks".
`devenv shell` is already active, there's no need for `devenv shell {command}`.
List tasks: `devenv --no-tui --quiet tasks list`
Run a task: `devenv --no-tui --quiet tasks run publish:clean 2>&1 >/dev/null`

## Coding

Never use recursion.

### Code style guidelines

`black` formats, and runs automatically. Do not run it.

### Validation

Every public interface implementation should validate the inputs using
assertions as a sort of sanity check. The assertion message must explain
the problem, and show the incorrect value.
This validation must be first in the function, as a separate paragraph.
Never validate types with code. Mypy will handle those.

### Type Annotations

Prefer type inference to explicit annotations.
When a concrete type is assigned to a variable, do not annotate the type.

## Testing

- `unittest` is the testing framework.
- Mirror the structure of the library in tests. E.g.: place all
`bounded_iterator` tests in `tests.test_bounded_iterator`
- List possible tests: `devenv --no-tui --quiet tasks list | rg test:`
- Type check: `mypy` (and less importantly, `pyright`)
- Lint: `ruff check *.py **/*.py`
- Run tests for a given Python version:

    devenv --no-tui --quiet tasks run test:py314

- Run tests for supported Python versions, `mypy`, `ruff`, formatters (do not
  truncate output):

    devenv --no-tui test 2>&1 | rg -v ' in \d| ignoring ' \
    ; echo EXITS:${PIPESTATUS[0]}

### Efficiency

1. Baseline: all tests for all versions once at start to capture pre-existing
   state.
2. Iterate fast: type-only change → `mypy` first; otherwise single interpreter,
   `test:py314`; single failure → that one `unittest` in isolation.
3. Verify: all tests for all versions at the end to double-check.

### Tests

Organize tests into 3 paragraphs: setup, execution, assertions.
Assign the type being tested to variable `subject`.
Name tests using BDD-like style. E.g.
`test_when_{scenario}_then_it_{expected outcome}`.

## Documentation

### Docstrings

Do not add redundant information. E.g. if a function has type annotations, do
not document the same information.
Type annotations are better than documentation, when containing the same info.

### Changelog (@CHANGES.txt)

When updating the changelog, include only changes that affect users or the
codebase's tested behavior:

- Code changes to the public API or behavior
- Bug fixes (prefix with "Bugfix:")
- Test additions/improvements
- Packaging changes that materially affect installation, such as replacing
  `setup.py` with `pyproject.toml`

Exclude development environment and incidental tooling noise:

- Cachix, devenv, Shippable, and other environment setup
- Pre-commit hooks, linters, and formatters
- Coverage configuration and dependency-only tooling changes
- Version bumps
