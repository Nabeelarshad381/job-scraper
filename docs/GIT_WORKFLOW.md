# Git Workflow & Commands Reference

**Professional Branching Strategy for Team Collaboration**

---

## 📌 Branching Model Overview

```
                    ┌──────────────┐
                    │    MAIN      │ (Production)
                    └──────┬───────┘
                           ▲
                           │ (releases)
                    ┌──────┴───────┐
                    │   DEVELOP    │ (Integration)
                    └──────┬───────┘
                           ▲
              ┌────────────┼────────────┐
              │            │            │
        ┌─────┴────┐ ┌────┴──────┐ ┌──┴──────┐
        │ FEATURE  │ │  FEATURE  │ │ FEATURE │
        │ Branch 1 │ │ Branch 2  │ │ Branch 3│
        └──────────┘ └───────────┘ └─────────┘
```

**Branch Purposes:**
- `main`: Stable, production-ready code (releases)
- `develop`: Integration branch for features
- `feature/*`: Individual feature development

---

## 🚀 Initial Repository Setup

### Step 1: Initialize Repository

```bash
cd c:\Users\Lenovo\job\ scraper
git init
git config user.name "Your Name"
git config user.email "your.email@university.edu"
```

### Step 2: Create Initial Commit

```bash
# Add all project files
git add .

# Verify files to be committed
git status

# Commit with descriptive message
git commit -m "Initial: Complete project scaffold with Selenium, Scrapy, and analysis tools"
```

### Step 3: Create Develop Branch

```bash
# Create develop branch (branches from main/master)
git branch develop

# Verify branch created
git branch -a

# Switch to develop
git checkout develop
```

### Step 4: Configure Remote (if using GitHub/GitLab)

```bash
# Add remote repository
git remote add origin https://github.com/your-org/job-scraper.git

# Push main branch
git push -u origin main

# Push develop branch
git push -u origin develop
```

---

## 🌳 Feature Branch Workflow

### Create Feature Branch

```bash
# Ensure you're on develop branch
git checkout develop

# Pull latest changes
git pull origin develop

# Create feature branch (from develop)
git checkout -b feature/selenium-scraper

# Naming convention: feature/{feature-name}
# Examples:
# - feature/selenium-scraper
# - feature/scrapy-spider
# - feature/data-analysis
# - feature/git-documentation
```

### Make Changes & Commit

```bash
# Work on files in your feature branch
# ... edit, test, verify ...

# Stage changes
git add selenium/ashby_scraper.py

# Commit with clear message
git commit -m "feat(selenium): Implement job link extraction with explicit waits

- Added WebDriver setup with explicit waits (15 second timeout)
- Implemented infinite scroll to load all job cards
- Added robots.txt compliance check
- Implemented sample link verification
- Added comprehensive error handling and logging"

# Commit messages follow conventional commits format:
# Types: feat, fix, docs, style, refactor, test, chore
```

### Commit Message Best Practices

```
# Format:
type(scope): Brief description

Detailed explanation of changes
- Bullet point 1
- Bullet point 2

Fixes #123  # Issue reference if applicable

# Examples:
# ✓ feat(selenium): Add explicit waits for job loading
# ✓ fix(scrapy): Handle stale element references
# ✓ docs(git): Add branching workflow documentation
# ✗ Updated code
# ✗ Fixed bug
```

### Push Feature Branch

```bash
# Push to remote (sets up upstream tracking)
git push -u origin feature/selenium-scraper

# Subsequent pushes
git push origin feature/selenium-scraper

# Verify on GitHub/GitLab (ready for pull request)
```

---

## 🔗 Merging Feature into Develop

### Option 1: Pull Request (Recommended for Teams)

```bash
# Create pull request on GitHub/GitLab/Bitbucket
# 1. Go to repository on platform
# 2. Click "New Pull Request"
# 3. Base: develop, Compare: feature/selenium-scraper
# 4. Add description and title
# 5. Request reviewers
# 6. After approval, merge

# Then locally sync
git checkout develop
git pull origin develop
```

