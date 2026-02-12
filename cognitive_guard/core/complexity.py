"""Cognitive complexity analysis engine"""

import ast
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ComplexityResult:
    """Result of complexity analysis for a single function"""
    
    name: str
    line_number: int
    complexity: int
    has_docstring: bool
    node: Any = None
    
    @property
    def brain_score(self) -> int:
        """Alias for complexity"""
        return self.complexity
    
    @property
    def severity(self) -> str:
        """Get severity level based on complexity"""
        if self.complexity <= 5:
            return "simple"
        elif self.complexity <= 10:
            return "moderate"
        elif self.complexity <= 15:
            return "complex"
        else:
            return "very_complex"
    
    @property
    def emoji(self) -> str:
        """Get emoji representation"""
        severity_map = {
            "simple": "🟢",
            "moderate": "🟡",
            "complex": "🟠",
            "very_complex": "🔴"
        }
        return severity_map[self.severity]


class ComplexityAnalyzer:
    """Analyzes cognitive complexity of code using AST traversal"""
    
    def __init__(self) -> None:
        self.complexity = 0
        self.nesting_level = 0
        self.function_name = None
    
    def analyze_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> ComplexityResult:
        """Analyze complexity of a single function"""
        self.complexity = 0
        self.nesting_level = 0
        self.function_name = node.name
        
        self._analyze_node(node)
        
        has_docstring = ast.get_docstring(node) is not None
        
        return ComplexityResult(
            name=node.name,
            line_number=node.lineno,
            complexity=self.complexity,
            has_docstring=has_docstring,
            node=node
        )
    
    def _analyze_node(self, node: ast.AST) -> None:
        """Recursively analyze AST node for complexity"""
        
        # Control flow structures add complexity
        if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
            self.complexity += 1 + self.nesting_level
            self._analyze_nested(node)
        
        elif isinstance(node, (ast.ExceptHandler,)):
            self.complexity += 1 + self.nesting_level
            self._analyze_nested(node)
        
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            self.complexity += 1
            self._analyze_nested(node)
        
        # Boolean operators in conditions
        elif isinstance(node, ast.BoolOp):
            self.complexity += len(node.values) - 1
            for child in ast.iter_child_nodes(node):
                self._analyze_node(child)
        
        # Ternary expressions
        elif isinstance(node, ast.IfExp):
            self.complexity += 1
            for child in ast.iter_child_nodes(node):
                self._analyze_node(child)
        
        # Recursion detection (only count self-referential calls)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and self.function_name:
                # Only add complexity for recursive calls (same function name)
                if node.func.id == self.function_name:
                    self.complexity += 2  # Recursion adds more complexity
            for child in ast.iter_child_nodes(node):
                self._analyze_node(child)
        
        else:
            # Continue traversing
            for child in ast.iter_child_nodes(node):
                self._analyze_node(child)
    
    def _analyze_nested(self, node: ast.AST) -> None:
        """Analyze nested structures with increased nesting level"""
        self.nesting_level += 1
        for child in ast.iter_child_nodes(node):
            self._analyze_node(child)
        self.nesting_level -= 1
    
    def analyze_file(self, file_path: str) -> List[ComplexityResult]:
        """Analyze all functions in a Python file"""
        import tokenize
        
        # Detect encoding to handle non-UTF-8 files
        try:
            with open(file_path, 'rb') as f:
                encoding, _ = tokenize.detect_encoding(f.readline)
        except Exception:
            encoding = 'utf-8'
        
        try:
            with open(file_path, "r", encoding=encoding, errors='replace') as f:
                content = f.read()
        except Exception as e:
            # Can't read file, return empty results
            return []
        
        try:
            tree = ast.parse(content, filename=file_path)
        except SyntaxError:
            return []
        
        results: List[ComplexityResult] = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                try:
                    result = self.analyze_function(node)
                    results.append(result)
                except (UnicodeDecodeError, UnicodeEncodeError):
                    # Skip functions with unicode issues in name
                    continue
        
        return results
    
    @staticmethod
    def get_complexity_description(score: int) -> str:
        """Get human-readable description of complexity score"""
        if score <= 5:
            return "Simple - Easy to understand"
        elif score <= 10:
            return "Moderate - Reasonably clear"
        elif score <= 15:
            return "Complex - Requires careful reading"
        else:
            return "Very Complex - Consider refactoring"
