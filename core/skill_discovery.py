"""
Skill Discovery Module
Automatically discovers Claude AI skills in specified directories
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class SkillDiscovery:
    def __init__(self, search_paths: List[str] = None):
        """
        Initialize SkillDiscovery

        Args:
            search_paths: List of paths to search for skills
        """
        self.search_paths = [Path(p) for p in search_paths] if search_paths else []

    def is_skill_directory(self, path: Path) -> bool:
        """
        Check if directory contains a valid skill

        Args:
            path: Path to check

        Returns:
            True if valid skill directory
        """
        # Check for SKILL.md
        if not (path / "SKILL.md").exists():
            return False

        # Check for references directory
        if not (path / "references").exists():
            return False

        return True

    def get_skill_info(self, skill_path: Path) -> Dict:
        """
        Extract basic info from a skill

        Args:
            skill_path: Path to skill directory

        Returns:
            Skill info dictionary
        """
        info = {
            'name': skill_path.name,
            'path': str(skill_path.absolute()),
            'has_metadata': (skill_path / ".skill_metadata.json").exists(),
            'skill_md_size': 0,
            'reference_count': 0,
            'last_modified': None
        }

        # Get SKILL.md size
        skill_md = skill_path / "SKILL.md"
        if skill_md.exists():
            info['skill_md_size'] = skill_md.stat().st_size
            info['last_modified'] = datetime.fromtimestamp(skill_md.stat().st_mtime).isoformat()

        # Count references
        references_dir = skill_path / "references"
        if references_dir.exists():
            info['reference_count'] = len(list(references_dir.glob("*.md")))

        # Load metadata if exists
        if info['has_metadata']:
            try:
                metadata_file = skill_path / ".skill_metadata.json"
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    info['version'] = metadata.get('version', 'Unknown')
                    info['created'] = metadata.get('created', 'Unknown')
                    info['last_updated'] = metadata.get('last_updated', 'Unknown')
            except Exception:
                pass

        return info

    def scan_directory(self, path: Path) -> List[Dict]:
        """
        Scan a directory for skills

        Args:
            path: Directory to scan

        Returns:
            List of skill info dictionaries
        """
        skills = []

        if not path.exists() or not path.is_dir():
            return skills

        # Check if this directory itself is a skill
        if self.is_skill_directory(path):
            skills.append(self.get_skill_info(path))
            return skills

        # Check subdirectories
        for subdir in path.iterdir():
            if subdir.is_dir():
                if self.is_skill_directory(subdir):
                    skills.append(self.get_skill_info(subdir))

        return skills

    def discover_all(self) -> List[Dict]:
        """
        Discover all skills in search paths

        Returns:
            List of all discovered skills
        """
        all_skills = []

        for search_path in self.search_paths:
            skills = self.scan_directory(search_path)
            all_skills.extend(skills)

        return all_skills

    def add_search_path(self, path: str):
        """
        Add a new search path

        Args:
            path: Path to add
        """
        p = Path(path)
        if p not in self.search_paths:
            self.search_paths.append(p)


def discover_skills(search_paths: List[str]) -> List[Dict]:
    """
    Main function to discover skills

    Args:
        search_paths: List of paths to search

    Returns:
        List of discovered skills
    """
    discovery = SkillDiscovery(search_paths)
    skills = discovery.discover_all()

    return skills


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python skill_discovery.py <search_path> [search_path2] ...")
        sys.exit(1)

    search_paths = sys.argv[1:]
    skills = discover_skills(search_paths)

    print(f"\n{'='*60}")
    print(f"🔍 Skill Discovery")
    print(f"{'='*60}")
    print(f"Found {len(skills)} skills:\n")

    for skill in skills:
        print(f"📚 {skill['name']}")
        print(f"   Path: {skill['path']}")
        print(f"   References: {skill['reference_count']}")
        print(f"   Has metadata: {'✅' if skill['has_metadata'] else '❌'}")
        if 'version' in skill:
            print(f"   Version: v{skill['version']}")
        print()