### Option 2: Local Merge

```bash
# Switch to develop branch
git checkout develop

# Ensure develop is up to date
git pull origin develop

# Merge feature branch
git merge feature/selenium-scraper -m "Merge feature/selenium-scraper into develop

- Adds Selenium-based job link extraction
- Implements robust error handling
- Includes comprehensive logging"

# Verify merge
git log --oneline | head -5

# Push to remote
git push origin develop
```

### Delete Feature Branch

```bash
# Delete locally (after merge)
git branch -d feature/selenium-scraper

# Delete on remote
git push origin --delete feature/selenium-scraper

# Verify deletion
git branch -a
```

---

## 📋 Complete Feature Development Sequence

### Full Example: Adding Selenium Scraper

```bash
# ============================================
# STEP 1: Initialize repository (first time)
# ============================================

cd c:\Users\Lenovo\job\ scraper
git init
git config user.name "Data Engineer"
git config user.email "engineer@university.edu"
git add .
git commit -m "Initial: Project scaffold with complete structure"
git branch develop
git push -u origin main
git push -u origin develop


# ============================================
# STEP 2: Create feature branch
# ============================================

git checkout develop
git pull origin develop
git checkout -b feature/selenium-scraper


# ============================================
# STEP 3: Develop and commit changes
# ============================================

# ... edit selenium/ashby_scraper.py ...

git add selenium/ashby_scraper.py
git commit -m "feat(selenium): Implement job scraper with scrolling"

# ... fix an issue ...

git add selenium/ashby_scraper.py
git commit -m "fix(selenium): Handle stale element exceptions"

# ... add logging ...

git add logs/
git commit -m "docs(selenium): Add comprehensive logging"


# ============================================
# STEP 4: Push feature branch
# ============================================

git push -u origin feature/selenium-scraper


# ============================================
# STEP 5: Merge back to develop (local)
# ============================================

git checkout develop
git pull origin develop
git merge feature/selenium-scraper

# Or with merge commit (recommended):
git merge --no-ff feature/selenium-scraper -m "Merge feature/selenium-scraper"

# Verify merge
git log --graph --oneline --all | head -10

# Push to remote
git push origin develop


# ============================================
# STEP 6: Cleanup
# ============================================

git branch -d feature/selenium-scraper
git push origin --delete feature/selenium-scraper

# Verify
git branch -a
```

---

## 🏷️ Release to Main

### Create Release Branch (Optional but Recommended)

```bash
# When develop is ready for release
git checkout -b release/v1.0.0 develop

# Make final adjustments (version bumps, release notes)
# ...

git commit -m "chore(release): Bump version to 1.0.0"

# Create tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Merge to main
git checkout main
git pull origin main
git merge --no-ff release/v1.0.0 -m "Release v1.0.0"

# Merge back to develop
git checkout develop
git merge --no-ff release/v1.0.0

# Push everything
git push origin main develop --tags

# Delete release branch
git branch -d release/v1.0.0
git push origin --delete release/v1.0.0
```

### Direct Merge to Main (Simpler)

```bash
# When develop is stable and ready
git checkout main
git pull origin main

# Merge develop
git merge --no-ff develop -m "Release: Merge develop into main for production"

# Create version tag
git tag -a v1.0.0 -m "Version 1.0.0 - Initial Release"

# Push
git push origin main --tags
```

---

## 📊 Useful Git Commands

### Viewing History

```bash
# View commit history
git log --oneline | head -10

# View graph
git log --graph --oneline --all

# View commits by author
git log --author="Your Name" --oneline

# View changes in commit
git show <commit-hash>

# View contributors
git shortlog -sn
```

### Branch Management

```bash
# List local branches
git branch

# List remote branches
git branch -r

# List all branches
git branch -a

# View branch details
git show-branch

# Switch branches
git checkout <branch-name>

# Create and switch
git checkout -b <branch-name>
```

### Stashing & Temporarily Saving Work

