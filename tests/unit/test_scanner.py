"""Tests for code scanner"""

import pytest
from pathlib import Path
import tempfile

from cognitive_guard.core.scanner import CodeScanner, ScanResults, FileResult
from cognitive_guard.core.config import Config


class TestCodeScanner:
    """Test cases for CodeScanner"""
    
    def test_should_ignore(self):
        """Test ignore pattern matching"""
        config = Config(ignore=["**/test_*.py", "**/__pycache__/**"])
        scanner = CodeScanner(config)
        
        assert scanner.should_ignore(Path("test_example.py"))
        assert scanner.should_ignore(Path("src/test_module.py"))
        assert scanner.should_ignore(Path("__pycache__/module.pyc"))
        assert not scanner.should_ignore(Path("src/module.py"))
    
    def test_scan_file(self):
        """Test scanning a single file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
def simple_func():
    """A simple function"""
    return 42

def complex_func(x, y, z):
    # No docstring, complex logic
    if x > 0:
        if y > 0:
            if z > 0:
                return x + y + z
    return 0
''')
            temp_path = Path(f.name)
        
        try:
            config = Config(complexity_threshold=5)
            scanner = CodeScanner(config)
            result = scanner.scan_file(temp_path)
            
            assert result.total_functions == 2
            assert len(result.violations) >= 1  # complex_func should be a violation
        finally:
            temp_path.unlink()


class TestScanResults:
    """Test cases for ScanResults"""
    
    def test_has_violations(self):
        """Test violation detection"""
        from cognitive_guard.core.complexity import ComplexityResult
        
        violation = ComplexityResult("func", 1, 15, False)
        file_result = FileResult("test.py", violations=[violation])
        results = ScanResults(files=[file_result])
        
        assert results.has_violations() is True
    
    def test_coverage_calculation(self):
        """Test coverage calculation"""
        from cognitive_guard.core.complexity import ComplexityResult
        
        func1 = ComplexityResult("func1", 1, 5, True)  # documented
        func2 = ComplexityResult("func2", 10, 5, False)  # not documented
        
        file_result = FileResult("test.py", functions=[func1, func2])
        results = ScanResults(files=[file_result])
        
        assert results.get_coverage() == 0.5
    
    def test_empty_results(self):
        """Test empty scan results"""
        results = ScanResults(files=[])
        
        assert results.has_violations() is False
        assert results.get_coverage() == 1.0
        assert results.get_total_violations() == 0
