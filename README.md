# lifedb


[![pypi](https://img.shields.io/pypi/v/lifedb.svg)](https://pypi.org/project/lifedb/)
[![python](https://img.shields.io/pypi/pyversions/lifedb.svg)](https://pypi.org/project/lifedb/)
[![Build Status](https://github.com/grchristensen/lifedb/actions/workflows/dev.yml/badge.svg)](https://github.com/grchristensen/lifedb/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/grchristensen/lifedb/branch/main/graphs/badge.svg)](https://codecov.io/github/grchristensen/lifedb)



Python code for processing data from finance/health/journaling/etc. apps and consolidating it into one database for monitoring aspect of one's personal life.


* Documentation: <https://grchristensen.github.io/lifedb>
* GitHub: <https://github.com/grchristensen/lifedb>
* PyPI: <https://pypi.org/project/lifedb/>
* Free software: Apache-2.0


## Table of Contents

- [Project Organization](#project-organization)
- [Setting up a Development Environment](#setting-up-a-development-environment)
- [Contacting](#contacting)
- [Other Information](#other-information)
- [Credits](#credits)

## Project Organization

```
├── docs               <- Project documentation (mkdocs).
├── lifedb               <- Package code.
├── tests              <- Package code.
├── README.md          <- The top-level README for developers using this project.
└── CONTRIBUTING.md    <- Contributing guidelines for this project.
```

The contents of `lifedb/` are

```
├── example_module1    <- Description of module contents.
├── example_module2    <- Description of module contents.
└── example_module3    <- Description of module contents.
```

--------

## Setting up a Development Environment

To test the package in development, run the following to grab necessary dependencies:

```bash
pip install -e .[test,dev,doc] poetry
```

You may want to create a virtual environment for testing this library first. All tests (including formatting) can be ran by using `tox`. There are also pre-commit hooks that will run formatting checks.

## Contacting

To ask questions or request changes to this project, please ...

## Other Information

- [Contributing](CONTRIBUTING.md)

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.
