# 🎛️ Skill Manager

**Central dashboard for managing all your Claude AI skills** in one place. Discover, monitor, update, and maintain your skills effortlessly!

> **Note**: Works with skills created by [Skill Seekers](https://github.com/yusufkaraaslan/skill-seekers) and integrates with [Skill Quality Checker](https://github.com/incarnator-x/skill-quality-checker) and [Skill Updater](https://github.com/incarnator-x/skill-updater).

## 🎯 Problem

- ✅ You have 10+ skills scattered across different folders
- 🔍 Hard to track which skills need updates
- 📊 No central view of quality scores
- ⏱️ Checking each skill manually takes forever
- 🤯 No unified way to manage everything

## 💡 Solution

**Skill Manager** provides a central dashboard to discover, monitor, and manage all your skills from one place!

## ✨ Features

### 1. 🔍 **Auto-Discovery**
```bash
python skill_manager.py --add-path /path/to/Skill_Seekers/output/

# Automatically finds all skills in directory
# ✅ Found 3 skills:
#    • react
#    • vue
#    • django
```

### 2. 📊 **Dashboard View**
```
======================================================================
🎛️  SKILL MANAGER DASHBOARD
======================================================================

📚 Your Skills (3 total)

======================================================================
 1. 🟢 react                (v1.1.0)   8.5/10  📅 2 days ago
 2. 🟡 vue                  (v1.0.0)   7.2/10  📅 3 months ago
 3. 🟢 django               (v2.1.0)   9.1/10  📅 1 week ago
======================================================================

📊 Statistics:

   • Total Skills: 3
   • With Metadata: 3 / Without: 0
   • Avg Quality Score: 8.3/10
   • Skills Needing Update: 1 (>30 days old)

⚡ Quick Actions:

   [1] Check all for updates     [2] Run quality checks
   [3] Update outdated skills    [4] Generate reports
   [5] Add search path           [6] Rescan for skills
   [7] Show skill details        [0] Exit
```

### 3. ⚡ **Bulk Operations**
```bash
# Check quality of all skills
python skill_manager.py --check-quality --quality-checker ../skill-quality-checker

# Check for updates
python skill_manager.py --check-updates --updater ../skill-updater

# Update all outdated skills
python skill_manager.py --update-all --updater ../skill-updater

# Initialize metadata for all
python skill_manager.py --init-metadata --updater ../skill-updater
```

### 4. 📈 **Status Tracking**
- 🟢 **Green** - Updated recently (<7 days)
- 🟡 **Yellow** - Needs attention (7-30 days)
- 🔴 **Red** - Very old (>30 days)
- ⚠️ **Warning** - No metadata

### 5. 📊 **Report Generation**
```bash
python skill_manager.py --report skills_report.md

# Generates comprehensive markdown report with:
# - Summary statistics
# - Individual skill status
# - Quality scores
# - Update recommendations
```

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/incarnator-x/skill-manager.git
cd skill-manager

# No dependencies needed! (Uses only Python stdlib)
```

## 🚀 Quick Start

### Step 1: Add Your Skills Path

```bash
python skill_manager.py --add-path /path/to/Skill_Seekers/output/

# Discovers all skills in that directory
```

### Step 2: View Dashboard

```bash
python skill_manager.py

# Shows interactive dashboard with all skills
```

### Step 3: Setup Integrations (Optional)

```bash
# With Quality Checker
python skill_manager.py --quality-checker ../skill-quality-checker --check-quality

# With Skill Updater
python skill_manager.py --updater ../skill-updater --check-updates
```

## 📖 Complete Workflow

### Initial Setup

```bash
# 1️⃣ Add skills directory
python skill_manager.py --add-path ~/Skill_Seekers/output/

# 2️⃣ Initialize metadata for all skills
python skill_manager.py --updater ../skill-updater --init-metadata

# 3️⃣ Run quality checks
python skill_manager.py --quality-checker ../skill-quality-checker --check-quality
```

### Daily Usage

```bash
# Show dashboard
python skill_manager.py

# Check for updates
python skill_manager.py --updater ../skill-updater --check-updates

# Update outdated skills
python skill_manager.py --updater ../skill-updater --update-all

# Generate status report
python skill_manager.py --report weekly_report.md
```

### Monthly Maintenance

```bash
# Full quality audit
python skill_manager.py --quality-checker ../skill-quality-checker --check-quality

# Update everything
python skill_manager.py --updater ../skill-updater --update-all

# Generate report for tracking
python skill_manager.py --report monthly_$(date +%Y%m).md
```

## 🎯 Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `--add-path <path>` | Add search path for skills | `python skill_manager.py --add-path ~/skills/` |
| `--scan` | Rescan for skills | `python skill_manager.py --scan` |
| `--skill <name>` | Show details for specific skill | `python skill_manager.py --skill react` |
| `--check-quality` | Check quality of all skills | `python skill_manager.py --check-quality --quality-checker ../qc` |
| `--check-updates` | Check for updates | `python skill_manager.py --check-updates --updater ../updater` |
| `--update-all` | Update all skills | `python skill_manager.py --update-all --updater ../updater` |
| `--init-metadata` | Initialize metadata for all | `python skill_manager.py --init-metadata --updater ../updater` |
| `--report <file>` | Generate report | `python skill_manager.py --report report.md` |
| `--dry-run` | Simulate without changes | `python skill_manager.py --update-all --dry-run` |

## 📁 Configuration

Config is stored at: `~/.skill_manager/config.json`

```json
{
  "search_paths": [
    "/home/user/Skill_Seekers/output/",
    "/home/user/custom_skills/"
  ]
}
```

## 🎨 Dashboard Indicators

### Status Emojis
- 🟢 **Fresh** - Updated within last week
- 🟡 **Aging** - 7-30 days old
- 🔴 **Stale** - Over 30 days old
- ⚠️ **No Data** - Missing metadata

### Quality Scores
- **9-10** - Excellent
- **8-9** - Very Good
- **7-8** - Good
- **6-7** - Fair
- **<6** - Needs Improvement

## ⚡ Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Discovery | 1-2 sec | Per 100 skills |
| Dashboard render | <1 sec | Instant |
| Quality check all | ~30 sec/skill | Parallel execution (future) |
| Update check all | ~1 min/skill | Fast HEAD requests |

## 🔗 Integration

### With Skill Seekers

```bash
# Create skills
cd Skill_Seekers
python cli/doc_scraper.py --config configs/react.json

# Manage with Skill Manager
cd ../skill-manager
python skill_manager.py --add-path ../Skill_Seekers/output/
```

### With Quality Checker

```bash
# Run quality checks on all skills
python skill_manager.py \
  --quality-checker ../skill-quality-checker \
  --check-quality
```

### With Skill Updater

```bash
# Check and apply updates to all skills
python skill_manager.py \
  --updater ../skill-updater \
  --check-updates

python skill_manager.py \
  --updater ../skill-updater \
  --update-all
```

## 📊 Use Cases

### Use Case 1: New User Onboarding
```bash
# First time setup
python skill_manager.py --add-path ~/Skill_Seekers/output/
python skill_manager.py --init-metadata --updater ../skill-updater
python skill_manager.py  # View dashboard
```

### Use Case 2: Weekly Maintenance
```bash
# Check status
python skill_manager.py --check-updates --updater ../skill-updater

# Update if needed
python skill_manager.py --update-all --updater ../skill-updater
```

### Use Case 3: Quality Audit
```bash
# Run comprehensive checks
python skill_manager.py --check-quality --quality-checker ../qc

# Generate audit report
python skill_manager.py --report audit_2024.md
```

### Use Case 4: Bulk Management
```bash
# Manage 50+ skills at once
python skill_manager.py --add-path ~/all_skills/
python skill_manager.py --check-updates --updater ../updater
python skill_manager.py --update-all --updater ../updater
```

## 🗺️ Roadmap

- [ ] Interactive TUI with arrow key navigation
- [ ] Parallel bulk operations
- [ ] Scheduled automatic checks (cron integration)
- [ ] Web dashboard (Flask/FastAPI)
- [ ] Skill comparison view
- [ ] Export to CSV/JSON
- [ ] Notification system
- [ ] Plugin system

## 🐛 Troubleshooting

### "No skills found"
**Solution**: Add search path with `--add-path`

### "Bulk operations not configured"
**Solution**: Provide tool paths with `--quality-checker` and `--updater`

### Config file location
**Windows**: `C:\Users\<user>\.skill_manager\config.json`
**Linux/Mac**: `~/.skill_manager/config.json`

## 📚 Related Projects

- **[Skill Seekers](https://github.com/yusufkaraaslan/skill-seekers)** - Create Claude AI skills
- **[Skill Quality Checker](https://github.com/incarnator-x/skill-quality-checker)** - Validate skill quality
- **[Skill Updater](https://github.com/incarnator-x/skill-updater)** - Keep skills up-to-date

## 🎯 Tool Ecosystem

```
Create → Validate → Maintain → Manage
   ↓         ↓          ↓         ↓
Seekers → Quality → Updater → MANAGER (You are here!)
```

## 📄 License

MIT License - See LICENSE file

## 🙏 Contributing

Contributions welcome! Please open an issue or PR.

---

**Made with ❤️ for the Claude AI community**
