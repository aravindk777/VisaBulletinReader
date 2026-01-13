# Contributing to Visa Bulletin Reader

First off, thank you for considering contributing to Visa Bulletin Reader! It's people like you that make this tool better for everyone.

This project was started to help users easily track visa bulletin dates and to learn Python and web scraping. We welcome all contributions, from bug reports to new features.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancement](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Local Development Setup](#local-development-setup)
- [Style Guide](#style-guide)
  - [Python Style Guide](#python-style-guide)

## Code of Conduct

By participating in this project, you are expected to uphold our code of conduct. Please be respectful and professional in all interactions.

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please open an issue on GitHub. Include:
- A clear and descriptive title.
- Steps to reproduce the issue.
- Expected vs actual behavior.
- Any relevant logs or screenshots.

### Suggesting Enhancements

We are always looking for ways to improve! If you have an idea:
- Check if a similar enhancement has already been suggested.
- Open an issue with a detailed description of the proposed feature.
- Explain why this enhancement would be useful.

### Pull Requests

1. Fork the repository.
2. Create a new branch for your feature or fix (`git checkout -b feature/your-feature-name`).
3. Commit your changes with descriptive messages.
4. Push to your branch (`git push origin feature/your-feature-name`).
5. Open a Pull Request against the `main` branch.

## Local Development Setup

To set up the project locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/VisaBulletinReader.git
   cd VisaBulletinReader
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-prod.txt  # Optional, for production-like environment
   pip install pylint flake8 pytest
   ```

4. **Run the application:**
   ```bash
   python server.py
   ```
   The app will be available at `http://127.0.0.1:5000/`.

5. **Run tests:**
   ```bash
   export PYTHONPATH=$PYTHONPATH:.  # On macOS/Linux
   # or
   set PYTHONPATH=%PYTHONPATH%;.    # On Windows
   pytest
   ```

## Style Guide

### Python Style Guide

We use `pylint` and `flake8` to maintain code quality. Please ensure your code passes these checks before submitting a PR.

- **Pylint:** Run `pylint $(git ls-files '*.py')` to check for errors and stylistic issues.
- **Flake8:** We use Flake8 for additional linting checks as defined in our CI workflow.
- **Docstrings:** All modules, classes, and functions should have clear docstrings.
- **Naming:** Follow PEP 8 naming conventions (snake_case for functions and variables, PascalCase for classes).

---
Thank you for contributing!
