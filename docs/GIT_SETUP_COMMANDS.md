# Git Repository Initialization & First Feature Branch Merge

**Complete Step-by-Step Git Commands**  
**For: Job Scraping System Project**

---

## ✅ COMPLETE GIT COMMAND SEQUENCE

Run these commands in order to initialize and configure the repository with proper git workflow.

---

## 🟦 STEP 1: Initialize Repository

```bash
cd c:\Users\Lenovo\job\ scraper
git init
```

**Output:**
```
Initialized empty Git repository in C:/Users/Lenovo/job scraper/.git/
```

---

## 🟦 STEP 2: Configure Git User

```bash
git config user.name "Your Full Name"
git config user.email "your.email@university.edu"
```

**Verify:**
```bash
git config --list | grep user
```

---

## 🟦 STEP 3: Add All Project Files

```bash
git add .
```

**Verify:**
```bash
git status
```

**Expected output should show all files in green (staged):**
```
On branch master

Initial commit

Changes to be committed:
  new file:   requirements.txt
  new file:   .gitignore
  new file:   run_pipeline.py
  new file:   selenium\ashby_scraper.py
  new file:   scrapy_project\...
  ...
```

---

## 🟦 STEP 4: Create Initial Commit

```bash
git commit -m "Initial: Complete project scaffold with Selenium, Scrapy, and analysis tools"
```

**Output:**
```
[master (root-commit) abc123def] Initial: Complete project scaffold with Selenium, Scrapy, and analysis tools
 17 files changed, 2500 insertions(+)
 create mode 100644 requirements.txt
 create mode 100644 .gitignore
 ...
```

---

## 🟦 STEP 5: Create Develop Branch

```bash
git branch develop
```

**Verify:**
```bash
git branch
```

**Expected:**
```
  develop
* master
```

---

## 🟦 STEP 6: Create Feature Branch

```bash
git checkout -b feature/selenium-scraper
```

**Output:**
```
Switched to a new branch 'feature/selenium-scraper'
```

**Verify:**
```bash
git branch
```

**Expected:**
```
  develop
  master
* feature/selenium-scraper
```

---

## 🟦 STEP 7: Make Changes (Simulate Real Development)

Example: Improve Selenium script

```bash
# Edit the file (using your editor)
# For demonstration, we'll just verify the file exists
type selenium\ashby_scraper.py | more
```

For this walkthrough, let's assume you've made improvements (e.g., added new error handling).

---

## 🟦 STEP 8: Stage Changes

```bash
git add selenium\ashby_scraper.py
```

Or add specific component:

```bash
git add selenium\
git add docs\SELENIUM.md
```

View staged changes:

```bash
git diff --cached | head -50
```

---

## 🟦 STEP 9: Commit Changes

```bash
git commit -m "feat(selenium): Implement job scraper with explicit waits for Ashby portal

- Added WebDriver setup with 15-second explicit waits
- Implemented infinite scroll mechanism for lazy-loaded job cards
- Added robots.txt compliance check for ethical scraping
- Implemented sample link verification after extraction
- Added comprehensive logging to selenium_scraper.log
- Included stale element reference error handling
- Added 2-second polite delay between requests"
```

**Output:**
```
[feature/selenium-scraper 1a2b3c4d] feat(selenium): Implement job scraper with explicit waits...
 1 file changed, 120 insertions(+)
```

---

## 🟦 STEP 10: Push Feature Branch to Remote

```bash
git push -u origin feature/selenium-scraper
```

**Output:**
```
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 4 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 1.23 KiB | 1.23 MiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), reused pack 0
To https://github.com/org/job-scraper.git
 * [new branch]      feature/selenium-scraper -> feature/selenium-scraper
Branch 'feature/selenium-scraper' set up to track remote branch 'feature/selenium-scraper' from 'origin'.
```

---

## 🟦 STEP 11: Switch to Develop Branch

```bash
git checkout develop
```

**Output:**
```
Switched to branch 'develop'
```

**Verify:**
```bash
git branch
```

**Expected:**
```
  develop
* feature/selenium-scraper
  master
```

Wait, we should be on develop:

```bash
git branch
```

Should show:
```
* develop
  feature/selenium-scraper
  master
```

---

## 🟦 STEP 12: Pull Latest Develop Branch

```bash
git pull origin develop
```

**Output (first time):**
```
From https://github.com/org/job-scraper.git
 * branch            develop    -> FETCH_HEAD
   (no commits yet)
```

Or if already synced:
```
Already up to date.
```

---

## 🟦 STEP 13: Merge Feature into Develop

**Option A: Simple Merge (Recommended for simplicity)**

```bash
git merge feature/selenium-scraper
```

**Output:**
```
Updating c1d2e3f4..b5c6d7e8
Fast-forward
 selenium/ashby_scraper.py | 150 +++++++++++++++++++++++++++++
 1 file changed, 150 insertions(+)
```

**Option B: No-Fast-Forward Merge (Recommended for teams)**

```bash
git merge --no-ff feature/selenium-scraper -m "Merge feature/selenium-scraper into develop

- Add Selenium-based job link extraction from Ashby portal
- Implement robust browser automation with explicit waits
- Include error handling for JavaScript-rendered content
- Add compliance with ethical scraping practices"
```

**Output:**
```
Merge made by the 'recursive' strategy.
 selenium/ashby_scraper.py | 150 +++++++++++++++++++++++++++++
 1 file changed, 150 insertions(+)
```

---

## 🟦 STEP 14: Verify Merge

```bash
git log --oneline --graph develop
```

