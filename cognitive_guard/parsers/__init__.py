"""Language-specific parsers for different programming languages"""

from abc import ABC, abstractmethod
from pathlib import Path

import lizard

from cognitive_guard.core.complexity import ComplexityResult


class BaseParser(ABC):
    """Base class for language-specific parsers"""

    @abstractmethod
    def parse_file(self, file_path: str) -> list[ComplexityResult]:
        """Parse a file and return complexity results"""
        pass

    @abstractmethod
    def supports_extension(self, extension: str) -> bool:
        """Check if this parser supports the given file extension"""
        pass


class PythonParser(BaseParser):
    """Parser for Python files using AST-based analysis"""

    def parse_file(self, file_path: str) -> list[ComplexityResult]:
        from cognitive_guard.core.complexity import ComplexityAnalyzer

        analyzer = ComplexityAnalyzer()
        return analyzer.analyze_file(file_path)

    def supports_extension(self, extension: str) -> bool:
        return extension in [".py", ".pyi"]


class JavaScriptParser(BaseParser):
    """Parser for JavaScript files using Lizard"""

    def parse_file(self, file_path: str) -> list[ComplexityResult]:
        """
        Parse JavaScript file and extract function complexity.

        Uses Lizard for complexity analysis and checks for JSDoc comments.
        """
        try:
            # Analyze with Lizard
            analysis = lizard.analyze_file(file_path)

            # Read file to check for JSDoc comments
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            results = []
            for func in analysis.function_list:
                # Check if function has JSDoc comment
                has_jsdoc = self._has_jsdoc(content, func.start_line)

                result = ComplexityResult(
                    name=func.name,
                    line_number=func.start_line,
                    complexity=func.cyclomatic_complexity,
                    has_docstring=has_jsdoc,
                    node=None,
                )
                results.append(result)

            return results

        except Exception as e:
            # Log parsing failure instead of silent return
            import sys

            print(f"Warning: Failed to parse JavaScript file {file_path}: {e}", file=sys.stderr)
            return []

    def _has_jsdoc(self, content: str, line_number: int) -> bool:
        """
        Check if a function has a JSDoc comment before it.

        JSDoc format: /** ... */
        """
        lines = content.split("\n")

        # Look backwards from the function line for JSDoc
        for i in range(line_number - 2, max(0, line_number - 10), -1):
            if i >= len(lines):
                continue

            line = lines[i].strip()

            # Found JSDoc end marker
            if line.endswith("*/"):
                # Now check if there's a JSDoc start marker above
                for j in range(i, max(0, i - 20), -1):
                    if j >= len(lines):
                        continue
                    if "/**" in lines[j]:
                        return True
                return False

            # Skip empty lines
            if not line:
                continue

            # If we hit code that's not a comment, no JSDoc
            if line and not line.startswith("//") and not line.startswith("*"):
                break

        return False

    def supports_extension(self, extension: str) -> bool:
        return extension in [".js", ".jsx", ".mjs"]


class TypeScriptParser(BaseParser):
    """Parser for TypeScript files using Lizard"""

    def parse_file(self, file_path: str) -> list[ComplexityResult]:
        """
        Parse TypeScript file and extract function complexity.

        Uses Lizard for complexity analysis and checks for JSDoc comments.
        TypeScript also supports TSDoc format.
        """
        try:
            # Lizard supports TypeScript out of the box
            analysis = lizard.analyze_file(file_path)

            # Read file to check for JSDoc/TSDoc comments
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            results = []
            for func in analysis.function_list:
                # Check if function has JSDoc/TSDoc comment
                has_doc = self._has_documentation(content, func.start_line)

                result = ComplexityResult(
                    name=func.name,
                    line_number=func.start_line,
                    complexity=func.cyclomatic_complexity,
                    has_docstring=has_doc,
                    node=None,
                )
                results.append(result)

            return results

        except Exception as e:
            # Log parsing failure instead of silent return
            import sys

            print(f"Warning: Failed to parse TypeScript file {file_path}: {e}", file=sys.stderr)
            return []

    def _has_documentation(self, content: str, line_number: int) -> bool:
        """
        Check if a function has JSDoc or TSDoc comment before it.

        Formats: /** ... */ or /// (triple-slash comments)
        """
        lines = content.split("\n")

        # Look backwards from the function line
        for i in range(line_number - 2, max(0, line_number - 10), -1):
            if i >= len(lines):
                continue

            line = lines[i].strip()

            # Found JSDoc end marker
            if line.endswith("*/"):
                # Check for JSDoc start marker above
                for j in range(i, max(0, i - 20), -1):
                    if j >= len(lines):
                        continue
                    if "/**" in lines[j]:
                        return True
                return False

            # Found triple-slash comment (TSDoc)
            if line.startswith("///"):
                return True

            # Skip empty lines
            if not line:
                continue

            # If we hit code that's not a comment, no documentation
            if line and not line.startswith("//") and not line.startswith("*"):
                break

        return False

    def supports_extension(self, extension: str) -> bool:
        return extension in [".ts", ".tsx"]


class ParserFactory:
    """Factory for creating appropriate parser based on file extension"""

    _parsers = [
        PythonParser(),
        JavaScriptParser(),
        TypeScriptParser(),
    ]

    @classmethod
    def get_parser(cls, file_path: str) -> BaseParser | None:
        """Get appropriate parser for the given file"""

        extension = Path(file_path).suffix

        for parser in cls._parsers:
            if parser.supports_extension(extension):
                return parser

        return None
