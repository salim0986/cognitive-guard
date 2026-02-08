"""
Cognitive Guard - Gamified Code Documentation Enforcer

A CLI tool that analyzes cognitive complexity of your code and enforces
documentation where it matters most.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__license__ = "MIT"

from cognitive_guard.core.complexity import ComplexityAnalyzer
from cognitive_guard.core.config import Config

__all__ = ["ComplexityAnalyzer", "Config", "__version__"]
