#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Manager
Central dashboard for managing Claude AI skills

Usage:
    python skill_manager.py                    # Show dashboard
    python skill_manager.py --add-path <path>  # Add search path
    python skill_manager.py --scan             # Rescan for skills
    python skill_manager.py --check-quality    # Check quality of all skills
    python skill_manager.py --check-updates    # Check for updates
"""

import argparse
import sys
import os
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'ignore')

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.skill_registry import SkillRegistry
from core.bulk_operations import BulkOperations
from ui.dashboard import Dashboard


class SkillManager:
    def __init__(self, config_file: str = None):
        """
        Initialize Skill Manager

        Args:
            config_file: Optional config file path
        """
        self.config_file = config_file
        self.registry = SkillRegistry(config_file)
        self.dashboard = Dashboard(self.registry)
        self.bulk_ops = None

    def setup_integrations(self, quality_checker_path: str = None, updater_path: str = None):
        """
        Setup tool integrations

        Args:
            quality_checker_path: Path to skill-quality-checker
            updater_path: Path to skill-updater
        """
        self.bulk_ops = BulkOperations(quality_checker_path, updater_path)

    def show_dashboard(self, interactive=False):
        """
        Show dashboard

        Args:
            interactive: If True, run interactive mode
        """
        if interactive:
            self.dashboard.run_interactive(self)
        else:
            self.dashboard.show(interactive=False)

    def add_search_path(self, path: str):
        """
        Add search path and scan

        Args:
            path: Path to add
        """
        print(f"\n📁 Adding search path: {path}")

        if not Path(path).exists():
            print(f"❌ Path does not exist: {path}")
            return

        self.registry.add_search_path(path)
        print(f"✅ Search path added")

        # Rescan
        self.scan_for_skills()

    def scan_for_skills(self):
        """Scan for skills"""
        print(f"\n🔍 Scanning for skills...")

        self.registry.scan_for_skills()
        skills = self.registry.get_all_skills()

        print(f"✅ Found {len(skills)} skills")

        if skills:
            print(f"\nSkills found:")
            for skill in skills:
                print(f"   • {skill.name} ({skill.path})")

    def show_skill_details(self, skill_name: str):
        """
        Show detailed information about a skill

        Args:
            skill_name: Name of skill
        """
        self.dashboard.show_skill_details(skill_name)

    def check_quality_all(self):
        """Check quality of all skills"""
        if not self.bulk_ops:
            print("\n❌ Bulk operations not configured")
            print("   Set tool paths with --quality-checker and --updater")
            return

        skills = self.registry.get_all_skills()

        if not skills:
            print("\n❌ No skills found")
            return

        results = self.bulk_ops.check_quality_all(skills)

        # Summary
        if 'results' in results:
            successful = [r for r in results['results'] if r.get('success')]
            print(f"\n✅ Checked {len(successful)}/{len(skills)} skills")

    def check_updates_all(self):
        """Check for updates on all skills"""
        if not self.bulk_ops:
            print("\n❌ Bulk operations not configured")
            print("   Set updater path with --updater")
            return

        skills = self.registry.get_all_skills()

        if not skills:
            print("\n❌ No skills found")
            return

        results = self.bulk_ops.check_updates_all(skills)

        # Summary
        if 'results' in results:
            needs_update = [r for r in results['results'] if r.get('has_updates')]
            print(f"\n📝 {len(needs_update)} skills have updates available")

    def update_all(self, dry_run: bool = False):
        """Update all skills"""
        if not self.bulk_ops:
            print("\n❌ Bulk operations not configured")
            return

        skills = self.registry.get_all_skills()

        if not skills:
            print("\n❌ No skills found")
            return

        results = self.bulk_ops.update_all(skills, dry_run=dry_run)

        # Summary
        if 'results' in results:
            successful = [r for r in results['results'] if r.get('success')]
            print(f"\n✅ Updated {len(successful)}/{len(skills)} skills")

    def init_metadata_all(self):
        """Initialize metadata for all skills"""
        if not self.bulk_ops:
            print("\n❌ Bulk operations not configured")
            return

        skills = self.registry.get_all_skills()

        if not skills:
            print("\n❌ No skills found")
            return

        results = self.bulk_ops.init_metadata_all(skills)

    def generate_report(self, output_file: str = None):
        """Generate markdown report"""
        skills = self.registry.get_all_skills()
        stats = self.registry.get_statistics()

        report = "# Skill Manager Report\n\n"
        report += f"**Generated**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

        report += "## Summary\n\n"
        report += f"- Total Skills: {stats['total_skills']}\n"
        report += f"- With Metadata: {stats['with_metadata']}\n"
        report += f"- Without Metadata: {stats['without_metadata']}\n"
        report += f"- Avg Quality Score: {stats['avg_quality_score']}/10\n"
        report += f"- Outdated Skills: {stats['outdated_skills']}\n\n"

        report += "## Skills\n\n"
        for skill in skills:
            report += f"### {skill.name}\n\n"
            report += f"- Version: v{skill.get_version()}\n"
            report += f"- Last Updated: {skill.get_last_updated()}\n"

            quality = skill.get_quality_score()
            if quality:
                report += f"- Quality Score: {quality}/10\n"

            report += f"- Status: {skill.get_status_emoji()}\n\n"

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Report saved to: {output_file}")
        else:
            print(report)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Skill Manager - Central dashboard for Claude AI skills',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show dashboard
  python skill_manager.py

  # Add search path
  python skill_manager.py --add-path /path/to/Skill_Seekers/output/

  # Rescan for skills
  python skill_manager.py --scan

  # Setup integrations and check quality
  python skill_manager.py --quality-checker ../skill-quality-checker --check-quality

  # Check for updates
  python skill_manager.py --updater ../skill-updater --check-updates

  # Generate report
  python skill_manager.py --report skills_report.md
        """
    )

    parser.add_argument('--add-path', type=str,
                       help='Add search path for skills')
    parser.add_argument('--scan', action='store_true',
                       help='Rescan for skills')
    parser.add_argument('--skill', type=str,
                       help='Show details for specific skill')
    parser.add_argument('--check-quality', action='store_true',
                       help='Check quality of all skills')
    parser.add_argument('--check-updates', action='store_true',
                       help='Check for updates on all skills')
    parser.add_argument('--update-all', action='store_true',
                       help='Update all skills')
    parser.add_argument('--init-metadata', action='store_true',
                       help='Initialize metadata for all skills')
    parser.add_argument('--report', type=str, metavar='FILE',
                       help='Generate markdown report')
    parser.add_argument('--quality-checker', type=str,
                       help='Path to skill-quality-checker')
    parser.add_argument('--updater', type=str,
                       help='Path to skill-updater')
    parser.add_argument('--config', type=str,
                       help='Config file path')
    parser.add_argument('--dry-run', action='store_true',
                       help='Simulate operations without making changes')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Run interactive dashboard mode')

    args = parser.parse_args()

    try:
        manager = SkillManager(args.config)

        # Setup integrations if provided
        if args.quality_checker or args.updater:
            manager.setup_integrations(args.quality_checker, args.updater)

        # Load existing skills
        manager.scan_for_skills()

        # Execute requested action
        if args.add_path:
            manager.add_search_path(args.add_path)
        elif args.scan:
            manager.scan_for_skills()
        elif args.skill:
            manager.show_skill_details(args.skill)
        elif args.check_quality:
            manager.check_quality_all()
        elif args.check_updates:
            manager.check_updates_all()
        elif args.update_all:
            manager.update_all(dry_run=args.dry_run)
        elif args.init_metadata:
            manager.init_metadata_all()
        elif args.report:
            manager.generate_report(args.report)
        else:
            # Default: show dashboard
            manager.show_dashboard(interactive=args.interactive)

    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
