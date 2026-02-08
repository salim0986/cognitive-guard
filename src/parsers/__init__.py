"""Language-specific parsers for different programming languages"""

from abc import ABC, abstractmethod
from typing import List

from cognitive_guard.core.complexity import ComplexityResult


class BaseParser(ABC):
    """Base class for language-specific parsers"""
    
    @abstractmethod
    def parse_file(self, file_path: str) -> List[ComplexityResult]:
        """Parse a file and return complexity results"""
        pass
    
    @abstractmethod
    def supports_extension(self, extension: str) -> bool:
        """Check if this parser supports the given file extension"""
        pass


class PythonParser(BaseParser):
    """Parser for Python files"""
    
    def parse_file(self, file_path: str) -> List[ComplexityResult]:
        from cognitive_guard.core.complexity import ComplexityAnalyzer
        analyzer = ComplexityAnalyzer()
        return analyzer.analyze_file(file_path)
    
    def supports_extension(self, extension: str) -> bool:
        return extension in [".py", ".pyi"]


class JavaScriptParser(BaseParser):
    """Parser for JavaScript files (stub for future implementation)"""
    
    def parse_file(self, file_path: str) -> List[ComplexityResult]:
        # TODO: Implement JavaScript parsing using esprima or similar
        return []
    
    def supports_extension(self, extension: str) -> bool:
        return extension in [".js", ".jsx", ".mjs"]


class TypeScriptParser(BaseParser):
    """Parser for TypeScript files (stub for future implementation)"""
    
    def parse_file(self, file_path: str) -> List[ComplexityResult]:
        # TODO: Implement TypeScript parsing
        return []
    
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
        from pathlib import Path
        extension = Path(file_path).suffix
        
        for parser in cls._parsers:
            if parser.supports_extension(extension):
                return parser
        
        return None
