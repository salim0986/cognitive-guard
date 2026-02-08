"""Test fixtures for Cognitive Guard tests"""

import pytest
from pathlib import Path
import tempfile

from cognitive_guard.core.config import Config


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def default_config():
    """Create a default configuration for tests"""
    return Config.create_default()


@pytest.fixture
def sample_python_file(temp_dir):
    """Create a sample Python file for testing"""
    file_path = temp_dir / "sample.py"
    
    content = '''
def simple_function():
    """A simple documented function"""
    return 42

def complex_function(a, b, c, d):
    # Missing docstring
    result = 0
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    result = a + b + c + d
                else:
                    result = a + b + c
            else:
                result = a + b
        else:
            result = a
    return result
'''
    
    file_path.write_text(content)
    return file_path


@pytest.fixture
def sample_config_file(temp_dir):
    """Create a sample configuration file"""
    config_path = temp_dir / ".cognitive-guard.yml"
    config = Config.create_default()
    config.save(config_path)
    return config_path
