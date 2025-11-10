"""
Bulk Operations Module
Performs operations on multiple skills at once
"""

import subprocess
from pathlib import Path
from typing import List, Dict
from .skill_info import SkillInfo


class BulkOperations:
    def __init__(self, quality_checker_path: str = None, updater_path: str = None):
        """
        Initialize BulkOperations

        Args:
            quality_checker_path: Path to skill-quality-checker
            updater_path: Path to skill-updater
        """
        self.quality_checker_path = quality_checker_path
        self.updater_path = updater_path

    def check_quality_all(self, skills: List[SkillInfo]) -> Dict:
        """
        Run quality check on all skills

        Args:
            skills: List of skills to check

        Returns:
            Results dictionary
        """
        if not self.quality_checker_path:
            return {'error': 'Quality checker path not configured'}

        results = []

        print(f"\n🔍 Running quality checks on {len(skills)} skills...\n")

        for i, skill in enumerate(skills, 1):
            print(f"   [{i}/{len(skills)}] Checking {skill.name}...", end='')

            try:
                cmd = [
                    'python',
                    str(Path(self.quality_checker_path) / 'skill_quality_checker.py'),
                    str(skill.path),
                    '--skip-ai'
                ]

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300
                )

                # Parse score from output (simplified)
                score = None
                for line in result.stdout.split('\n'):
                    if 'Overall Score:' in line:
                        try:
                            score = float(line.split(':')[1].split('/')[0].strip())
                        except:
                            pass

                results.append({
                    'skill': skill.name,
                    'success': result.returncode == 0,
                    'score': score
                })

                if score:
                    print(f" ✅ Score: {score}/10")
                else:
                    print(f" ⚠️ Completed")

            except subprocess.TimeoutExpired:
                results.append({
                    'skill': skill.name,
                    'success': False,
                    'error': 'Timeout'
                })
                print(f" ❌ Timeout")

            except Exception as e:
                results.append({
                    'skill': skill.name,
                    'success': False,
                    'error': str(e)
                })
                print(f" ❌ Error: {e}")

        return {'results': results}

    def check_updates_all(self, skills: List[SkillInfo]) -> Dict:
        """
        Check for updates on all skills

        Args:
            skills: List of skills to check

        Returns:
            Results dictionary
        """
        if not self.updater_path:
            return {'error': 'Updater path not configured'}

        results = []

        print(f"\n🔄 Checking updates for {len(skills)} skills...\n")

        for i, skill in enumerate(skills, 1):
            # Skip skills without metadata
            if not skill.has_metadata():
                print(f"   [{i}/{len(skills)}] {skill.name} ⏭️  (No metadata)")
                results.append({
                    'skill': skill.name,
                    'has_updates': False,
                    'skipped': True
                })
                continue

            print(f"   [{i}/{len(skills)}] Checking {skill.name}...", end='')

            try:
                cmd = [
                    'python',
                    str(Path(self.updater_path) / 'skill_updater.py'),
                    str(skill.path),
                    '--check-updates'
                ]

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120
                )

                # Parse output for updates
                has_updates = 'Updates available' in result.stdout

                results.append({
                    'skill': skill.name,
                    'success': True,
                    'has_updates': has_updates
                })

                if has_updates:
                    print(f" 📝 Updates available")
                else:
                    print(f" ✅ Up to date")

            except Exception as e:
                results.append({
                    'skill': skill.name,
                    'success': False,
                    'error': str(e)
                })
                print(f" ❌ Error")

        return {'results': results}

    def update_all(self, skills: List[SkillInfo], dry_run: bool = False) -> Dict:
        """
        Update all skills with available updates

        Args:
            skills: List of skills to update
            dry_run: If True, simulate without making changes

        Returns:
            Results dictionary
        """
        if not self.updater_path:
            return {'error': 'Updater path not configured'}

        print(f"\n🔄 Updating {len(skills)} skills...\n")

        if dry_run:
            print("   (DRY RUN MODE - No actual changes)\n")

        results = []

        for i, skill in enumerate(skills, 1):
            if not skill.has_metadata():
                print(f"   [{i}/{len(skills)}] {skill.name} ⏭️  (No metadata)")
                continue

            print(f"   [{i}/{len(skills)}] Updating {skill.name}...")

            try:
                cmd = [
                    'python',
                    str(Path(self.updater_path) / 'skill_updater.py'),
                    str(skill.path),
                    '--update'
                ]

                if dry_run:
                    cmd.append('--dry-run')

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=600
                )

                results.append({
                    'skill': skill.name,
                    'success': result.returncode == 0
                })

                if result.returncode == 0:
                    print(f"      ✅ Updated successfully")
                else:
                    print(f"      ⚠️ Update failed")

            except Exception as e:
                results.append({
                    'skill': skill.name,
                    'success': False,
                    'error': str(e)
                })
                print(f"      ❌ Error: {e}")

        return {'results': results}

    def init_metadata_all(self, skills: List[SkillInfo]) -> Dict:
        """
        Initialize metadata for skills that don't have it

        Args:
            skills: List of skills

        Returns:
            Results dictionary
        """
        skills_without_metadata = [s for s in skills if not s.has_metadata()]

        if not skills_without_metadata:
            print("\n✅ All skills already have metadata")
            return {'results': []}

        print(f"\n📝 Initializing metadata for {len(skills_without_metadata)} skills...\n")

        results = []

        for i, skill in enumerate(skills_without_metadata, 1):
            print(f"   [{i}/{len(skills_without_metadata)}] {skill.name}...", end='')

            try:
                cmd = [
                    'python',
                    str(Path(self.updater_path) / 'skill_updater.py'),
                    str(skill.path),
                    '--init-metadata'
                ]

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                results.append({
                    'skill': skill.name,
                    'success': result.returncode == 0
                })

                print(" ✅")

            except Exception as e:
                results.append({
                    'skill': skill.name,
                    'success': False,
                    'error': str(e)
                })
                print(f" ❌")

        return {'results': results}
