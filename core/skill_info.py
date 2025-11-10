"""
Skill Info Module
Represents a single skill with all its information
"""

from pathlib import Path
from typing import Optional
from datetime import datetime
import json


class SkillInfo:
    def __init__(self, path: str, discovered_info: dict = None):
        """
        Initialize SkillInfo

        Args:
            path: Path to skill directory
            discovered_info: Optional pre-discovered info
        """
        self.path = Path(path)
        self.name = self.path.name
        self.metadata = self.load_metadata()

        # Merge discovered info if provided (but skip method names)
        if discovered_info:
            for key, value in discovered_info.items():
                if key not in ['has_metadata']:  # Skip conflicting keys
                    setattr(self, key, value)

    def load_metadata(self) -> dict:
        """Load metadata if exists"""
        metadata_file = self.path / ".skill_metadata.json"

        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass

        return {}

    def get_version(self) -> str:
        """Get skill version"""
        return self.metadata.get('version', 'Unknown')

    def get_last_updated(self) -> str:
        """Get last update timestamp"""
        last_updated = self.metadata.get('last_updated', 'Unknown')

        if last_updated != 'Unknown':
            try:
                dt = datetime.fromisoformat(last_updated)
                return dt.strftime('%Y-%m-%d')
            except:
                pass

        return 'Unknown'

    def get_age_days(self) -> Optional[int]:
        """Get age in days since last update"""
        last_updated = self.metadata.get('last_updated')

        if last_updated:
            try:
                dt = datetime.fromisoformat(last_updated)
                age = (datetime.now() - dt).days
                return age
            except:
                pass

        return None

    def get_status_emoji(self) -> str:
        """Get status emoji based on age and quality"""
        age = self.get_age_days()

        if age is None:
            return "⚠️"
        elif age > 90:
            return "🔴"  # Very old
        elif age > 30:
            return "🟡"  # Needs attention
        else:
            return "🟢"  # Recent

    def get_quality_score(self) -> Optional[float]:
        """Get quality score if available"""
        stats = self.metadata.get('stats', {})
        return stats.get('quality_score')

    def has_metadata(self) -> bool:
        """Check if skill has metadata"""
        return bool(self.metadata)

    def get_stats(self) -> dict:
        """Get skill statistics"""
        stats = self.metadata.get('stats', {})

        return {
            'total_pages': stats.get('total_pages', 0),
            'total_links': stats.get('total_links', 0),
            'total_code_blocks': stats.get('total_code_blocks', 0),
            'quality_score': stats.get('quality_score'),
        }

    def get_summary(self) -> str:
        """Get one-line summary"""
        version = self.get_version()
        age = self.get_age_days()
        age_str = f"{age}d ago" if age else "Unknown age"
        quality = self.get_quality_score()
        quality_str = f"{quality}/10" if quality else "No score"
        status = self.get_status_emoji()

        return f"{status} {self.name} (v{version}) - {quality_str} - Updated {age_str}"

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'path': str(self.path),
            'version': self.get_version(),
            'last_updated': self.get_last_updated(),
            'age_days': self.get_age_days(),
            'quality_score': self.get_quality_score(),
            'has_metadata': self.has_metadata(),
            'stats': self.get_stats()
        }