```bash
# Stash uncommitted changes
git stash

# List stashes
git stash list

# Apply stash
git stash apply stash@{0}

# Pop stash (apply and remove)
git stash pop

# Drop stash
git stash drop stash@{0}
```

### Undoing Changes

```bash
# Discard local changes to file
git checkout -- <filename>

# Unstage file
git reset HEAD <filename>

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert commit (create new commit undoing it)
git revert <commit-hash>
```

### Remote Operations

```bash
# View remote URLs
git remote -v

# Add remote
git remote add origin https://github.com/org/repo.git

# Remove remote
git remote remove origin

# Fetch updates (don't merge)
git fetch origin

# Pull updates (fetch + merge)
git pull origin develop

# Push updates
git push origin develop

# Push all branches
git push origin --all

# Push tags
git push origin --tags
```

---

## 🔄 Handling Conflicts

### Merge Conflicts

```bash
# If conflicts occur during merge
git merge feature/branch-name

# Shows conflict markers:
# <<<<<<< HEAD
# Current branch changes
# =======
# Incoming changes
# >>>>>>> feature/branch-name

# Resolve conflicts manually in editor

# After fixing
git add <resolved-files>
git commit -m "Merge: Resolve conflicts from feature/branch-name"
```

### Rebase (Alternative to Merge)

```bash
# Rebase feature onto develop (cleaner history)
git checkout feature/branch-name
git rebase develop

# Resolve conflicts if any
git add <resolved-files>
git rebase --continue

# Push after rebase (with force if needed)
git push origin feature/branch-name
```

---

## 👥 Team Collaboration Example

### Scenario: Multiple Developers

```
Developer 1 (Selenium)              Developer 2 (Scrapy)
    │                                   │
    git checkout develop                git checkout develop
    git pull origin develop             git pull origin develop
    │                                   │
    git checkout -b feature/selenium    git checkout -b feature/scrapy
    │                                   │
    ... develop ...                     ... develop ...
    git push -u origin feature/...      git push -u origin feature/...
    [Create PR]                         [Create PR]
    │                                   │
    [Code Review] ──────────────────────[Code Review]
    │                                   │
    [Approve & Merge] ────────────────[Approve & Merge]
    │                                   │
    git checkout develop ─────────────── git checkout develop
    git pull origin develop ────────────git pull origin develop
    │                                   │
    [Both have latest code]
```

---

## 🛠️ Troubleshooting Git Issues

### Accidental Delete a Branch?

```bash
# Find the deleted branch commit
git reflog | grep "feature/branch-name"

# Recover
git checkout -b feature/branch-name <commit-hash>
```

### Committed to Wrong Branch?

```bash
# Undo commit on current branch
git reset --soft HEAD~1

# Switch to correct branch
git checkout correct-branch

# Commit again
git commit -m "..."
```

### Need to Edit Last Commit?

```bash
# Amend last commit
git commit --amend -m "New message"

# Push (if already pushed, force is needed)
git push origin branch-name --force-with-lease
```

### Sync Fork with Upstream

```bash
# Add upstream remote
git remote add upstream https://github.com/original/repo.git

# Fetch from upstream
git fetch upstream

# Rebase develop on upstream
git checkout develop
git rebase upstream/develop
git push origin develop
```

---

## 📋 Branching Strategy Summary

| Branch | Purpose | Management |
|--------|---------|------------|
| `main` | Production | Merge from develop, tag releases |
| `develop` | Integration | Merge features, never direct commits |
| `feature/*` | Development | Create from develop, merge back to develop |
| `hotfix/*` | Emergency fixes | Create from main, merge to both main & develop |

## ✅ Pre-Merge Checklist

Before merging to develop:
- [ ] Feature implemented completely
- [ ] Code tested locally
- [ ] No merge conflicts
- [ ] Commit messages clear and descriptive
- [ ] Documentation updated
- [ ] Code follows project standards
- [ ] No debugging prints or commented code
- [ ] Tests pass (if applicable)

---

*Reference: Git 2.30+, Standard Git Workflow*
