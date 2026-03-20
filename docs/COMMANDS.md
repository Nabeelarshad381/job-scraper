# Complete Command Reference

**Quick Reference Guide for All Commands**

---

## 🚀 EXECUTION COMMANDS

### Run Complete Pipeline (All 3 Phases)

```bash
cd c:\Users\Lenovo\job\ scraper
python run_pipeline.py
```

---

## 📋 INDIVIDUAL PHASE COMMANDS

### Phase 1: Selenium Job Link Extraction

```bash
cd c:\Users\Lenovo\job\ scraper\selenium
python ashby_scraper.py
```

**Output:** Creates `data/raw/job_links.csv` with job URLs

---

### Phase 2: Scrapy Job Details Extraction

```bash
cd c:\Users\Lenovo\job\ scraper\scrapy_project
scrapy crawl ashby_jobs
```

**Output:** Creates `data/final/jobs.csv` with 9 fields per job

---

### Phase 3: Data Analysis & Reporting

```bash
cd c:\Users\Lenovo\job\ scraper\analysis
python job_analysis.py
```

**Output:** Creates visualizations and reports in `reports/` directory

---

## 💻 SETUP & INSTALLATION COMMANDS

### Create Virtual Environment

**Windows:**
```bash
cd c:\Users\Lenovo\job\ scraper
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
cd path/to/job\ scraper
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Verify Installation

```bash
python -c "import selenium; import scrapy; import pandas; print('✓ All packages installed')"
```

---

## 🔀 GIT WORKFLOW COMMANDS

### Initial Repository Setup

```bash
cd c:\Users\Lenovo\job\ scraper
git init
git config user.name "Your Name"
git config user.email "your.email@university.edu"
git add .
git commit -m "Initial: Complete project scaffold"
git branch develop
git push -u origin main
git push -u origin develop
```

### Creating and Pushing Feature Branch

```bash
# Create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/selenium-scraper

# Make changes (edit files)

# Stage and commit
git add selenium/ashby_scraper.py
git commit -m "feat(selenium): Implement job link extraction with explicit waits"

# Push to remote
git push -u origin feature/selenium-scraper
```

### Merging Feature into Develop (Local)

```bash
# Switch to develop
git checkout develop

# Ensure up to date
git pull origin develop

# Merge feature branch
git merge feature/selenium-scraper

# Push to remote
git push origin develop

# Delete feature branch
git branch -d feature/selenium-scraper
git push origin --delete feature/selenium-scraper
```

### Complete Feature Workflow (All Steps)

```bash
# 1. Create feature
git checkout develop && git pull origin develop
git checkout -b feature/my-feature

# 2. Work and commit
git add .
git commit -m "feat(area): Description of changes"

# 3. Push
git push -u origin feature/my-feature

# 4. Merge back
git checkout develop && git pull origin develop
git merge --no-ff feature/my-feature
git push origin develop

# 5. Cleanup
git branch -d feature/my-feature
git push origin --delete feature/my-feature
```

### Create Release on Main

```bash
# Merge develop to main (production)
git checkout main
git pull origin main
git merge --no-ff develop -m "Release: v1.0.0"

# Tag release
git tag -a v1.0.0 -m "Version 1.0.0 - Initial Release"

# Push
git push origin main --tags
```

---

## 📂 PROJECT STRUCTURE CREATION

### Full Directory Setup

```bash
cd c:\Users\Lenovo\job\ scraper

# Create directories
mkdir selenium
mkdir scrapy_project\ashby_spider\spiders
mkdir data\raw
mkdir data\final
mkdir analysis
mkdir docs
mkdir logs

# Verify structure
tree /F  # Windows
# or
find . -type d  # macOS/Linux
```

---

## 🔍 UTILITY & VERIFICATION COMMANDS

### Check Data Files

```bash
# Windows - List files
dir data\raw\
dir data\final\
dir analysis\reports\

# Linux/macOS - List files
ls -la data/raw/
ls -la data/final/
ls -la analysis/reports/
```

### View Generated Reports

```bash
# Windows
start analysis\reports\analysis_report.txt

# macOS
open analysis/reports/analysis_report.txt

# Linux
cat analysis/reports/analysis_report.txt
```

### Check Logs

```bash
# Windows
type logs\selenium_scraper.log

# macOS/Linux
cat logs/selenium_scraper.log
tail -f logs/selenium_scraper.log  # Follow in real-time
```

---

## 🐞 DEBUG & TESTING COMMANDS

### Test Selenium Setup

```bash
cd selenium
python -c "from selenium import webdriver; print('✓ Selenium OK')"
```

### Test Scrapy Spider

```bash
cd scrapy_project
scrapy list
scrapy check ashby_jobs
```

### Test Data Analysis

```bash
cd analysis
python -c "import pandas; print('✓ Analysis OK')"
```

### Interactive Python Shell

```bash
python
>>> import pandas as pd
>>> df = pd.read_csv('../data/final/jobs.csv')
>>> df.shape
>>> df.head()
>>> exit()
```

---

## 📊 GIT VIEWING & INFORMATION COMMANDS

### View Git Status

```bash
# Current status
git status

# Branches
git branch -a

# Remote URLs
git remote -v
```

### View Commit History

```bash
# Basic log
git log --oneline | head -10

# Graph view
git log --graph --oneline --all

