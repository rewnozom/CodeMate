# Project Details

# Table of Contents
- [..\requirements\base.txt](#-requirements-basetxt)
- [..\requirements\dev.txt](#-requirements-devtxt)
- [..\requirements\prod.txt](#-requirements-prodtxt)
- [..\requirements\__init__.py](#-requirements-__init__py)


# ..\..\requirements\base.txt
## File: ..\..\requirements\base.txt

```txt
# ..\..\requirements\base.txt
# requirements/base.txt
pyside6>=6.0.0
anthropic>=0.3.0
openai>=1.0.0
python-dotenv>=0.19.0
rich>=10.0.0
typer>=0.4.0
pyyaml>=6.0.0
psutil>=5.8.0
watchdog>=2.1.0
transformers>=4.30.0
numpy>=1.21.0
pandas>=1.3.0
pytest>=7.0.0
black>=22.0.0
flake8>=4.0.0
```

---

# ..\..\requirements\dev.txt
## File: ..\..\requirements\dev.txt

```txt
# ..\..\requirements\dev.txt
# requirements/dev.txt
-r base.txt
pytest-cov>=2.12.0
pytest-asyncio>=0.18.0
pytest-mock>=3.6.0
black>=22.0.0
flake8>=4.0.0
mypy>=0.910
isort>=5.9.0
pre-commit>=2.15.0
coverage>=6.2
```

---

# ..\..\requirements\prod.txt
## File: ..\..\requirements\prod.txt

```txt
# ..\..\requirements\prod.txt
# requirements/prod.txt
-r base.txt
gunicorn>=20.1.0
uvicorn>=0.15.0
```

---

# ..\..\requirements\__init__.py
## File: ..\..\requirements\__init__.py

```py
# ..\..\requirements\__init__.py
# Auto-generated __init__.py file

```

---

