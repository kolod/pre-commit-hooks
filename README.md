# pre-commit hooks

This repo defines Git pre-commit hooks intended for use with [pre-commit](http://pre-commit.com/). The currently
supported hooks are:

* **coverage-badge**: Automatically build coverage badge by [shields.io](https://shields.io/).

## General Usage

In your repository, add a file called `.pre-commit-config.yaml` with the following contents:
```yaml
repos:
  - repo: https://github.com/kolod/pre-commit-hooks
    rev: <VERSION> # Get the latest from: https://github.com/kolod/pre-commit-hooks/releases
    hooks:
      - id: coverage-badge
```
Next, have every developer:
1. Install [pre-commit](http://pre-commit.com/). E.g. `brew install pre-commit`.
2. Run `pre-commit install` in the repo.

For start checks manually run `pre-commit run --all-files`

## Hooks

### coverage-badge hook
- --input - path to the coverage database
- --output - path where the coverage badge will be placed
- --style - optional badge style `{ plastic | flat | flat-square | for-the-badge | social }`
- --logo - optional badge logo: see [simpleicons.org](https://simpleicons.org/) for names of icons

```yaml
repos:
  - repo: https://github.com/kolod/pre-commit-hooks
    rev: <VERSION> # Get the latest from: https://github.com/kolod/pre-commit-hooks/releases
    hooks:
    - id: coverage-badge
      args: [
        --input=./.coverage,
        --output=./images/coverage.svg,
        --style=flat,
        --logo=codecov
      ]
```

## Example: Enforcing in CI

If you'd like to enforce all your hooks, you can configure your CI build to fail if the code doesn't pass checks by
adding the following to your build scripts:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

If all the hooks pass, the last command will exit with an exit code of 0. If any of the hooks make changes (e.g.,
because files are not formatted), the last command will exit with a code of 1, causing the build to fail.

## Build
* Install [python >= 3.7](https://www.python.org/downloads/).
* Install [poetry](https://python-poetry.org/).

### Commands
* Install git pre-commit hooks: </br>
`poetry run pre-commit install`
* Run pre-commit hooks manually: </br>
`poetry run pre-commit run --all-files`

## License
This code is released under the MIT license. Please see [LICENSE](LICENSE) for more details.
