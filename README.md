# 🧠 Cognitive Guard

> **Gamify your code documentation. Block commits that hurt brains.**

Cognitive Guard is a revolutionary CLI tool that analyzes the cognitive complexity of your code in real-time and enforces documentation where it matters most. Instead of nagging you about every missing docstring, it focuses on the code that's genuinely hard to understand.

## 🎯 The Problem

- Traditional linters check for missing docs everywhere (boring!)
- Complex code without documentation causes cognitive overload
- Developers skip documentation because it feels like busywork
- No feedback loop between code complexity and documentation requirements

## ✨ The Solution

Cognitive Guard:
- 🎮 **Gamifies** documentation with Brain Scores and achievements
- 🧮 **Calculates** cognitive complexity using AST traversal
- 🎯 **Targets** only complex code (Score > configurable threshold)
- 🚫 **Blocks** commits for undocumented complex functions
- 🖥️ **Launches** an interactive TUI to fix issues on the spot
- 📊 **Tracks** your documentation coverage over time

## 🚀 Quick Start

### Installation

```bash
pip install cognitive-guard
```

### Initialize in Your Project

```bash
cd your-project
cognitive-guard init
```

This installs the git pre-commit hook and creates a `.cognitive-guard.yml` config file.

### Configuration

Edit `.cognitive-guard.yml` to customize:

```yaml
# Complexity threshold (1-20, default: 10)
complexity_threshold: 10

# Target documentation coverage (0.0-1.0, default: 0.9)
target_coverage: 0.9

# Languages to analyze
languages:
  - python
  - javascript
  - typescript
  - java

# Patterns to ignore
ignore:
  - "**/test_*.py"
  - "**/*.test.js"
  - "**/migrations/**"

# Gamification settings
gamification:
  enabled: true
  show_achievements: true
  track_stats: true
```

## 💡 How It Works

1. **Pre-Commit Hook**: Cognitive Guard runs automatically before each commit
2. **AST Analysis**: Parses staged files and builds Abstract Syntax Trees
3. **Brain Score Calculation**: Computes cognitive complexity for each function
4. **Documentation Check**: Verifies complex functions (Score > threshold) have docs
5. **Interactive TUI**: If violations found, launches a beautiful terminal UI to fix them
6. **Commit Decision**: Allows commit only when documentation requirements are met

## 🎮 Brain Score Metrics

Cognitive complexity is calculated based on:

- **Control Flow**: if/else, switch, loops (+1 each)
- **Nesting**: Each level of nesting (+1)
- **Boolean Operators**: &&, ||, ?? in conditions (+1)
- **Recursion**: Recursive calls (+2)
- **Exception Handling**: try/catch blocks (+1)

### Score Ranges

- **0-5**: 🟢 Simple - No docs required
- **6-10**: 🟡 Moderate - Docs recommended
- **11-15**: 🟠 Complex - Docs required
- **16+**: 🔴 Very Complex - Detailed docs required + consider refactoring

## 🖥️ CLI Commands

### Check Staged Changes

```bash
cognitive-guard check
```

Analyzes staged changes and reports complexity scores.

### Scan Entire Codebase

```bash
cognitive-guard scan
```

Full codebase analysis with coverage report.

### Interactive TUI

```bash
cognitive-guard tui
```

Launch the interactive documentation assistant.

### Stats & Achievements

```bash
cognitive-guard stats
```

View your documentation journey and achievements.

### Update Hook

```bash
cognitive-guard update-hook
```

Update the git hook to the latest version.

## 🏆 Gamification Features

### Achievements

- 📝 **First Steps**: Document your first complex function
- 🎯 **Marksman**: Achieve 90% documentation coverage
- 🧠 **Mind Reader**: Document 10 functions with Score > 15
- 🚀 **Speed Demon**: Document 5 functions in one session
- 💯 **Perfectionist**: Achieve 100% documentation coverage

### Stats Tracking

- Total functions analyzed
- Documentation coverage %
- Average Brain Score
- Most complex function
- Documentation streak (consecutive days)

## 🛠️ Advanced Usage

### Bypass Hook (Emergency)

```bash
git commit --no-verify
```

### Custom Thresholds Per File

```python
# cognitive-guard: threshold=15
def ultra_complex_function():
    """This function needs threshold 15 instead of default 10"""
    pass
```

### CI/CD Integration

```yaml
# .github/workflows/cognitive-guard.yml
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

## 🧪 Development

### Setup Development Environment

```bash
git clone https://github.com/yourusername/cognitive-guard.git
cd cognitive-guard
pip install -e ".[dev]"
pre-commit install
```

### Run Tests

```bash
pytest
```

### Code Quality

```bash
black cognitive_guard tests
ruff cognitive_guard tests
mypy cognitive_guard
```

## 📚 Architecture

```
cognitive_guard/
├── core/           # Core complexity calculation engine
├── parsers/        # Language-specific AST parsers
├── analyzers/      # Complexity analyzers per language
├── tui/            # Interactive terminal UI (Textual)
├── hooks/          # Git hook integration
└── utils/          # Shared utilities
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Inspired by cognitive complexity research
- Built with [Textual](https://textual.textualize.io/) for the TUI
- Uses [Radon](https://radon.readthedocs.io/) and [Lizard](https://github.com/terryyin/lizard) for complexity analysis

## 📞 Support

- 📖 [Documentation](https://cognitive-guard.readthedocs.io)
- 🐛 [Issue Tracker](https://github.com/yourusername/cognitive-guard/issues)
- 💬 [Discussions](https://github.com/yourusername/cognitive-guard/discussions)

---

**Remember**: Complex code without documentation is like a puzzle missing the picture on the box. 🧩
