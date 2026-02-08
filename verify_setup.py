#!/usr/bin/env python3
"""
Setup verification script for Cognitive Guard
Checks that all components are properly configured
"""

import sys
from pathlib import Path


def check_file(path: Path, description: str) -> bool:
    """Check if a file exists"""
    if path.exists():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description}: {path} [MISSING]")
        return False


def check_directory(path: Path, description: str) -> bool:
    """Check if a directory exists"""
    if path.is_dir():
        print(f"✓ {description}: {path}/")
        return True
    else:
        print(f"✗ {description}: {path}/ [MISSING]")
        return False


def main() -> int:
    """Run all checks"""
    print("🔍 Cognitive Guard Setup Verification")
    print("=" * 50)
    
    root = Path(__file__).parent
    checks = []
    
    print("\n📦 Core Package Structure:")
    checks.append(check_directory(root / "cognitive_guard", "Main package"))
    checks.append(check_file(root / "cognitive_guard" / "__init__.py", "Package init"))
    checks.append(check_file(root / "cognitive_guard" / "cli.py", "CLI module"))
    
    print("\n🧠 Core Modules:")
    checks.append(check_directory(root / "cognitive_guard" / "core", "Core module"))
    checks.append(check_file(root / "cognitive_guard" / "core" / "complexity.py", "Complexity analyzer"))
    checks.append(check_file(root / "cognitive_guard" / "core" / "scanner.py", "Code scanner"))
    checks.append(check_file(root / "cognitive_guard" / "core" / "config.py", "Configuration"))
    
    print("\n🖥️  UI Components:")
    checks.append(check_directory(root / "cognitive_guard" / "tui", "TUI module"))
    checks.append(check_file(root / "cognitive_guard" / "tui" / "app.py", "TUI application"))
    
    print("\n🪝 Git Hooks:")
    checks.append(check_directory(root / "cognitive_guard" / "hooks", "Hooks module"))
    checks.append(check_file(root / "cognitive_guard" / "hooks" / "installer.py", "Hook installer"))
    
    print("\n📊 Utilities:")
    checks.append(check_directory(root / "cognitive_guard" / "utils", "Utils module"))
    checks.append(check_file(root / "cognitive_guard" / "utils" / "stats.py", "Statistics tracker"))
    
    print("\n🧪 Tests:")
    checks.append(check_directory(root / "tests", "Test directory"))
    checks.append(check_directory(root / "tests" / "unit", "Unit tests"))
    checks.append(check_directory(root / "tests" / "integration", "Integration tests"))
    checks.append(check_file(root / "tests" / "conftest.py", "Test fixtures"))
    
    print("\n📚 Documentation:")
    checks.append(check_file(root / "README.md", "Main README"))
    checks.append(check_file(root / "QUICKSTART.md", "Quick start guide"))
    checks.append(check_file(root / "CONTRIBUTING.md", "Contributing guide"))
    checks.append(check_file(root / "docs" / "README.md", "User documentation"))
    checks.append(check_file(root / "docs" / "ARCHITECTURE.md", "Architecture docs"))
    
    print("\n⚙️  Configuration Files:")
    checks.append(check_file(root / "pyproject.toml", "Project configuration"))
    checks.append(check_file(root / ".gitignore", "Git ignore"))
    checks.append(check_file(root / ".pre-commit-config.yaml", "Pre-commit config"))
    checks.append(check_file(root / "LICENSE", "License file"))
    checks.append(check_file(root / "Makefile", "Makefile"))
    
    print("\n🚀 CI/CD:")
    checks.append(check_file(root / ".github" / "workflows" / "ci.yml", "CI workflow"))
    checks.append(check_file(root / ".github" / "workflows" / "release.yml", "Release workflow"))
    
    print("\n💡 Examples:")
    checks.append(check_directory(root / "examples", "Examples directory"))
    checks.append(check_file(root / "examples" / "sample_code.py", "Sample Python code"))
    checks.append(check_file(root / "examples" / "demo.sh", "Demo script"))
    
    print("\n" + "=" * 50)
    
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"✅ All checks passed! ({passed}/{total})")
        print("\n🎉 Cognitive Guard is ready to use!")
        print("\nNext steps:")
        print("  1. pip install -e '.[dev]'")
        print("  2. make test")
        print("  3. cognitive-guard init")
        return 0
    else:
        print(f"⚠️  Some checks failed: {passed}/{total} passed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