# Show specific commit
git show <commit-hash>

# View changes
git diff HEAD~1
```

### View Branch Information

```bash
# Show branches
git branch -a

# Show branch tracking
git branch -vv

# Show merged branches
git branch --merged develop

# Show unmerged branches
git branch --no-merged develop
```

---

## 🔄 COMMON WORKFLOW SEQUENCES

### Scenario 1: Add New Feature

```bash
# Setup
git checkout develop && git pull origin develop

# Create feature
git checkout -b feature/new-feature

# Develop
# ... make changes ...
git add .
git commit -m "feat(module): Add new feature"

# Push and merge
git push -u origin feature/new-feature
git checkout develop && git pull origin develop
git merge feature/new-feature
git push origin develop
git branch -d feature/new-feature && git push origin --delete feature/new-feature
```

### Scenario 2: Fix a Bug

```bash
# Create bugfix branch
git checkout develop && git pull origin develop
git checkout -b fix/bug-description

# Fix
# ... make changes ...
git add .
git commit -m "fix(module): Fix bug description"

# Merge
git push -u origin fix/bug-description
git checkout develop && git pull origin develop
git merge fix/bug-description
git push origin develop
```

### Scenario 3: Update Documentation

```bash
# Create docs branch
git checkout develop && git pull origin develop
git checkout -b docs/update-readme

# Update docs
# ... edit documentation ...
git add docs/README.md
git commit -m "docs: Update project documentation"

# Merge
git push -u origin docs/update-readme
git checkout develop && git pull origin develop
git merge docs/update-readme
git push origin develop
```

---

## 🗑️ CLEANUP COMMANDS

### Remove Old Branches

```bash
# Delete local branch
git branch -d feature/old-branch

# Delete remote branch
git push origin --delete feature/old-branch

# Prune deleted remote branches
git fetch --prune
```

### Clean Git Cache

```bash
# Clear stale branches
git gc --prune=now

# Clean working directory
git clean -fd  # Remove untracked files and directories
```

---

## ⚠️ EMERGENCY UNDO COMMANDS

### Undo Last Local Commit

```bash
# Undo but keep changes
git reset --soft HEAD~1

# Undo and discard changes
git reset --hard HEAD~1
```

### Recover Deleted Branch

```bash
# Find deleted branch
git reflog | grep "feature-name"

# Recover
git checkout -b feature-name <commit-hash>
```

### Revert Pushed Commit

```bash
# Create new commit undoing changes
git revert <commit-hash>
git push origin develop
```

---

## 📝 BATCH OPERATIONS

### Commit Multiple Files

```bash
git add file1.py file2.py file3.py
git commit -m "feat: Update multiple modules"
git push origin branch-name
```

### Stash Uncommitted Changes

```bash
# Save changes
git stash

# Continue work
git checkout other-branch

# Restore changes
git stash pop
```

### Rebase Interactive (Clean History)

```bash
# Show last 5 commits
git rebase -i HEAD~5

# Squash, reorder, or edit commits
# (follow interactive prompt)

git push origin branch-name --force-with-lease
```

---

## 🎯 MULTIPLE FEATURE PARALLEL DEVELOPMENT

### Developer 1

```bash
git checkout -b feature/selenium-enhancements
# ... develop ...
git push -u origin feature/selenium-enhancements
```

### Developer 2 (Parallel)

```bash
git checkout -b feature/scrapy-improvements
# ... develop ...
git push -u origin feature/scrapy-improvements
```

### Merge Both to Develop

```bash
git checkout develop && git pull origin develop

# Merge first feature
git merge feature/selenium-enhancements

# Merge second feature
git merge feature/scrapy-improvements

# If conflicts, resolve and commit
git push origin develop
```

---

## 📋 TROUBLESHOOTING COMMAND SEQUENCES

### Fix Merge Conflict

```bash
# During merge conflict
git merge feature-branch

# Edit conflicted files manually
# Resolve <<<<<<, =======, >>>>>> markers

# Complete merge
git add resolved-files
git commit -m "Merge: Resolve conflicts"
```

### Fix Wrong Branch Commit

```bash
# Undo on wrong branch
git reset --soft HEAD~1

# Switch correct branch
git checkout correct-branch

# Commit on correct branch
git commit -m "..."
```

### Sync Fork with Upstream

```bash
# Add upstream
git remote add upstream https://github.com/original/repo.git

# Fetch upstream
git fetch upstream

# Update develop
git checkout develop
git merge upstream/develop
git push origin develop
```

---

## 🚀 FINAL EXECUTION CHECKLIST

### Before Deployment

- [ ] All code committed: `git status` (clean)
- [ ] All tests pass: `python run_pipeline.py`
- [ ] Documentation updated
- [ ] No debug code or print statements
- [ ] Version tagged: `git tag -a v1.0.0 -m "Release"`

### Commands to Run

```bash
# 1. Verify status
git status

# 2. Run complete pipeline
python run_pipeline.py

# 3. Check outputs
dir data\final\
dir analysis\reports\

# 4. Create release
git checkout main && git pull origin main
git merge --no-ff develop
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin main --tags
```

---

*Last Updated: March 19, 2026*
*For detailed information, refer to specific guides: GIT_WORKFLOW.md, SELENIUM.md, SCRAPY.md, ANALYSIS.md*
