# Quick Start Guide

## Prerequisites

- Python 3.9 or higher
- Git
- pip

## Installation

### Option 1: From PyPI (when published)

```bash
pip install cognitive-guard
```

### Option 2: From Source

```bash
git clone https://github.com/yourusername/cognitive-guard.git
cd cognitive-guard
pip install -e ".[dev]"
```

## First Time Setup

### 1. Initialize in Your Project

```bash
cd your-project
cognitive-guard init
```

This will:
- Create `.cognitive-guard.yml` configuration file
- Install git pre-commit hook
- Display setup confirmation

### 2. Customize Configuration (Optional)

Edit `.cognitive-guard.yml`:

```yaml
complexity_threshold: 10  # Adjust based on your team's preference
target_coverage: 0.9      # 90% documentation coverage goal
languages:
  - python
  # - javascript  # Enable as needed
  # - typescript
```

### 3. Run Your First Scan

```bash
cognitive-guard scan
```

You'll see:
- Total functions analyzed
- Current documentation coverage
- List of violations (if any)

## Understanding Your First Report

### Example Output

```
📊 Scan Results

Files analyzed: 15
Total functions: 47
Documentation coverage: 85.1%
Violations: 7

🚫 Documentation Violations
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━┓
┃ File           ┃ Function    ┃ Line ┃ Score ┃ Severity     ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━┩
│ src/utils.py   │ process     │  45  │  12   │ 🟠 complex   │
│ src/api.py     │ handle_req  │  78  │  15   │ 🟠 complex   │
└────────────────┴─────────────┴──────┴───────┴──────────────┘
```

### What This Means

- **🟢 Simple (0-5)**: No documentation required
- **🟡 Moderate (6-10)**: Documentation recommended but not enforced
- **🟠 Complex (11-15)**: Documentation required - commit will be blocked
- **🔴 Very Complex (16+)**: Consider refactoring + detailed docs required

## Fixing Violations

### Method 1: Interactive TUI (Recommended)

```bash
cognitive-guard tui
```

This launches an interactive interface where you can:
1. See each violation one by one
2. Write documentation in the editor
3. Save and move to the next
4. Track your progress

### Method 2: Manual Editing

Open the flagged file and add a docstring:

```python
def process(data, options):
    """
    Process data according to specified options.
    
    Args:
        data: Input data to process
        options: Dictionary of processing options
            - mode: 'strict' or 'lenient'
            - threshold: Numeric filtering threshold
    
    Returns:
        Processed data list
    
    Raises:
        ValueError: If options are invalid
    """
    # implementation...
```

### Method 3: Adjust Threshold (If Appropriate)

If many functions are flagged but aren't truly complex for your domain:

```yaml
# .cognitive-guard.yml
complexity_threshold: 12  # Raised from 10
```

## Daily Workflow

### Before Committing

The hook runs automatically:

```bash
git add .
git commit -m "feat: add new feature"
```

If violations exist:
```
🚫 Commit blocked!
Complex functions without documentation detected.

Launch interactive TUI to fix? (y/n)
```

### Checking Staged Changes Only

```bash
cognitive-guard check --staged
```

### Viewing Progress

```bash
cognitive-guard stats
```

See your achievements and documentation journey!

## Tips for Success

### 1. Start with Examples

Look at `examples/sample_code.py` to see good documentation examples.

### 2. Focus on the "Why"

Good docstrings explain:
- **What** the function does (brief)
- **Why** it exists (context)
- **How** to use it (examples)
- **Edge cases** to watch for

Bad docstrings just restate the code:
```python
def add(a, b):
    """Add two numbers"""  # Too obvious
    return a + b
```

### 3. Refactor When Score > 20

If a function scores very high, consider:
- Breaking it into smaller functions
- Extracting nested logic
- Simplifying conditionals

### 4. Use Ignore Patterns

Don't analyze everything:

```yaml
ignore:
  - "**/test_*.py"      # Tests
  - "**/migrations/**"  # Generated code
  - "**/__init__.py"    # Usually simple
```

### 5. Team Adoption

- Start with `threshold: 15` (lenient)
- Gradually lower to `10` as team adapts
- Review configuration in team meetings
- Celebrate achievements together!

## Troubleshooting

### "Hook not triggering"

```bash
cognitive-guard update-hook
```

### "Too many false positives"

Increase threshold or add ignore patterns.

### "Need to commit urgently"

```bash
git commit --no-verify
```

Use sparingly!

### "Command not found"

Ensure installation completed:
```bash
pip install -e .
which cognitive-guard
```

## Next Steps

- Read [full documentation](docs/README.md)
- Review [architecture](docs/ARCHITECTURE.md)
- Check [contributing guide](CONTRIBUTING.md)
- Star the repo! ⭐

## Getting Help

- 🐛 [Report bugs](https://github.com/yourusername/cognitive-guard/issues)
- 💬 [Ask questions](https://github.com/yourusername/cognitive-guard/discussions)
- 📧 Email: support@example.com

---

Happy documenting! 🧠✨
