"""Code scanner for analyzing files and detecting violations"""

import fnmatch
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

from git import Repo
from rich.console import Console
from rich.table import Table

from cognitive_guard.core.complexity import ComplexityAnalyzer, ComplexityResult
from cognitive_guard.core.config import Config


@dataclass
class FileResult:
    """Results for a single file"""
    
    file_path: str
    functions: List[ComplexityResult] = field(default_factory=list)
    violations: List[ComplexityResult] = field(default_factory=list)
    
    @property
    def total_functions(self) -> int:
        return len(self.functions)
    
    @property
    def documented_functions(self) -> int:
        return sum(1 for f in self.functions if f.has_docstring)
    
    @property
    def coverage(self) -> float:
        if self.total_functions == 0:
            return 1.0
        return self.documented_functions / self.total_functions


@dataclass
class ScanResults:
    """Aggregated scan results"""
    
    files: List[FileResult] = field(default_factory=list)
    config: Config | None = None
    
    def has_violations(self) -> bool:
        """Check if any violations exist"""
        return any(file.violations for file in self.files)
    
    def get_coverage(self) -> float:
        """Calculate overall documentation coverage"""
        total = sum(file.total_functions for file in self.files)
        documented = sum(file.documented_functions for file in self.files)
        
        if total == 0:
            return 1.0
        return documented / total
    
    def get_total_violations(self) -> int:
        """Get total number of violations"""
        return sum(len(file.violations) for file in self.files)
    
    def display(self, console: Console) -> None:
        """Display results in a pretty table"""
        
        if not self.files:
            console.print("[yellow]No files analyzed[/yellow]")
            return
        
        # Summary statistics
        total_functions = sum(file.total_functions for file in self.files)
        total_violations = self.get_total_violations()
        coverage = self.get_coverage()
        
        console.print(f"\n[bold]📊 Scan Results[/bold]\n")
        console.print(f"Files analyzed: {len(self.files)}")
        console.print(f"Total functions: {total_functions}")
        console.print(f"Documentation coverage: [{'green' if coverage >= 0.9 else 'yellow'}]{coverage:.1%}[/]")
        console.print(f"Violations: [{'red' if total_violations > 0 else 'green'}]{total_violations}[/]\n")
        
        if total_violations > 0:
            table = Table(title="🚫 Documentation Violations", show_header=True)
            table.add_column("File", style="cyan")
            table.add_column("Function", style="yellow")
            table.add_column("Line", style="dim")
            table.add_column("Score", justify="right")
            table.add_column("Severity", justify="center")
            
            for file_result in self.files:
                for violation in file_result.violations:
                    table.add_row(
                        file_result.file_path,
                        violation.name,
                        str(violation.line_number),
                        str(violation.complexity),
                        f"{violation.emoji} {violation.severity}"
                    )
            
            console.print(table)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert results to dictionary"""
        return {
            "total_files": len(self.files),
            "total_functions": sum(file.total_functions for file in self.files),
            "coverage": self.get_coverage(),
            "violations": self.get_total_violations(),
            "files": [
                {
                    "path": file.file_path,
                    "functions": file.total_functions,
                    "documented": file.documented_functions,
                    "violations": [
                        {
                            "function": v.name,
                            "line": v.line_number,
                            "complexity": v.complexity,
                            "severity": v.severity
                        }
                        for v in file.violations
                    ]
                }
                for file in self.files
            ]
        }


class CodeScanner:
    """Scans code files and detects documentation violations"""
    
    def __init__(self, config: Config):
        self.config = config
        self.analyzer = ComplexityAnalyzer()
    
    def should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored"""
        path_str = str(path)
        for pattern in self.config.ignore:
            if fnmatch.fnmatch(path_str, pattern):
                return True
        return False
    
    def scan_file(self, file_path: Path) -> FileResult:
        """Scan a single file for violations"""
        results = self.analyzer.analyze_file(str(file_path))
        
        violations = [
            result for result in results
            if result.complexity > self.config.complexity_threshold
            and not result.has_docstring
        ]
        
        return FileResult(
            file_path=str(file_path),
            functions=results,
            violations=violations
        )
    
    def scan_staged(self) -> ScanResults:
        """Scan only staged files in git"""
        try:
            repo = Repo(Path.cwd(), search_parent_directories=True)
        except Exception:
            return ScanResults(config=self.config)
        
        staged_files = [item.a_path for item in repo.index.diff("HEAD")]
        
        file_results: List[FileResult] = []
        
        for file_path in staged_files:
            path = Path(file_path)
            
            if not path.exists() or self.should_ignore(path):
                continue
            
            if path.suffix == ".py":  # Currently only Python
                result = self.scan_file(path)
                if result.functions:  # Only include files with functions
                    file_results.append(result)
        
        return ScanResults(files=file_results, config=self.config)
    
    def scan_all(self) -> ScanResults:
        """Scan all files in the project"""
        file_results: List[FileResult] = []
        
        # For now, only scan Python files
        for py_file in Path.cwd().rglob("*.py"):
            if self.should_ignore(py_file):
                continue
            
            result = self.scan_file(py_file)
            if result.functions:
                file_results.append(result)
        
        return ScanResults(files=file_results, config=self.config)
