@echo off
REM ============================================
REM Complete Git Setup & GitHub Upload Script
REM Job Scraping Project - Professional Workflow
REM For: Windows Command Prompt
REM ============================================

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo GIT SETUP - JOB SCRAPING PROJECT
echo ==========================================
echo.

REM ============================================
REM CONFIGURE GIT USER (One-time setup)
REM ============================================
echo [1/8] Configuring Git user...
git config --global user.name "Nabeelarshad381"
git config --global user.email "nabeelarshad3000@gmail.com"
echo ✓ Git user configured
echo.

REM ============================================
REM NAVIGATE TO PROJECT DIRECTORY
REM ============================================
cd /d "c:\Users\Lenovo\job scraper"
echo [2/8] Project directory: %cd%
echo.

REM ============================================
REM INITIALIZE REPOSITORY
REM ============================================
echo [3/8] Initializing Git repository...
git init
echo ✓ Repository initialized
echo.

REM ============================================
REM CREATE INITIAL COMMIT
REM ============================================
echo [4/8] Creating initial commit...
git add .
git commit -m "Initial: Complete professional job-scraping system scaffold"
echo ✓ Initial commit created on main branch
echo.

REM ============================================
REM CREATE DEVELOP BRANCH
REM ============================================
echo [5/8] Creating develop branch...
git branch develop
echo ✓ Develop branch created
echo.

REM ============================================
REM CREATE FEATURE BRANCHES
REM ============================================
echo [6/8] Creating feature branches...
git checkout -b feature/selenium-scraper develop >nul 2>&1
git checkout develop >nul 2>&1
git checkout -b feature/scrapy-spider develop >nul 2>&1
git checkout develop >nul 2>&1
git checkout -b feature/data-analysis develop >nul 2>&1
git checkout develop >nul 2>&1
git checkout -b feature/documentation develop >nul 2>&1
git checkout develop >nul 2>&1
echo ✓ Feature branches created:
echo   - feature/selenium-scraper
echo   - feature/scrapy-spider
echo   - feature/data-analysis
echo   - feature/documentation
echo.

REM ============================================
REM CONFIGURE REMOTE REPOSITORY
REM ============================================
echo [7/8] Configuring GitHub remote...
git remote add origin https://github.com/Nabeelarshad381/job-scraper.git
git remote -v
echo ✓ Remote repository configured
echo.

REM ============================================
REM PUSH ALL BRANCHES TO GITHUB
REM ============================================
echo [8/8] Pushing all branches to GitHub...
echo.
echo Pushing main branch...
git push -u origin main
echo ✓ Main branch pushed
echo.
echo Pushing develop branch...
git push -u origin develop
echo ✓ Develop branch pushed
echo.
echo Pushing feature branches...
git push -u origin feature/selenium-scraper
git push -u origin feature/scrapy-spider
git push -u origin feature/data-analysis
git push -u origin feature/documentation
echo ✓ All feature branches pushed
echo.

REM ============================================
REM CREATE RELEASE TAG
REM ============================================
echo Creating release tag v1.0.0...
git tag -a v1.0.0 -m "Version 1.0.0 - Initial Release"
git push origin v1.0.0
echo ✓ Release tag created and pushed
echo.

REM ============================================
REM FINAL STATUS
REM ============================================
echo ==========================================
echo ✓ GIT SETUP COMPLETE
echo ==========================================
echo.
echo Repository Status:
git status
echo.
echo Local Branches:
git branch -a
echo.
echo Remote Configuration:
git remote -v
echo.
echo Tags:
git tag -l
echo.
echo ==========================================
echo GitHub Repository:
echo https://github.com/Nabeelarshad381/job-scraper
echo ==========================================
echo.
echo Next Steps:
echo 1. Visit: https://github.com/Nabeelarshad381/job-scraper
echo 2. Review branches and commit history
echo 3. Start working on feature branches
echo 4. Create pull requests for code review
echo 5. Merge features to develop
echo.
echo For workflow details, see: docs\GIT_WORKFLOW.md
echo ==========================================
echo.
pause
