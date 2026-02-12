# Copilot Instructions for Cognitive Guard

## Project Overview

Cognitive Guard is a CLI tool that analyzes cognitive complexity of code and enforces documentation for complex functions through git hooks. It gamifies the documentation process with achievements and statistics tracking.

## Build, Test, and Lint

### Setup
```bash
pip install -e ".[dev]"       # Install with dev dependencies
pre-commit install            # Install pre-commit hooks
make install-dev              # Alternative: install + setup pre-commit
```

### Testing
```bash
pytest                                 # Run all tests
pytest tests/unit/test_complexity.py   # Run single test file
pytest -k "test_simple_function"       # Run specific test
pytest --cov=cognitive_guard           # Run with coverage
make test                              # Run all tests (via Makefile)
make test-cov                          # Run with HTML coverage report
```

### Code Quality
```bash
black cognitive_guard tests   # Format code
ruff cognitive_guard tests    # Lint code
mypy cognitive_guard          # Type check
make lint                     # Run all linters at once
make format                   # Format and auto-fix linting issues
```

### Running the CLI
```bash
cognitive-guard init          # Initialize in a repository
cognitive-guard scan          # Scan entire codebase
cognitive-guard check         # Check all files
cognitive-guard check --staged  # Check only staged files
cognitive-guard tui           # Launch interactive TUI
cognitive-guard stats         # View achievements and statistics
```

## Architecture

### Core Data Flow

1. **Analysis Pipeline**: `scanner.py` → `parsers` → `complexity.py` → `ComplexityResult`
   - Scanner identifies files to analyze
   - Parser (language-specific) reads the file
   - ComplexityAnalyzer traverses AST and calculates Brain Score
   - Returns ComplexityResult with severity classification

2. **Result Aggregation**: Multiple `ComplexityResult` → `FileResult` → `ScanResults`
   - Each function produces a ComplexityResult
   - Functions from same file grouped into FileResult
   - All files aggregated into ScanResults for reporting

3. **Violation Detection**: Happens in `scanner.py` during `scan_file()`
   - A function is a violation if: `complexity > threshold AND has_docstring == False`
   - Threshold configured in `.cognitive-guard.yml` (default: 10)

### Key Components

