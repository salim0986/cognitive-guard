"""Statistics tracking and achievements"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cognitive_guard.core.config import Config


@dataclass
class Achievement:
    """Represents an unlocked achievement"""
    
    id: str
    name: str
    description: str
    icon: str
    unlocked_at: str | None = None
    
    def is_unlocked(self) -> bool:
        return self.unlocked_at is not None


@dataclass
class Stats:
    """User statistics"""
    
    total_functions_documented: int = 0
    total_commits_with_guard: int = 0
    highest_complexity_documented: int = 0
    current_streak_days: int = 0
    achievements: List[Achievement] = field(default_factory=list)
    last_activity: str | None = None
    
    def to_dict(self) -> Dict:
        return {
            "total_functions_documented": self.total_functions_documented,
            "total_commits_with_guard": self.total_commits_with_guard,
            "highest_complexity_documented": self.highest_complexity_documented,
            "current_streak_days": self.current_streak_days,
            "achievements": [
                {
                    "id": a.id,
                    "name": a.name,
                    "description": a.description,
                    "icon": a.icon,
                    "unlocked_at": a.unlocked_at
                }
                for a in self.achievements
            ],
            "last_activity": self.last_activity
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Stats":
        achievements = [
            Achievement(**a) for a in data.get("achievements", [])
        ]
        return cls(
            total_functions_documented=data.get("total_functions_documented", 0),
            total_commits_with_guard=data.get("total_commits_with_guard", 0),
            highest_complexity_documented=data.get("highest_complexity_documented", 0),
            current_streak_days=data.get("current_streak_days", 0),
            achievements=achievements,
            last_activity=data.get("last_activity")
        )


class StatsTracker:
    """Tracks and displays user statistics and achievements"""
    
    ACHIEVEMENTS = [
        Achievement("first_steps", "📝 First Steps", "Document your first complex function", "📝"),
        Achievement("marksman", "🎯 Marksman", "Achieve 90% documentation coverage", "🎯"),
        Achievement("mind_reader", "🧠 Mind Reader", "Document 10 functions with Score > 15", "🧠"),
        Achievement("speed_demon", "🚀 Speed Demon", "Document 5 functions in one session", "🚀"),
        Achievement("perfectionist", "💯 Perfectionist", "Achieve 100% documentation coverage", "💯"),
    ]
    
    def __init__(self, config: Config):
        self.config = config
        self.stats_file = Path.cwd() / ".cognitive-guard" / "stats.json"
        self.stats = self._load_stats()
    
    def _load_stats(self) -> Stats:
        """Load statistics from file"""
        if not self.stats_file.exists():
            return Stats(achievements=self.ACHIEVEMENTS.copy())
        
        try:
            with open(self.stats_file, "r") as f:
                data = json.load(f)
            return Stats.from_dict(data)
        except Exception:
            return Stats(achievements=self.ACHIEVEMENTS.copy())
    
    def save(self) -> None:
        """Save statistics to file"""
        self.stats_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.stats_file, "w") as f:
            json.dump(self.stats.to_dict(), f, indent=2)
    
    def record_documentation(self, complexity: int) -> None:
        """Record a documented function"""
        self.stats.total_functions_documented += 1
        self.stats.highest_complexity_documented = max(
            self.stats.highest_complexity_documented,
            complexity
        )
        self.stats.last_activity = datetime.now().isoformat()
        self._check_achievements()
        self.save()
    
    def record_commit(self) -> None:
        """Record a commit with Cognitive Guard"""
        self.stats.total_commits_with_guard += 1
        self.stats.last_activity = datetime.now().isoformat()
        self.save()
    
    def _check_achievements(self) -> None:
        """Check and unlock achievements"""
        # First Steps
        if self.stats.total_functions_documented >= 1:
            self._unlock_achievement("first_steps")
        
        # Marksman - This would need coverage data
        # Mind Reader
        if self.stats.highest_complexity_documented > 15:
            # Count from history, simplified here
            self._unlock_achievement("mind_reader")
    
    def _unlock_achievement(self, achievement_id: str) -> None:
        """Unlock an achievement"""
        for achievement in self.stats.achievements:
            if achievement.id == achievement_id and not achievement.is_unlocked():
                achievement.unlocked_at = datetime.now().isoformat()
    
    def display(self, console: Console) -> None:
        """Display statistics and achievements"""
        
        # Stats panel
        stats_text = f"""
[bold]📊 Your Documentation Journey[/bold]

Functions Documented: {self.stats.total_functions_documented}
Commits with Guard: {self.stats.total_commits_with_guard}
Highest Complexity: {self.stats.highest_complexity_documented}
Current Streak: {self.stats.current_streak_days} days
        """.strip()
        
        console.print(Panel(stats_text, title="Statistics", border_style="green"))
        
        # Achievements table
        table = Table(title="\n🏆 Achievements", show_header=True)
        table.add_column("Icon", justify="center")
        table.add_column("Achievement")
        table.add_column("Status", justify="center")
        
        for achievement in self.stats.achievements:
            status = "✅ Unlocked" if achievement.is_unlocked() else "🔒 Locked"
            style = "green" if achievement.is_unlocked() else "dim"
            
            table.add_row(
                achievement.icon,
                f"[{style}]{achievement.name}[/]\n[dim]{achievement.description}[/]",
                status
            )
        
        console.print(table)
