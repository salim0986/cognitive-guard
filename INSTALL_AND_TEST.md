# Installing and Testing Cognitive Guard (Local Development)

Since this package is not yet published to PyPI, follow these steps to install and test it locally.

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- git (optional, for git hook features)

## Installation Steps

### 1. Navigate to the project directory

```bash
cd cognitive-guard
```

### 2. Create and activate a virtual environment (recommended)

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install pip (if not available in venv)

```bash
python -m ensurepip
```

### 4. Install the package in editable mode

```bash
pip install -e .
```

This installs cognitive-guard with all its dependencies from the local directory.

### 5. For development (with testing tools)

```bash
pip install -e ".[dev]"
```

This includes pytest, black, ruff, mypy, and other development tools.

## Testing the CLI

### Basic Commands

**Check version and help:**
```bash
cognitive-guard --version
cognitive-guard --help
```

**View all commands:**
```bash
cognitive-guard --help
```

### Test with Example Code

The project includes example code to test with:

```bash
# Navigate to examples directory
cd examples

# Initialize Cognitive Guard
cognitive-guard init

# Scan the example code
cognitive-guard scan

# Check for violations
cognitive-guard check

# View statistics
cognitive-guard stats
```

### Test in Your Own Project

```bash
# Navigate to your project
cd /path/to/your/project

# Initialize (creates .cognitive-guard.yml and installs git hook)
cognitive-guard init

# Scan your codebase
cognitive-guard scan

# Check only staged files (useful before commit)
cognitive-guard check --staged

# Launch interactive TUI
cognitive-guard tui
```

## Running Tests

If you installed with `[dev]` dependencies:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_complexity.py

# Run with coverage
pytest --cov=cognitive-guard

# Run tests via Makefile
make test
make test-cov  # with HTML coverage report
```

## Code Quality Checks

```bash
# Format code
black cognitive_guard tests

# Lint code
ruff cognitive_guard tests

# Type check
mypy cognitive_guard

# Run all checks at once
make lint
```

## Expected Output Example

When you run `cognitive-guard scan` on the examples, you should see:

```
🔍 Scanning codebase...

📊 Scan Results

Files analyzed: 1
Total functions: 6
Documentation coverage: 83.3%
Violations: 1

                    🚫 Documentation Violations                    
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┓
┃ File              ┃ Function          ┃ Line ┃ Score ┃  Severity  ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━╇━━━━━━━━━━━━┩
│ sample_code.py    │ undocumented_...  │ 48   │   20  │ 🔴 very... │
└───────────────────┴───────────────────┴──────┴───────┴────────────┘
```

## Troubleshooting

### "cognitive-guard: command not found"

Make sure:
1. You've activated the virtual environment
2. You've installed the package with `pip install -e .`
3. The `.venv/bin` directory is in your PATH

### "No module named pip"

Run: `python -m ensurepip` to install pip in your virtual environment

### Import errors

Make sure you've installed all dependencies:
```bash
pip install -e ".[dev]"
```

## Configuration

After running `cognitive-guard init`, edit `.cognitive-guard.yml` to customize:

- `complexity_threshold`: Minimum complexity requiring documentation (default: 10)
- `target_coverage`: Target documentation coverage (default: 0.9 = 90%)
- `languages`: Languages to analyze (default: python, javascript, typescript, java)
- `ignore`: File patterns to skip (tests, migrations, etc.)

## Quick Demo

```bash
# One-liner to test everything
cd examples && \
  cognitive-guard init && \
  cognitive-guard scan && \
  cognitive-guard stats
```

## Deactivating Virtual Environment

When you're done:
```bash
deactivate
```

## Next Steps

- Try it on your own Python projects
- Customize `.cognitive-guard.yml` for your needs
- Commit code to trigger the pre-commit hook
- Explore the interactive TUI with `cognitive-guard tui`
- Check your achievements with `cognitive-guard stats`

---

**Note:** This is a local development installation. To publish to PyPI, use:
```bash
make build    # Build distribution packages
make publish  # Publish to PyPI (requires credentials)
```
