"""Tests for complexity analyzer"""

import ast
import pytest

from cognitive_guard.core.complexity import ComplexityAnalyzer, ComplexityResult


class TestComplexityAnalyzer:
    """Test cases for ComplexityAnalyzer"""
    
    def test_simple_function(self):
        """Test analysis of a simple function"""
        code = '''
def simple():
    """A simple function"""
    return 42
'''
        tree = ast.parse(code)
        func = tree.body[0]
        
        analyzer = ComplexityAnalyzer()
        result = analyzer.analyze_function(func)
        
        assert result.name == "simple"
        assert result.complexity == 0
        assert result.has_docstring is True
        assert result.severity == "simple"
    
    def test_function_with_if(self):
        """Test function with if statement"""
        code = '''
def with_if(x):
    if x > 0:
        return x
    return 0
'''
        tree = ast.parse(code)
        func = tree.body[0]
        
        analyzer = ComplexityAnalyzer()
        result = analyzer.analyze_function(func)
        
        assert result.name == "with_if"
        assert result.complexity >= 1
    
    def test_nested_complexity(self):
        """Test nested control structures"""
        code = '''
def nested(x, y):
    if x > 0:
        if y > 0:
            return x + y
    return 0
'''
        tree = ast.parse(code)
        func = tree.body[0]
        
        analyzer = ComplexityAnalyzer()
        result = analyzer.analyze_function(func)
        
        assert result.complexity > 2  # Should account for nesting
    
    def test_no_docstring(self):
        """Test function without docstring"""
        code = '''
def no_docs():
    return 42
'''
        tree = ast.parse(code)
        func = tree.body[0]
        
        analyzer = ComplexityAnalyzer()
        result = analyzer.analyze_function(func)
        
        assert result.has_docstring is False
    
    def test_complexity_description(self):
        """Test complexity description helper"""
        assert "Simple" in ComplexityAnalyzer.get_complexity_description(3)
        assert "Moderate" in ComplexityAnalyzer.get_complexity_description(8)
        assert "Complex" in ComplexityAnalyzer.get_complexity_description(12)
        assert "Very Complex" in ComplexityAnalyzer.get_complexity_description(20)
    
    def test_severity_levels(self):
        """Test severity level classification"""
        analyzer = ComplexityAnalyzer()
        
        # Create dummy results with different complexities
        simple = ComplexityResult("func", 1, 3, True)
        moderate = ComplexityResult("func", 1, 8, True)
        complex = ComplexityResult("func", 1, 12, True)
        very_complex = ComplexityResult("func", 1, 20, True)
        
        assert simple.severity == "simple"
        assert moderate.severity == "moderate"
        assert complex.severity == "complex"
        assert very_complex.severity == "very_complex"
