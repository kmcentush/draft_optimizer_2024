# Fantasy Football Draft Optimizer - 2024

## Features:
- Data Scraping
  - Player metadata and weekly point projections from Sleeper
- Draft Recommendations
  - Sync draft state from Sleeper leagues
  - Use convex optimization to recommend an optimal roster
    - Obj*ective function: maximize the minimum points your team will score each week

## Installation
1. Install [uv](https://github.com/astral-sh/uv) for your system.
2. Install [make](https://www.gnu.org/software/make/) for your system.
3. Clone this repository and `cd` into it.
4. Run `uv venv --python 3.12` to initialize a virtual environment with Python 3.12.
5. Run `make prd_install` to install all requirements exactly as compiled in the `requirements.txt` file.
   1. If you want to update any dependencies, run `make install` to install all requirements, or `make dev_install` to 
   install all requirements plus additional dependencies required for code formatting, tests, etc.
   2. Then run `make prd_compile` to regenerate the universal `requirements.txt` file.

## Formatting and Tests
1. Follow the `Installation` section above, being sure to use `make dev_install` instead of `make prd_install`.
2. Run `make format` to lint and format all code using `ruff`, then check types using `pyright`.
3. Run `make pytest` to run tests and output a code coverage report. At this time, there is not full code coverage.

## Version Bumping
- Edit `__version__` in `src/football/__init__.py`
