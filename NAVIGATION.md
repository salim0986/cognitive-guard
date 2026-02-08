# 🧭 Navigation Guide

Welcome to **Cognitive Guard**! This guide helps you navigate the project structure.

## 📖 Where to Start

| I want to... | Go to... |
|--------------|----------|
| **Understand the project** | [README.md](README.md) |
| **Get started quickly** | [QUICKSTART.md](QUICKSTART.md) |
| **See complete project info** | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |
| **Learn the architecture** | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| **Read user documentation** | [docs/README.md](docs/README.md) |
| **Contribute code** | [CONTRIBUTING.md](CONTRIBUTING.md) |
| **Report security issues** | [SECURITY.md](SECURITY.md) |
| **Check version history** | [CHANGELOG.md](CHANGELOG.md) |

## 🗂️ Directory Structure

```
cognitive-guard/
│
├── 📚 Documentation
│   ├── README.md              → Project overview
│   ├── QUICKSTART.md          → Getting started guide
│   ├── PROJECT_SUMMARY.md     → Complete project summary
│   ├── CONTRIBUTING.md        → How to contribute
│   ├── CHANGELOG.md           → Version history
│   ├── SECURITY.md            → Security policy
│   └── docs/
│       ├── README.md          → User documentation
│       └── ARCHITECTURE.md    → Technical architecture
│
├── 💻 Source Code
│   └── cognitive_guard/
│       ├── cli.py             → CLI entry point
│       ├── core/              → Core functionality
│       │   ├── complexity.py  → Complexity analyzer
│       │   ├── scanner.py     → File scanner
│       │   └── config.py      → Configuration
│       ├── parsers/           → Language parsers
│       ├── analyzers/         → Complexity analyzers
│       ├── tui/               → Terminal UI
│       ├── hooks/             → Git hook manager
│       └── utils/             → Statistics & achievements
│
├── 🧪 Tests
│   └── tests/
│       ├── unit/              → Unit tests
│       ├── integration/       → Integration tests
│       ├── fixtures/          → Test data
│       └── conftest.py        → Pytest configuration
│
├── 💡 Examples
│   └── examples/
│       ├── sample_code.py     → Example Python file
│       └── demo.sh            → Demo script
│
├── ⚙️ Configuration
│   ├── pyproject.toml         → Project configuration
│   ├── .pre-commit-config.yaml→ Pre-commit hooks
│   ├── .gitignore             → Git ignore patterns
│   ├── .cognitive-guard.example.yml → Example config
│   └── Makefile               → Build automation
│
├── 🚀 CI/CD
│   └── .github/workflows/
│       ├── ci.yml             → Continuous integration
│       └── release.yml        → Release automation
│
└── 🛠️ Tools
    ├── LICENSE                → MIT license
    └── verify_setup.py        → Setup verification
```

## 🎯 Common Tasks

### For Users

```bash
# Read the quick start guide
cat QUICKSTART.md

# Install the tool
pip install -e '.[dev]'

# Verify installation
python3 verify_setup.py

# Initialize in your project
cognitive-guard init

# Run a scan
cognitive-guard scan
```

### For Developers

```bash
# Setup development environment
make install-dev

# Run tests
make test

# Check code quality
make lint

# Format code
make format

# View all make targets
make help
```

### For Contributors

1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Check [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
3. Look at example tests in `tests/unit/`
4. Follow the code style guidelines

## 🔍 Finding Specific Information

### How It Works
- Algorithm: `cognitive_guard/core/complexity.py`
- File scanning: `cognitive_guard/core/scanner.py`
- Git hooks: `cognitive_guard/hooks/`

### Configuration
- Config structure: `cognitive_guard/core/config.py`
- Example config: `.cognitive-guard.example.yml`
- Defaults: See `Config.create_default()` in code

### User Interface
- CLI commands: `cognitive_guard/cli.py`
- TUI app: `cognitive_guard/tui/app.py`
- Output formatting: Uses Rich library

### Statistics & Gamification
- Achievement system: `cognitive_guard/utils/stats.py`
- Data storage: Local `.cognitive-guard/stats.json`

### Testing
- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`
- Test fixtures: `tests/conftest.py`

### Examples
- Sample code: `examples/sample_code.py`
- Demo script: `examples/demo.sh`

## 📞 Getting Help

| Question Type | Resource |
|---------------|----------|
| "How do I use it?" | [QUICKSTART.md](QUICKSTART.md) |
| "How does it work?" | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| "How do I contribute?" | [CONTRIBUTING.md](CONTRIBUTING.md) |
| "Is it secure?" | [SECURITY.md](SECURITY.md) |
| "What's new?" | [CHANGELOG.md](CHANGELOG.md) |
| "Everything else" | [README.md](README.md) |

## 🎓 Learning Path

1. **Beginner**: Read README.md → Try QUICKSTART.md → Run demo
2. **User**: Read docs/README.md → Configure for your project
3. **Developer**: Read ARCHITECTURE.md → Study code → Run tests
4. **Contributor**: Read CONTRIBUTING.md → Pick an issue → Submit PR

## 🚀 Project Status

✅ **Production Ready**

- All core features implemented
- Comprehensive test suite
- Full documentation
- CI/CD configured
- Ready for PyPI publication

## 📬 Contact & Support

- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/cognitive-guard/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/cognitive-guard/discussions)
- 📧 Email: support@example.com

---

**Happy coding!** 🧠✨
