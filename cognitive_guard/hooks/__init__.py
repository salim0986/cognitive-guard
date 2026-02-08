"""Git hook installer and manager"""

import os
import stat
from pathlib import Path
from typing import Optional

from git import Repo


class HookInstaller:
    """Manages installation and updates of git pre-commit hook"""
    
    HOOK_SCRIPT = """#!/usr/bin/env python3
\"\"\"Cognitive Guard pre-commit hook\"\"\"

import sys
import subprocess

def main():
    result = subprocess.run(
        ["cognitive-guard", "hook"],
        capture_output=False
    )
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
"""
    
    def __init__(self):
        self.repo_path = self._find_repo()
    
    def _find_repo(self) -> Optional[Path]:
        """Find git repository root"""
        try:
            repo = Repo(Path.cwd(), search_parent_directories=True)
            return Path(repo.git_dir)
        except Exception:
            return None
    
    def _get_hook_path(self) -> Optional[Path]:
        """Get path to pre-commit hook"""
        if not self.repo_path:
            return None
        return self.repo_path / "hooks" / "pre-commit"
    
    def install(self) -> bool:
        """Install pre-commit hook"""
        hook_path = self._get_hook_path()
        
        if not hook_path:
            return False
        
        # Create hooks directory if it doesn't exist
        hook_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write hook script
        with open(hook_path, "w") as f:
            f.write(self.HOOK_SCRIPT)
        
        # Make executable
        st = os.stat(hook_path)
        os.chmod(hook_path, st.st_mode | stat.S_IEXEC)
        
        return True
    
    def update(self) -> bool:
        """Update existing hook"""
        hook_path = self._get_hook_path()
        
        if not hook_path or not hook_path.exists():
            return False
        
        return self.install()
    
    def is_installed(self) -> bool:
        """Check if hook is installed"""
        hook_path = self._get_hook_path()
        return hook_path is not None and hook_path.exists()
