# Contributing to WFGY

Thank you for your interest in contributing to **WFGY**! To make contributions smooth and effective, please follow this guide.

## 1. Reporting Issues
- Before opening a new issue, search existing issues to see if the topic has already been raised.
- To create a new issue, choose the appropriate issue template (bug report or feature request) and provide:
  - A clear description of the problem or feature.
  - Steps to reproduce (for bugs), including code snippets or minimal reproduction example.
  - Environment details: Python version, OS, WFGY SDK version, etc.
- If you discover a security vulnerability, do **not** disclose details publicly. Instead, follow the procedure in `SECURITY.md`.

## 2. Fork & Clone
```bash
git clone https://github.com/onestardao/WFGY.git
cd WFGY
# Use Python >= 3.10 in a virtual environment
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows PowerShell:
# .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
