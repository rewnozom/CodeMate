# Project Details

# Table of Contents
- [..\CodeMate\.github\workflows\__init__.py](#-CodeMate-github-workflows-__init__py)
- [..\CodeMate\.github\workflows\main.yml](#-CodeMate-github-workflows-mainyml)


# ..\..\CodeMate\.github\workflows\__init__.py
## File: ..\..\CodeMate\.github\workflows\__init__.py

```py
# ..\..\CodeMate\.github\workflows\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\CodeMate\.github\workflows\main.yml
## File: ..\..\CodeMate\.github\workflows\main.yml

```yml
# ..\..\CodeMate\.github\workflows\main.yml
# .github/workflows/main.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, "3.10"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Cache pip packages
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('requirements/*.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements/dev.txt

    - name: Run linting
      run: |
        flake8 src tests
        black --check src tests
        isort --check-only src tests
        mypy src tests

    - name: Run tests
      run: |
        pytest tests/ -v --cov=src --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"

    - name: Build package
      run: |
        pip install build
        python -m build

    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: dist
        path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
    - uses: actions/download-artifact@v3
      with:
        name: dist
        path: dist/

    - name: Deploy to PyPI
      env:
        TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
        TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
      run: |
        pip install twine
        twine upload dist/*
```

---

