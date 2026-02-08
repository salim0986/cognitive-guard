# Cognitive Guard Documentation

## Installation

```bash
pip install cognitive-guard
```

## Quick Start

```bash
# Initialize in your project
cd your-project
cognitive-guard init

# Check staged changes
cognitive-guard check --staged

# Scan entire codebase
cognitive-guard scan

# View statistics
cognitive-guard stats
```

## Configuration

Create `.cognitive-guard.yml` in your project root:

```yaml
complexity_threshold: 10
target_coverage: 0.9
languages:
  - python
  - javascript
  - typescript
ignore:
  - "**/test_*.py"
  - "**/*.test.js"
gamification:
  enabled: true
  show_achievements: true
  track_stats: true
```

## Understanding Brain Scores

Brain Score = Cognitive Complexity calculated using:

- **Control Flow**: +1 for each if, while, for, switch
- **Nesting**: +1 for each nesting level
- **Boolean Logic**: +1 for each && or ||
- **Recursion**: +2 for recursive calls
- **Exception Handling**: +1 for each try/catch

### Score Interpretation

| Score | Emoji | Meaning |
|-------|-------|---------|
| 0-5   | 🟢 | Simple - No documentation required |
| 6-10  | 🟡 | Moderate - Documentation recommended |
| 11-15 | 🟠 | Complex - Documentation required |
| 16+   | 🔴 | Very Complex - Detailed docs required, consider refactoring |

## CLI Commands

### `cognitive-guard init`

Initializes Cognitive Guard in your repository. Creates `.cognitive-guard.yml` and installs the git pre-commit hook.

Options:
- `--force` - Overwrite existing configuration

### `cognitive-guard check`

Checks code for documentation violations.

Options:
- `--staged` - Only check staged files (default in pre-commit hook)
- `--json` - Output results as JSON

### `cognitive-guard scan`

Scans entire codebase and generates coverage report.

Options:
- `--fail-under <threshold>` - Fail if coverage is below threshold (0.0-1.0)

### `cognitive-guard tui`

Launches interactive terminal UI for fixing violations.

### `cognitive-guard stats`

Displays your documentation statistics and achievements.

### `cognitive-guard update-hook`

Updates the git pre-commit hook to the latest version.

## Bypassing the Hook

In emergencies, you can bypass the pre-commit hook:

```bash
git commit --no-verify
```

**Note**: Use sparingly! The hook exists to help maintain code quality.

## Custom Thresholds

You can set custom thresholds for specific files:

```python
# cognitive-guard: threshold=15
def very_complex_function():
    """This needs a higher threshold"""
    pass
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Cognitive Guard

on: [pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Cognitive Guard
        run: pip install cognitive-guard
      - name: Check Documentation
        run: cognitive-guard scan --fail-under 0.9
```

### GitLab CI

```yaml
cognitive-guard:
  image: python:3.11
  script:
    - pip install cognitive-guard
    - cognitive-guard scan --fail-under 0.9
  only:
    - merge_requests
```

## Language Support

### Currently Supported

- ✅ Python (full support)

### Planned

- 🚧 JavaScript/TypeScript
- 🚧 Java
- 🚧 Go
- 🚧 Rust

## Achievements

Track your documentation journey with gamification:

- 📝 **First Steps**: Document your first complex function
- 🎯 **Marksman**: Achieve 90% documentation coverage
- 🧠 **Mind Reader**: Document 10 functions with Score > 15
- 🚀 **Speed Demon**: Document 5 functions in one session
- 💯 **Perfectionist**: Achieve 100% documentation coverage

## Best Practices

1. **Document complexity, not simplicity** - Focus on functions above the threshold
2. **Explain the "why", not the "what"** - Good docstrings explain intent and reasoning
3. **Use examples** - Show how to use complex functions
4. **Keep it updated** - When code changes significantly, update docs
5. **Consider refactoring** - If Score > 20, maybe the function is too complex

## Troubleshooting

### Hook not triggering

```bash
# Reinstall the hook
cognitive-guard update-hook

# Verify installation
cat .git/hooks/pre-commit
```

### False positives

Adjust `complexity_threshold` in `.cognitive-guard.yml` or use inline comments:

```python
# cognitive-guard: threshold=15
# or
# cognitive-guard: ignore
```

### Performance issues

Add aggressive ignore patterns to skip large files:

```yaml
ignore:
  - "**/migrations/**"
  - "**/node_modules/**"
  - "**/*.min.js"
```

## API Reference

See [API.md](API.md) for detailed API documentation.
