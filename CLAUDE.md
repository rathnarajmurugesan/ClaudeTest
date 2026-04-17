# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
py main.py

# Run tests
pytest

# Run a single test
pytest tests/test_main.py::test_main
```

## Architecture

This is a Python 3.12 project with a simple flat layout:

- `main.py` — entry point and application logic
- `tests/` — pytest test suite
- `requirements.txt` — runtime and dev dependencies