**cognitive_guard/core/**
- `complexity.py` - AST-based complexity analyzer
  - Entry point: `ComplexityAnalyzer.analyze_file()` returns list of `ComplexityResult`
  - `ComplexityResult` dataclass has `.brain_score`, `.severity`, `.emoji` properties
- `scanner.py` - File scanning and violation detection
  - Entry points: `CodeScanner.scan_all()` or `.scan_staged()` return `ScanResults`
  - `FileResult` aggregates results for one file
  - `ScanResults` aggregates all files and has `.display(console)` method
- `config.py` - Re-exports from `cognitive_guard/core/__init__.py`
  - Actual `Config` and `GamificationSettings` Pydantic models in `core/__init__.py`
  - Config loaded from `.cognitive-guard.yml` via `Config.load()`

**cognitive_guard/parsers/**
- Language-specific parsers implementing `BaseParser` (ABC)
- `PythonParser` fully implemented; `JavaScriptParser`/`TypeScriptParser` are stubs
- `ParserFactory.get_parser(file_path)` returns appropriate parser for file extension
- To add a language: subclass `BaseParser`, implement `parse_file()` and `supports_extension()`, register in `ParserFactory._parsers`

**cognitive_guard/cli.py**
- Click-based CLI with 7 commands: `init`, `check`, `scan`, `tui`, `stats`, `update-hook`, `hook`
- `hook` command is called by the git pre-commit hook (not meant for manual use)
- All commands use Rich Console for styled output

**cognitive_guard/tui/**
- `__init__.py` contains the full TUI implementation (154 lines)
- `app.py` is a thin wrapper that re-exports `CognitiveGuardApp`
- Textual-based interactive UI with keyboard bindings (q=quit, s=save, n=next)
- NOTE: Save functionality is stubbed (`action_save()` passes)

**cognitive_guard/hooks/**
- `__init__.py` contains full `HookInstaller` implementation (81 lines)
- `installer.py` is a thin wrapper that re-exports `HookInstaller`
- Installs Python script to `.git/hooks/pre-commit` that calls `cognitive-guard hook`
- Uses GitPython to find repository root

**cognitive_guard/utils/**
- `__init__.py` contains full implementation (176 lines): `Achievement`, `Stats`, `StatsTracker`
- `stats.py` is a thin wrapper that re-exports these classes
- Tracks achievements and statistics in `.cognitive-guard/stats.json`
- Achievement unlocking logic in `StatsTracker._check_achievements()`
- NOTE: Statistics recording is manual (not automatically triggered by scans)

### Complexity Calculation (Brain Score)

Located in `cognitive_guard/core/complexity.py`, method `ComplexityAnalyzer._analyze_node()`:

- **Control flow** (+1 + nesting): `if`, `while`, `for`, `with`
- **Exception handlers** (+1 + nesting): `try`/`except` blocks
- **Boolean operators** (+1 per additional operand): `&&`, `||` in conditions
- **Ternary expressions** (+1): ternary if
- **Function calls** (+1): simplified recursion detection
- **Nesting multiplier**: Each level of nesting increases the score

**Severity classification** (in `ComplexityResult.severity` property):
- 0-5: "simple" 🟢
- 6-10: "moderate" 🟡
- 11-15: "complex" 🟠
- 16+: "very_complex" 🔴

Example: A function with 4 nested `if` statements gets a much higher score than 4 sequential `if` statements due to nesting multiplication.

## Conventions

### Module Structure (IMPORTANT!)
- **Inconsistent pattern**: Some modules have thin wrappers, others have full implementations in `__init__.py`
- **Core modules** (`complexity.py`, `scanner.py`): Full implementations in their own files
- **Config**: `config.py` is a thin wrapper; actual implementation in `core/__init__.py`
- **TUI**: `tui/__init__.py` has full implementation (154 lines); `app.py` is wrapper
- **Hooks**: `hooks/__init__.py` has full implementation (81 lines); `installer.py` is wrapper
- **Utils**: `utils/__init__.py` has full implementation (176 lines); `stats.py` is wrapper
- **Import pattern**: Always import from the wrapper when available
  - ✅ `from cognitive_guard.core.config import Config`
  - ✅ `from cognitive_guard.tui.app import CognitiveGuardApp`
  - ✅ `from cognitive_guard.utils.stats import StatsTracker`
  - ❌ `from cognitive_guard.core import Config` (works but inconsistent)
- **When adding new features**: Follow existing pattern - check if module uses thin wrapper pattern

### Result Objects Pattern
Three result types follow a consistent pattern:
1. `ComplexityResult` - single function analysis
2. `FileResult` - aggregates results for one file
3. `ScanResults` - aggregates results for entire scan

All have:
- Data as public fields/properties
- A `to_dict()` or similar serialization method
- Display helpers (e.g., `display(console)` on ScanResults)

### Configuration

- All config lives in `.cognitive-guard.yml` at project root (YAML format only)
- Loaded via `Config.load()` which returns Pydantic model (defined in `core/__init__.py`)
- Default config: `Config.create_default()`
- Key fields:
  - `complexity_threshold` (int, 1-20, default: 10): Functions above this need docs
  - `target_coverage` (float, 0.0-1.0, default: 0.9): Project documentation goal
  - `languages` (list[str]): Languages to analyze (default: python, javascript, typescript, java)
  - `ignore` (list[str]): Glob patterns to ignore (default includes test files and migrations)
  - `gamification` (GamificationSettings): Nested config for achievement features
- Config validation: Pydantic enforces constraints (e.g., threshold must be 1-20)
- Save config: `config.save(path)` - serializes to YAML with `yaml.dump()`

### Parser/Analyzer Split
- **Parsers** (`cognitive_guard/parsers/`) read source files and identify functions
- **Analyzers** (`cognitive_guard/analyzers/`) calculate complexity for those functions
- Currently Python uses AST directly; future languages may use external tools (esprima, tree-sitter)

### Type Hints
- All function signatures have type hints
- MyPy strict mode enabled (`disallow_untyped_defs = true`)
- Use `from typing import ...` for Python 3.9 compatibility

### CLI Output
- Use Rich library for formatting: `from rich.console import Console`
- Table display for violations: `from rich.table import Table`
- Emojis for severity: 🟢 simple, 🟡 moderate, 🟠 complex, 🔴 very complex

### Testing Patterns
- Unit tests in `tests/unit/` test individual components
- Integration tests in `tests/integration/` test CLI commands
- Fixtures in `tests/conftest.py` create temp files/configs
- Use `pytest-mock` for mocking external dependencies (Git, file system)

## Adding Language Support

1. Create parser class in `cognitive_guard/parsers/`:
   ```python
   class NewLanguageParser(BaseParser):
       def parse_file(self, file_path: str) -> List[ComplexityResult]:
           # Parse and analyze
           pass
       
       def supports_extension(self, extension: str) -> bool:
           return extension in [".ext"]
   ```

2. Register in `ParserFactory._parsers` list

3. Add tests in `tests/unit/test_parsers.py` (create if needed)

4. Update `languages` list in default config (`config.py`)

## Pre-commit Hook Flow

1. User runs `git commit`
2. Git executes `.git/hooks/pre-commit`
3. Hook script runs `cognitive-guard hook`
4. CLI loads config and scans staged files
5. If violations found:
   - Display violations table
   - Prompt to launch TUI
   - Exit with code 1 (blocks commit)
6. If no violations, exit with code 0 (allows commit)

## Common Gotchas

- **Config file**: Must be named `.cognitive-guard.yml` (not `.yaml`)
- **Ignore patterns**: Use fnmatch/glob syntax (`**/test_*.py`), not regex
- **Complexity scoring**: Includes nesting multiplication - deeply nested code scores much higher
- **Module structure**: Check if you're editing a wrapper file vs. the real implementation
  - TUI real code: `tui/__init__.py` (154 lines), not `app.py` (5 lines)
  - Hooks real code: `hooks/__init__.py` (81 lines), not `installer.py` (5 lines)
  - Utils real code: `utils/__init__.py` (176 lines), not `stats.py` (5 lines)
- **TUI save**: `CognitiveGuardApp.action_save()` is stubbed (just `pass`) - doesn't actually write to files
- **Stats tracking**: Requires manual calls to `StatsTracker.record_documentation()` - NOT automatically triggered by scans
- **Parser registration**: After creating a new parser, add it to `ParserFactory._parsers` list
- **Type hints**: Python 3.9 compatibility - use `from typing import ...` for types like `List`, `Dict`, `Optional` (not built-in `list[...]`)
