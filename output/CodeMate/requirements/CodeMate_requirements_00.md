# Project Details

# Table of Contents
- [..\CodeMate\requirements\__init__.py](#-CodeMate-requirements-__init__py)
- [..\CodeMate\requirements\base.txt](#-CodeMate-requirements-basetxt)
- [..\CodeMate\requirements\dev.txt](#-CodeMate-requirements-devtxt)
- [..\CodeMate\requirements\prod.txt](#-CodeMate-requirements-prodtxt)


# ..\..\CodeMate\requirements\__init__.py
## File: ..\..\CodeMate\requirements\__init__.py

```py
# ..\..\CodeMate\requirements\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\CodeMate\requirements\base.txt
## File: ..\..\CodeMate\requirements\base.txt

```txt
# ..\..\CodeMate\requirements\base.txt
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

# Added LLM dependencies
pydantic>=2.0.0
langchain>=0.1.0
langchain-anthropic>=0.1.0
langchain-openai>=0.1.0
langchain-groq>=0.1.0
groq>=0.1.0

# Added Core dependencies
asyncio>=3.4.3
aiofiles>=0.8.0
uvicorn>=0.15.0
prompt_toolkit>=3.0.0
pathlib>=1.0.1
```

---

# ..\..\CodeMate\requirements\dev.txt
## File: ..\..\CodeMate\requirements\dev.txt

```txt
# ..\..\CodeMate\requirements\dev.txt
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

# ..\..\CodeMate\requirements\prod.txt
## File: ..\..\CodeMate\requirements\prod.txt

```txt
# ..\..\CodeMate\requirements\prod.txt
# requirements/prod.txt
-r base.txt
gunicorn>=20.1.0
uvicorn>=0.15.0
```

---

