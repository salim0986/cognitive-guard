"""Integration tests for the CLI"""

import os
import tempfile
from pathlib import Path

from click.testing import CliRunner

from cognitive_guard.cli import main


class TestCLI:
    """Integration tests for CLI commands"""

    def test_version(self):
        """Test version command"""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0

    def test_init_command(self):
        """Test init command"""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            runner.invoke(main, ["init"])

            # Check if config file was created
            config_path = Path(tmpdir) / ".cognitive-guard.yml"
            assert config_path.exists()

    def test_check_without_init(self):
        """Test check command without initialization"""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            result = runner.invoke(main, ["check"])
            assert result.exit_code == 1
            assert "No .cognitive-guard.yml found" in result.output
