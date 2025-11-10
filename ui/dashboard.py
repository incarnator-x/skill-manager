"""
Dashboard Module
Interactive terminal-based dashboard for viewing and managing skills
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.skill_registry import SkillRegistry


class Dashboard:
    def __init__(self, registry: SkillRegistry):
        """
        Initialize Dashboard

        Args:
            registry: SkillRegistry instance
        """
        self.registry = registry
        self.last_activity = []

    def clear_screen(self):
        """Clear terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Print dashboard header"""
        print("\n" + "="*70)
        print("🎛️  SKILL MANAGER DASHBOARD")
        print("="*70)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"📅 {now}")
        print("="*70)

    def print_skills_table(self):
        """Print table of skills"""
        skills = self.registry.get_all_skills()

        if not skills:
            print("\n📭 No skills found.")
            print("   Add search paths with: skill_manager.py --add-path /path/to/skills")
            return

        print(f"\n📚 Your Skills ({len(skills)} total)\n")
        print("="*70)

        for i, skill in enumerate(skills, 1):
            # Status emoji
            status = skill.get_status_emoji()

            # Name and version
            name = skill.name[:25]  # Truncate long names
            version = skill.get_version()

            # Quality score
            quality = skill.get_quality_score()
            quality_str = f"{quality:.1f}/10" if quality else "No score"

            # Age
            age = skill.get_age_days()
            if age is not None:
                if age == 0:
                    age_str = "Today"
                elif age == 1:
                    age_str = "Yesterday"
                elif age < 7:
                    age_str = f"{age}d ago"
                elif age < 30:
                    weeks = age // 7
                    age_str = f"{weeks}w ago"
                else:
                    months = age // 30
                    age_str = f"{months}mo ago"
            else:
                age_str = "No data"

            # Has metadata indicator
            metadata_icon = "✅" if skill.has_metadata() else "❌"

            print(f"{i:2}. {status} {name:<25} v{version:<8} {quality_str:>10} {metadata_icon}  📅 {age_str}")

        print("="*70)

    def print_enhanced_statistics(self):
        """Print enhanced statistics with more detail"""
        stats = self.registry.get_statistics()
        skills = self.registry.get_all_skills()

        # Calculate additional stats
        total_pages = sum(s.get_stats().get('total_pages', 0) for s in skills)
        total_links = sum(s.get_stats().get('total_links', 0) for s in skills)
        total_code = sum(s.get_stats().get('total_code_blocks', 0) for s in skills)

        # Quality distribution
        excellent = len([s for s in skills if s.get_quality_score() and s.get_quality_score() >= 9])
        good = len([s for s in skills if s.get_quality_score() and 7 <= s.get_quality_score() < 9])
        needs_work = len([s for s in skills if s.get_quality_score() and s.get_quality_score() < 7])
        no_score = len([s for s in skills if not s.get_quality_score()])

        print(f"\n📊 Statistics:\n")
        print(f"   📚 Content:")
        print(f"      • Total Skills: {stats['total_skills']}")
        print(f"      • Total Pages: {total_pages:,}")
        if total_links > 0:
            print(f"      • Total Links: {total_links:,}")
        if total_code > 0:
            print(f"      • Code Examples: {total_code:,}")

        print(f"\n   🏥 Health:")
        print(f"      • With Metadata: {stats['with_metadata']}/{stats['total_skills']}")

        if stats['avg_quality_score'] > 0:
            avg_score = stats['avg_quality_score']
            health_emoji = "💚" if avg_score >= 8 else "💛" if avg_score >= 7 else "❤️"
            print(f"      • Avg Quality: {avg_score}/10 {health_emoji}")

        if stats['outdated_skills'] > 0:
            print(f"      • Outdated: {stats['outdated_skills']} (>30 days)")

        # Quality distribution
        if excellent + good + needs_work > 0:
            print(f"\n   ⭐ Quality Distribution:")
            if excellent > 0:
                bar = self.create_progress_bar(excellent, stats['total_skills'])
                print(f"      Excellent (9-10) {bar} {excellent} skill{'s' if excellent != 1 else ''}")
            if good > 0:
                bar = self.create_progress_bar(good, stats['total_skills'])
                print(f"      Good (7-9)       {bar} {good} skill{'s' if good != 1 else ''}")
            if needs_work > 0:
                bar = self.create_progress_bar(needs_work, stats['total_skills'])
                print(f"      Needs Work (<7)  {bar} {needs_work} skill{'s' if needs_work != 1 else ''}")

    def create_progress_bar(self, value, total, width=10):
        """Create ASCII progress bar"""
        if total == 0:
            return "░" * width

        filled = int((value / total) * width)
        empty = width - filled
        percentage = int((value / total) * 100)

        return f"{'█' * filled}{'░' * empty} {percentage:3}%"

    def print_actionable_insights(self):
        """Print actionable insights and recommendations"""
        skills = self.registry.get_all_skills()

        actions = []

        # Check for skills without metadata
        no_metadata = [s for s in skills if not s.has_metadata()]
        if no_metadata:
            actions.append(f"❌ {len(no_metadata)} skill{'s' if len(no_metadata) != 1 else ''} missing metadata → [Run: --init-metadata]")

        # Check for outdated skills
        outdated = self.registry.get_outdated_skills(30)
        if outdated:
            actions.append(f"🔄 {len(outdated)} skill{'s' if len(outdated) != 1 else ''} need update (>30 days) → [Run: --check-updates]")

        # Check for skills without quality scores
        no_score = [s for s in skills if not s.get_quality_score()]
        if len(no_score) > 0:
            actions.append(f"📊 {len(no_score)} skill{'s' if len(no_score) != 1 else ''} need quality check → [Run: --check-quality]")

        if actions:
            print(f"\n⚠️  Action Required:\n")
            for action in actions:
                print(f"   {action}")
        else:
            print(f"\n✅ All Good! No actions required.")

    def print_recent_activity(self):
        """Print recent activity"""
        print(f"\n📜 Recent Activity:\n")

        if not self.last_activity:
            print(f"   No recent activity")
        else:
            for activity in self.last_activity[-5:]:  # Last 5 activities
                print(f"   • {activity}")

    def add_activity(self, activity: str):
        """Add activity to log"""
        timestamp = datetime.now().strftime('%H:%M')
        self.last_activity.append(f"{timestamp} - {activity}")

    def print_quick_actions(self):
        """Print interactive quick action menu"""
        print(f"\n⚡ Quick Actions:\n")
        print(f"   [1] Check all for updates     [2] Run quality checks")
        print(f"   [3] Update outdated skills    [4] Init metadata for all")
        print(f"   [5] Generate report           [6] Show skill details")
        print(f"   [7] Rescan for skills         [8] Add search path")
        print(f"   [0] Exit")
        print()

    def show(self, interactive=False):
        """
        Show dashboard

        Args:
            interactive: If True, show interactive menu
        """
        self.clear_screen()
        self.print_header()
        self.print_skills_table()
        self.print_enhanced_statistics()
        self.print_actionable_insights()
        self.print_recent_activity()

        if interactive:
            self.print_quick_actions()

        print()

    def show_skill_details(self, skill_name: str):
        """
        Show detailed information about a skill

        Args:
            skill_name: Name of skill to show
        """
        skill = self.registry.get_skill_by_name(skill_name)

        if not skill:
            print(f"\n❌ Skill '{skill_name}' not found")
            return

        print("\n" + "="*70)
        print(f"📚 Skill Details: {skill.name}")
        print("="*70)

        print(f"\n📌 General:")
        print(f"   Name: {skill.name}")
        print(f"   Version: v{skill.get_version()}")
        print(f"   Path: {skill.path}")
        print(f"   Last Updated: {skill.get_last_updated()}")

        age = skill.get_age_days()
        if age is not None:
            print(f"   Age: {age} days")
            if age > 30:
                print(f"   ⚠️  Warning: Skill is outdated (>30 days)")

        print(f"\n📊 Statistics:")
        stats = skill.get_stats()
        print(f"   Total Pages: {stats['total_pages']}")
        print(f"   Total Links: {stats['total_links']}")
        print(f"   Code Blocks: {stats['total_code_blocks']}")

        quality = stats.get('quality_score')
        if quality:
            print(f"   Quality Score: {quality}/10")
            if quality >= 9:
                print(f"   ⭐ Excellent quality!")
            elif quality >= 7:
                print(f"   👍 Good quality")
            else:
                print(f"   ⚠️  Needs improvement")

        print(f"\n📦 Status:")
        print(f"   Has Metadata: {'✅' if skill.has_metadata() else '❌'}")
        print(f"   Status: {skill.get_status_emoji()}")

        print("="*70)

    def run_interactive(self, manager):
        """
        Run interactive dashboard loop

        Args:
            manager: SkillManager instance
        """
        while True:
            self.show(interactive=True)

            try:
                choice = input("Choose action (0-8): ").strip()

                if choice == "0":
                    print("\n👋 Goodbye!")
                    break
                elif choice == "1":
                    print("\n🔄 Checking for updates...")
                    self.add_activity("Checking for updates")
                    manager.check_updates_all()
                    input("\nPress Enter to continue...")
                elif choice == "2":
                    print("\n🔍 Running quality checks...")
                    self.add_activity("Running quality checks")
                    manager.check_quality_all()
                    input("\nPress Enter to continue...")
                elif choice == "3":
                    print("\n⬆️  Updating skills...")
                    self.add_activity("Updating skills")
                    manager.update_all(dry_run=False)
                    input("\nPress Enter to continue...")
                elif choice == "4":
                    print("\n📝 Initializing metadata...")
                    self.add_activity("Initializing metadata")
                    manager.init_metadata_all()
                    input("\nPress Enter to continue...")
                elif choice == "5":
                    print("\n📊 Generating report...")
                    self.add_activity("Generated report")
                    manager.generate_report("skill_report.md")
                    input("\nPress Enter to continue...")
                elif choice == "6":
                    skill_name = input("\nEnter skill name: ").strip()
                    self.show_skill_details(skill_name)
                    input("\nPress Enter to continue...")
                elif choice == "7":
                    print("\n🔍 Rescanning for skills...")
                    self.add_activity("Rescanned for skills")
                    manager.scan_for_skills()
                    input("\nPress Enter to continue...")
                elif choice == "8":
                    path = input("\nEnter path to add: ").strip()
                    manager.add_search_path(path)
                    self.add_activity(f"Added path: {path}")
                    input("\nPress Enter to continue...")
                else:
                    print("\n❌ Invalid choice. Try again.")
                    input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("\nPress Enter to continue...")
