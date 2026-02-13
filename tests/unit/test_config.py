"""Tests for configuration management"""

import tempfile
from pathlib import Path

import pytest

from cognitive_guard.core.config import Config, GamificationSettings


class TestConfig:
    """Test cases for Config"""

    def test_default_config(self):
        """Test default configuration creation"""
        config = Config.create_default()

        assert config.complexity_threshold == 10
        assert config.target_coverage == 0.9
        assert "python" in config.languages
        assert config.gamification.enabled is True

    def test_save_and_load(self):
        """Test saving and loading configuration"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "test.yml"

            # Create and save
            config = Config(
                complexity_threshold=15,
                target_coverage=0.95,
                languages=["python"],
            )
            config.save(config_path)

            # Load and verify
            loaded = Config.load(config_path)
            assert loaded.complexity_threshold == 15
            assert loaded.target_coverage == 0.95
            assert loaded.languages == ["python"]

    def test_load_nonexistent_file(self):
        """Test loading non-existent config file"""
        with pytest.raises(FileNotFoundError):
            Config.load(Path("/nonexistent/path.yml"))

    def test_gamification_settings(self):
        """Test gamification settings"""
        settings = GamificationSettings(enabled=False, show_achievements=False, track_stats=True)

        config = Config(gamification=settings)
        assert config.gamification.enabled is False
        assert config.gamification.track_stats is True

    def test_config_to_dict(self):
        """Test configuration to dictionary conversion"""
        config = Config.create_default()
        data = config.to_dict()

        assert isinstance(data, dict)
        assert "complexity_threshold" in data
        assert "gamification" in data
