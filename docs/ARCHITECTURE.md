# Cognitive Guard Project Structure

```
cognitive-guard/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Continuous Integration pipeline
│       └── release.yml         # Release automation
│
├── cognitive_guard/            # Main package
│   ├── __init__.py            # Package initialization
│   ├── cli.py                 # CLI entry point and commands
│   │
│   ├── core/                  # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── complexity.py      # Complexity analysis engine
│   │   └── scanner.py         # File scanning and violation detection
│   │
│   ├── parsers/               # Language-specific parsers
│   │   └── __init__.py        # Python, JS, TS parsers (extensible)
│   │
│   ├── analyzers/             # Complexity analyzers
│   │   └── __init__.py        # Language-specific analyzers
│   │
│   ├── tui/                   # Terminal User Interface
│   │   ├── __init__.py
│   │   └── app.py             # Textual-based interactive TUI
│   │
│   ├── hooks/                 # Git hook management
│   │   ├── __init__.py
│   │   └── installer.py       # Hook installation and updates
│   │
│   └── utils/                 # Utilities
│       ├── __init__.py
│       └── stats.py           # Statistics and achievements tracking
│
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures
│   ├── unit/                  # Unit tests
│   │   ├── test_complexity.py
│   │   ├── test_config.py
│   │   └── test_scanner.py
│   ├── integration/           # Integration tests
│   │   └── test_cli.py
│   └── fixtures/              # Test fixtures and sample files
│
├── docs/                      # Documentation
│   └── README.md              # User guide
│
├── examples/                  # Example files
│   ├── sample_code.py         # Demo Python file
│   └── demo.sh                # Demo script
│
├── pyproject.toml             # Project configuration and dependencies
├── README.md                  # Project overview
├── LICENSE                    # MIT License
├── CHANGELOG.md               # Version history
├── CONTRIBUTING.md            # Contribution guidelines
├── .gitignore                 # Git ignore patterns
├── .pre-commit-config.yaml    # Pre-commit hooks configuration
└── .cognitive-guard.example.yml  # Example configuration file
```

## Key Components

### CLI (`cognitive_guard/cli.py`)
- Main entry point for all commands
- Commands: init, check, scan, tui, stats, update-hook, hook
- Uses Click for command-line interface

### Core Engine (`cognitive_guard/core/`)
- **complexity.py**: AST-based cognitive complexity calculator
- **scanner.py**: File scanner and violation detector
- **config.py**: Configuration management with Pydantic

### TUI (`cognitive_guard/tui/`)
- Interactive terminal UI built with Textual
- Helps users fix violations interactively
- Shows real-time statistics and progress

### Git Hooks (`cognitive_guard/hooks/`)
- Installs and manages pre-commit hook
- Runs automatically before commits
- Blocks commits with undocumented complex code

### Gamification (`cognitive_guard/utils/stats.py`)
- Tracks documentation statistics
- Achievement system
- Streak tracking
- Leaderboard-ready data structure

## Architecture Decisions

### Why Python?
- Excellent AST parsing with built-in `ast` module
- Rich ecosystem for CLI tools (Click, Rich, Textual)
- Easy to extend with other language parsers

### Why AST Traversal?
- Accurate complexity calculation
- Language-agnostic approach (extensible)
- Better than regex-based analysis

### Why Git Hooks?
- Enforcement at commit time
- Prevents undocumented complex code from entering repo
- Optional bypass with --no-verify

### Why Gamification?
- Makes documentation fun
- Provides motivation and feedback
- Encourages consistent documentation habits

## Extension Points

### Adding New Languages
1. Create parser in `cognitive_guard/parsers/`
2. Implement `BaseParser` interface
3. Add language-specific complexity rules
4. Register in `ParserFactory`

### Custom Achievements
1. Define in `StatsTracker.ACHIEVEMENTS`
2. Add unlock logic in `_check_achievements()`
3. Save to stats.json

### CI/CD Integrations
- GitHub Actions (included)
- GitLab CI (documented)
- Jenkins, CircleCI, etc. (extensible)
