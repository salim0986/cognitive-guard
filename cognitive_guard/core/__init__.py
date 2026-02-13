"""Configuration management for Cognitive Guard"""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class GamificationSettings(BaseModel):
    """Gamification feature settings"""

    enabled: bool = True
    show_achievements: bool = True
    track_stats: bool = True


class Config(BaseModel):
    """Main configuration for Cognitive Guard"""

    complexity_threshold: int = Field(
        default=10,
        ge=1,
        le=20,
        description="Cognitive complexity threshold for requiring documentation",
    )
    target_coverage: float = Field(
        default=0.9, ge=0.0, le=1.0, description="Target documentation coverage (0.0-1.0)"
    )
    languages: list[str] = Field(
        default=["python", "javascript", "typescript", "java"], description="Languages to analyze"
    )
    ignore: list[str] = Field(
        default=["**/test_*.py", "**/*.test.js", "**/migrations/**"],
        description="Patterns to ignore",
    )
    gamification: GamificationSettings = Field(
        default_factory=GamificationSettings, description="Gamification settings"
    )

    @classmethod
    def create_default(cls) -> "Config":
        """Create default configuration"""
        return cls()

    @classmethod
    def load(cls, path: Path | None = None) -> "Config":
        """Load configuration from file"""
        if path is None:
            path = Path.cwd() / ".cognitive-guard.yml"

        if not path.exists():
            raise FileNotFoundError(f"Configuration not found: {path}")

        with open(path) as f:
            data = yaml.safe_load(f)

        return cls(**data)

    def save(self, path: Path) -> None:
        """Save configuration to file"""
        data = self.model_dump()

        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return self.model_dump()
