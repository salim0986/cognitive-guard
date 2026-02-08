# Contributing to Cognitive Guard

Thank you for your interest in contributing! 🎉

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cognitive-guard.git
   cd cognitive-guard
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cognitive_guard

# Run specific test file
pytest tests/unit/test_complexity.py

# Run with verbose output
pytest -v
```

## Code Quality

Before submitting a PR, ensure your code passes all checks:

```bash
# Format code
black cognitive_guard tests

# Lint code
ruff cognitive_guard tests

# Type check
mypy cognitive_guard
```

## Adding Support for New Languages

To add support for a new programming language:

1. Create a parser in `cognitive_guard/parsers/`
2. Create an analyzer in `cognitive_guard/analyzers/`
3. Add tests for the new language
4. Update documentation

Example structure:
```python
# cognitive_guard/parsers/your_language.py
from cognitive_guard.parsers import BaseParser

class YourLanguageParser(BaseParser):
    def parse_file(self, file_path: str) -> List[ComplexityResult]:
        # Implementation
        pass
    
    def supports_extension(self, extension: str) -> bool:
        return extension in [".your_ext"]
```

## Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

Example: `feat: add support for Java complexity analysis`

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'feat: add amazing feature'`)
7. Push to your fork (`git push origin feat/amazing-feature`)
8. Open a Pull Request

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Questions?

Feel free to open an issue or start a discussion!