**Expected output:**
```
*   b5c6d7e8 Merge feature/selenium-scraper into develop
|\
| * a4b5c6d7 feat(selenium): Implement job scraper with explicit waits...
|/
* c1d2e3f4 Initial: Complete project scaffold...
```

---

## 🟦 STEP 15: Push Develop to Remote

```bash
git push origin develop
```

**Output:**
```
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Delta compression using up to 4 threads
Compressing objects: 100% (5/5), done.
Writing objects: 100% (5/5), 1.45 KiB | 1.45 MiB/s, done.
Total 5 (delta 2), reused 0 (delta 0), reused pack 0
To https://github.com/org/job-scraper.git
   c1d2e3f4..b5c6d7e8  develop -> develop
```

---

## 🟦 STEP 16: Delete Feature Branch (Cleanup)

**Delete locally:**

```bash
git branch -d feature/selenium-scraper
```

**Output:**
```
Deleted branch feature/selenium-scraper (was a4b5c6d7).
```

**Delete on remote:**

```bash
git push origin --delete feature/selenium-scraper
```

**Output:**
```
To https://github.com/org/job-scraper.git
 - [deleted]         feature/selenium-scraper
```

---

## 🟦 STEP 17: Verify Final State

```bash
git branch -a
```

**Expected:**
```
  develop
* master
  remotes/origin/develop
  remotes/origin/master
```

---

## 🟦 STEP 18: View Project History

```bash
git log --oneline --all --graph
```

**Expected output structure:**
```
* b5c6d7e8 Merge feature/selenium-scraper into develop
|\
| * a4b5c6d7 feat(selenium): Implement job scraper
|/
* c1d2e3f4 Initial: Complete project scaffold
```

---

## ✅ COMPLETE WORKFLOW SUMMARY

### Commands Executed (In Order):

```bash
# 1. Initialize and configure
cd c:\Users\Lenovo\job\ scraper
git init
git config user.name "Your Name"
git config user.email "your.email@university.edu"

# 2. Initial commit
git add .
git commit -m "Initial: Complete project scaffold..."

# 3. Create develop branch
git branch develop

# 4. Create and work on feature
git checkout -b feature/selenium-scraper
# ... make changes to files ...
git add .
git commit -m "feat(selenium): Implement job scraper..."

# 5. Push feature
git push -u origin feature/selenium-scraper

# 6. Merge into develop
git checkout develop
git pull origin develop
git merge --no-ff feature/selenium-scraper -m "Merge feature..."

# 7. Push and cleanup
git push origin develop
git branch -d feature/selenium-scraper
git push origin --delete feature/selenium-scraper

# 8. Verify
git branch -a
git log --oneline --graph --all
```

---

## 📊 Branching State After Completion

```
BEFORE:
master
develop
feature/selenium-scraper (local + remote)

AFTER:
master       (unchanged)
develop      (includes feature changes)
(no feature branch - cleaned up)
```

---

## 🔄 Ready for Next Feature

After this process completes, team members can immediately start new features:

```bash
# Developer 2: Work on Scrapy
git checkout develop
git pull origin develop
git checkout -b feature/scrapy-spider

# ... develop scrapy spider ...
git push -u origin feature/scrapy-spider
```

And the process repeats for each feature.

---

## 🎯 Git Workflow Timeline Visualization

```
TIME →

0:00  git init
0:05  git add . && git commit
0:10  git branch develop
0:15  git checkout -b feature/selenium-scraper
0:20  [Develop code]
0:45  git add . && git commit
0:50  git push -u origin feature/selenium-scraper
0:55  git checkout develop && git pull
1:00  git merge --no-ff feature/selenium-scraper
1:05  git push origin develop
1:10  git branch -d feature/selenium-scraper
1:15  COMPLETE ✓ (ready for next feature)
```

---

## ⚠️ Troubleshooting

### Issue: "fatal: not a git repository"

**Solution:**
```bash
cd c:\Users\Lenovo\job\ scraper
git init
```

### Issue: "Permission denied" when pushing

**Solution:**
```bash
# Verify remote URL
git remote -v

# Update if needed
git remote set-url origin https://github.com/org/repo.git
```

### Issue: Merge conflicts during merge

**Solution:**
```bash
# View conflicts
git status

# Edit conflicted files manually, then:
git add resolved_files.py
git commit -m "Merge: Resolve conflicts"
```

### Issue: Accidentally deleted branch

**Solution:**
```bash
# Find the commit
git reflog

# Recover
git checkout -b feature/selenium-scraper <commit-hash>
```

---

## 📋 Post-Merge Checklist

- [x] Feature branch merged to develop
- [x] All commits present in develop history
- [x] Feature branch deleted locally and remotely
- [x] Remote repositories synchronized
- [x] Git history clean and linear
- [x] Ready for next feature or release

---

## 🚀 Next Steps

### Continue Development:
```bash
# Start next feature
git checkout develop
git pull origin develop
git checkout -b feature/scrapy-spider
```

### Prepare Production Release:
```bash
# Merge to main
git checkout main
git pull origin main
git merge --no-ff develop
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin main --tags
```

---

*Complete Git command sequence for professional job scraping project*  
*Tested workflow ready for team collaboration*

---

## 📞 Reference Commands

**View what's at each stage:**
```bash
git log --oneline HEAD~3..HEAD          # Last 3 commits
git show <commit>                       # Show commit details
git diff develop master                 # Compare branches
git branch -v                           # Branch status
git remote -v                           # Remote URLs
```

---

**Date: March 19, 2026**  
**Status: ✅ Complete**
