# AGENTS.md
## Build/Lint/Test Commands
### Environment Setup
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate    # Windows
pip install -e .[dev]
```
Linting
# Run all linters
pylint logmaster
flake8 logmaster
mypy logmaster
# Auto-formatting
black logmaster
isort logmaster
Testing
# Run all tests
python -m pytest tests/
# Run single test file
python -m pytest tests/test_parser.py
# Run specific test case
python -m pytest tests/test_parser.py::TestParser::test_error_line_filtering
# Run with coverage
python -m pytest --cov=logmaster --cov-report=html tests/
Code Style Guidelines
General Principles
1. Follow PEP 8 unless contradicted here
2. Prefer clarity over cleverness
3. Document "why" not "what"
Imports
# 1. Standard library
import os
import sys
# 2. Third-party
import patoolib
# 3. Local
from .exceptions import LogParseError
Formatting
- Line length: 100 chars (Black-enforced)
- Strings: Prefer double quotes
- Indentation: 4 spaces
- Trailing commas: Required for multi-line collections
- Black settings:
    [tool.black]
  line-length = 100
  target-version = ['py39']
  include = '\.pyi?$'
  
Type Annotations
- Full type hints required (mypy strict)
- Use Protocol for interfaces
- Avoid Any - prefer explicit types
- Annotate public APIs thoroughly
Naming
Type
Module
Class
Function
Variable
Constant
Protected
Error Handling
1. Use custom exceptions:
class LogParseError(Exception):
    """Base error for log parsing failures."""
2. Validate early:
def parse_file(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Log file missing: {path}")
3. Context-rich messages:
try:
    parse_file("test.hilog")
except LogParseError as e:
    logger.error(f"Failed to parse: {e}\n{debug_info}")
    raise
File Operations
Always use context managers:
with open(path, encoding="utf8") as f:
    content = f.read()  # For small files
# For large files:
for line in io.open(path, encoding=detected_encoding):
    process(line)
Testing Conventions
1. Test files mirror source structure
2. Prefer pytest fixtures over setUp
3. Test names should read like specifications:
def test_parser_handles_unicode_smoke_test():
    """Test we can process log files with special chars."""
4. Golden rule:
> One assertion per behavior (not per test case)
Git Practices
- Commit messages:
    feat(parser): add RAR archive support
  fix(analysis): handle missing timestamps
  - Branch naming: feature/rar-support
Code Review Checklist
1. [ ] All new classes have docstrings
2. [ ] Types exist for all public methods
3. [ ] Error cases are properly handled
4. [ ] Tests cover edge cases
5. [ ] No sensitive data in commits