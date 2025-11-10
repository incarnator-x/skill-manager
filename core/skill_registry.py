"""
Skill Registry Module
Manages collection of discovered skills
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from .skill_info import SkillInfo
from .skill_discovery import SkillDiscovery


class SkillRegistry:
    def __init__(self, config_file: str = None):
        """
        Initialize SkillRegistry

        Args:
            config_file: Optional config file path
        """
        self.config_file = Path(config_file) if config_file else Path.home() / ".skill_manager" / "config.json"
        self.skills: List[SkillInfo] = []
        self.search_paths = []

        self.load_config()

    def load_config(self):
        """Load configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.search_paths = config.get('search_paths', [])
            except Exception:
                pass

    def save_config(self):
        """Save configuration"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)

        config = {
            'search_paths': self.search_paths,
            'last_scan': None
        }

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

    def add_search_path(self, path: str):
        """Add search path"""
        if path not in self.search_paths:
            self.search_paths.append(path)
            self.save_config()

    def scan_for_skills(self):
        """Scan all search paths for skills"""
        if not self.search_paths:
            return

        discovery = SkillDiscovery(self.search_paths)
        discovered = discovery.discover_all()

        self.skills = [SkillInfo(skill['path'], skill) for skill in discovered]

    def get_all_skills(self) -> List[SkillInfo]:
        """Get all skills"""
        return self.skills

    def get_skill_by_name(self, name: str) -> Optional[SkillInfo]:
        """Get skill by name"""
        for skill in self.skills:
            if skill.name == name:
                return skill
        return None

    def get_outdated_skills(self, max_age_days: int = 30) -> List[SkillInfo]:
        """Get skills older than specified days"""
        outdated = []

        for skill in self.skills:
            age = skill.get_age_days()
            if age and age > max_age_days:
                outdated.append(skill)

        return outdated

    def get_skills_without_metadata(self) -> List[SkillInfo]:
        """Get skills without metadata"""
        return [skill for skill in self.skills if not skill.has_metadata()]

    def get_statistics(self) -> Dict:
        """Get overall statistics"""
        total = len(self.skills)
        with_metadata = len([s for s in self.skills if s.has_metadata()])

        # Average quality score
        scores = [s.get_quality_score() for s in self.skills if s.get_quality_score()]
        avg_score = sum(scores) / len(scores) if scores else 0

        # Outdated count
        outdated = len(self.get_outdated_skills(30))

        return {
            'total_skills': total,
            'with_metadata': with_metadata,
            'without_metadata': total - with_metadata,
            'avg_quality_score': round(avg_score, 1),
            'outdated_skills': outdated
        }

    def sort_by_age(self, reverse: bool = False):
        """Sort skills by age"""
        self.skills.sort(key=lambda s: s.get_age_days() or 999999, reverse=reverse)

    def sort_by_quality(self, reverse: bool = True):
        """Sort skills by quality score"""
        self.skills.sort(key=lambda s: s.get_quality_score() or 0, reverse=reverse)

    def sort_by_name(self):
        """Sort skills by name"""
        self.skills.sort(key=lambda s: s.name)
