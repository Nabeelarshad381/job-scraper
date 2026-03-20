# Professional Job Scraping System - Hybrid Selenium + Scrapy

**Course:** Tools & Techniques for Data Science  
**University:** University of Central Punjab  
**Date:** March 2026  
**Team:** Senior Data Engineers

## 📋 Project Overview

This is a professional-grade, production-ready job scraping system designed for the [Ashby HQ Job Portal](https://jobs.ashbyhq.com/ashby-embed-demo-org). The system implements a hybrid approach combining:

- **Selenium WebDriver** for JavaScript-rendered content and browser automation
- **Scrapy Framework** for scalable, structured data extraction
- **Pandas + Matplotlib** for data analysis and visualization
- **Industry best practices** for ethical scraping and data handling

### Key Features

✅ **Ethical Compliance**
- Robots.txt verification
- 2-second polite delay between requests
- NO authentication bypass or private data collection
- Automatic rate limiting

✅ **Robust Architecture**
- Explicit waits and error handling
- Stale element reference recovery
- Structured logging and monitoring
- CSV data persistence

✅ **Complete Data Pipeline**
- 9 required fields per job posting
- Skill extraction and tagging
- Location type classification (Remote/Hybrid/On-site)
- Comprehensive analysis and reporting

---

## 🗂️ Project Structure

```
job scraper/
├── selenium/                   # Phase 1: Selenium automation
│   └── ashby_scraper.py       # Browser automation script
├── scrapy_project/            # Phase 2: Scrapy extraction
│   ├── ashby_spider/
│   │   ├── spiders/
│   │   │   └── ashby_spider.py  # Main spider
│   │   ├── items.py           # Scrapy item definitions
│   │   ├── pipelines.py       # Data processing pipelines
│   │   └── settings.py        # Scrapy configuration
│   └── setup.py               # Scrapy project setup
├── data/
│   ├── raw/                   # Intermediate data
│   │   └── job_links.csv      # URLs from Selenium
│   └── final/                 # Final cleaned data
│       └── jobs.csv           # Complete job dataset
├── analysis/                  # Phase 3: Analysis
│   ├── job_analysis.py        # Analytics script
│   └── reports/               # Generated reports
├── docs/                      # Documentation
├── run_pipeline.py            # Complete workflow orchestrator
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git exclusions
└── README.md                  # This file
```

---

## 🚀 Quick Start Guide

### Prerequisites

- **Python 3.8+**
- **Git**
- **Microsoft Edge** or **Chrome** browser (for Selenium)

### Installation

1. **Clone the repository**
```bash
git clone <repository_url>
cd job\ scraper
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Enable WebDriver**
```bash
# WebDriver Manager will auto-download Edge driver
# First run may take a moment for driver setup
```

---

## 📊 Three-Phase Workflow

### Phase 1: Selenium Automation (Job Link Extraction)

**File:** `selenium/ashby_scraper.py`

Automates browser navigation to extract job posting URLs.

```bash
cd selenium
python ashby_scraper.py
```

**What it does:**
- Navigates to Ashby job portal
- Implements infinite scroll to load all jobs
- Extracts job detail page URLs
- Validates sample links
- Saves to `data/raw/job_links.csv`

**Output:**
```csv
job_url,extracted_timestamp
https://jobs.ashbyhq.com/ashby-embed-demo-org/job/...,2026-03-19T10:15:30.123456
...
```

**Key Features:**
- ✓ Explicit waits (up to 15 seconds)
- ✓ Scroll automation with height detection
- ✓ Robots.txt compliance check
- ✓ Stale element handling
- ✓ Comprehensive logging

---

### Phase 2: Scrapy Data Extraction (Job Details)

**File:** `scrapy_project/ashby_spider/spiders/ashby_spider.py`

Extracts structured job data from each posting.

```bash
cd scrapy_project
scrapy crawl ashby_jobs
```

**9 Required Fields Extracted:**

1. **job_title** - Position name (e.g., "Software Engineer")
2. **company_name** - Hiring company (e.g., "Ashby Demo Org")
3. **location** - Job location with work type tag:
   - `New York, NY [ON-SITE]`
   - `San Francisco, CA [REMOTE]`
   - `Austin, TX [HYBRID]`
4. **department** - Team/Department (e.g., "Engineering", "Sales")
5. **employment_type** - Type of position
   - Full-time, Part-time, Contract, Internship
6. **posted_date** - Publication date
7. **job_url** - Direct link to job posting
8. **job_description** - Complete job description text
9. **required_skills** - Extracted skills (pipe-separated):
   - `Python|JavaScript|React|SQL`

**Output:** `data/final/jobs.csv`

**Key Features:**
- ✓ Reads URLs from Phase 1 output
- ✓ Configurable polite delays (2 seconds)
- ✓ Item validation before export
- ✓ Skill extraction & parsing
- ✓ Location type tagging
- ✓ Automatic retry (up to 3 attempts)
- ✓ CSV export with proper encoding

---

### Phase 3: Analysis & Reporting

**File:** `analysis/job_analysis.py`

Generates insights and visualizations from job data.

```bash
cd analysis
python job_analysis.py
```

**Analysis Produced:**

1. **Top Skills Analysis**
   - Identifies 15 most required skills
   - Bar chart visualization
   - Output: `reports/top_skills.png`

2. **Top Locations**
   - Geographic distribution of jobs
   - Work environment breakdown (Remote/Hybrid/On-site)
   - Output: `reports/top_locations.png`

3. **Top Hiring Companies**
   - Companies with most open positions
   - Bar chart ranking
   - Output: `reports/top_companies.png`

4. **Entry-Level Analysis**
   - Count and percentage of junior/intern roles
   - Pie charts and statistics
   - Output: `reports/entry_level_analysis.png`

5. **Summary Report**
   - Text summary of all findings
   - Data quality metrics
   - Output: `reports/analysis_report.txt`

---

## ⚙️ Running the Complete Pipeline

Execute all three phases automatically:

```bash
python run_pipeline.py
```

This will:
1. Run Selenium script (extracts job URLs)
2. Run Scrapy spider (extracts job details)
3. Run analysis script (generates reports)

With progress logging and error handling.

---

## 🔧 Configuration

### Selenium Settings
**File:** `selenium/ashby_scraper.py`

```python
self.base_url = "https://jobs.ashbyhq.com/ashby-embed-demo-org"
self.polite_delay = 2  # Seconds between requests
self.wait = WebDriverWait(driver, timeout=15)  # Max wait time
```

### Scrapy Settings
**File:** `scrapy_project/ashby_spider/settings.py`

```python
DOWNLOAD_DELAY = 2  # Polite delay between requests
CONCURRENT_REQUESTS = 1  # Sequential requests
AUTOTHROTTLE_ENABLED = True  # Automatic throttling
RETRY_TIMES = 3  # Retry failed requests
```

### Analysis Output
**File:** `analysis/job_analysis.py`

```python
analyzer = JobDataAnalyzer(
    csv_path='../data/final/jobs.csv',
    output_dir='./reports'
)
```

---

## 📝 Git Workflow & Branching Strategy

This project follows professional Git branching conventions.

### Initial Setup

**Initialize repository:**
```bash
git init
git config user.name "Your Name"
git config user.email "your.email@university.edu"
git add .
git commit -m "Initial commit: Project scaffold and documentation"
```

### Branching Strategy

**Main branches:**
- `main` - Production-ready code (stable releases)
- `develop` - Integration branch for features

**Feature workflow:**
```
feature/selenium-scraper
    ↓ (merge with PR)
develop
    ↓ (release ready)
main
```

### Creating Feature Branch

```bash
# Create and switch to feature branch
cd job\ scraper
git checkout -b feature/selenium-scraper

# Make changes, test, and commit
git add selenium/ashby_scraper.py
git commit -m "feat(selenium): Implement job link extraction with scrolling"

# Push feature branch
git push -u origin feature/selenium-scraper
```

### Merging Feature into Develop

**Step 1: Create pull request (recommended for team environments)**
```bash
# (On GitHub/GitLab/Bitbucket - create PR from feature to develop)
```

**Or locally merge:**

```bash
# Switch to develop branch
git checkout develop

# Ensure develop is up to date
git pull origin develop

# Merge feature branch
git merge feature/selenium-scraper

# Delete feature branch (after merge)
git branch -d feature/selenium-scraper
git push origin --delete feature/selenium-scraper

# Push to remote
git push origin develop
```

### Complete Git Command Sequence for First Feature

```bash
# Phase 1: Initialize repo
cd c:\Users\Lenovo\job\ scraper
git init
git config user.name "Data Engineer"
git config user.email "engineer@university.edu"
git add .
git commit -m "Initial: Complete project scaffold"

# Phase 2: Create develop branch
git branch develop
git push -u origin develop

# Phase 3: Create feature branch
git checkout -b feature/selenium-scraper

# Phase 4: Make and commit changes
git add selenium/
git commit -m "feat(selenium): Implement Ashby portal scraper with explicit waits"

# Phase 5: Merge into develop
git checkout develop
git pull origin develop
git merge feature/selenium-scraper -m "Merge feature/selenium-scraper into develop"
git branch -d feature/selenium-scraper

# Phase 6: Push to remote
git push origin develop

# (Optional) Release to main
git checkout main
git merge develop -m "Release: v1.0.0 - Initial stable release"
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin main --tags
```

---

## 🔍 Troubleshooting

### Common Issues

**Issue: "WebDriver executable not found"**
```bash
# Solution: WebDriver Manager will auto-download
pip install webdriver-manager
```

**Issue: "Timeout waiting for job board to load"**
- Check internet connection
- Verify Ashby portal is accessible
- Increase timeout in settings: `WebDriverWait(driver, timeout=30)`

**Issue: "No jobs extracted"**
- Ashby portal may have updated HTML structure
- Update CSS selectors in `ashby_spider.py`
- Check browser console for JavaScript errors

**Issue: "CSV file not found" error in Scrapy**
- Ensure Selenium script completed successfully
- Check `data/raw/job_links.csv` exists
- Run: `cd selenium && python ashby_scraper.py`

### Verifying Installation

```bash
# Test Selenium
cd selenium
python -c "from selenium import webdriver; print('✓ Selenium OK')"

# Test Scrapy
cd ../scrapy_project
scrapy --version

# Test dependencies
cd ..
python -c "import pandas, matplotlib; print('✓ Analysis tools OK')"
```

---

## 💾 Data Format Reference

### Job Links CSV (`data/raw/job_links.csv`)

```csv
job_url,extracted_timestamp
https://jobs.ashbyhq.com/ashby-embed-demo-org/job/12345,2026-03-19T10:15:30.123456
```

### Final Jobs CSV (`data/final/jobs.csv`)

```csv
job_title,company_name,location,department,employment_type,posted_date,job_url,job_description,required_skills,extracted_timestamp
"Software Engineer","Ashby Demo Org","San Francisco, CA [REMOTE]","Engineering","Full-time","March 2026","https://jobs.ashbyhq.com/...","Build scalable systems...","Python|JavaScript|React|SQL",2026-03-19T11:20:45.987654
```

---

## 📚 API Reference

### AshbyJobScraper Class

```python
scraper = AshbyJobScraper()
scraper.setup_driver()              # Initialize WebDriver
scraper.navigate_to_jobs_page()     # Navigate to portal
scraper.scroll_to_load_all_jobs()   # Load all jobs via scroll
scraper.extract_job_links()         # Extract URLs
scraper.save_links_to_csv()         # Save to CSV
scraper.run()                       # Run complete workflow
```

### Scrapy Spider

```bash
scrapy crawl ashby_jobs             # Run spider
scrapy list                         # List available spiders
scrapy shell 'url'                  # Interactive shell
```

---

## 🔐 Ethical Compliance Checklist

✅ **Robots.txt Compliance**
- [ ] Spider checks and respects robots.txt
- [ ] ROBOTSTXT_OBEY = True in Scrapy settings
- [ ] Verified before scraping begins

✅ **Rate Limiting**
- [ ] 2-second delay between requests
- [ ] Sequential requests (CONCURRENT_REQUESTS = 1)
- [ ] Auto-throttle enabled

✅ **Data Privacy**
- [ ] No login/authentication bypass
- [ ] Only public job posting data collected
- [ ] PII (emails, phone numbers) excluded
- [ ] User agents properly identified

✅ **Technical Practice**
- [ ] Server load monitoring
- [ ] Error handling and recovery
- [ ] Request timeout configuration
- [ ] Comprehensive logging

---

## 📈 Performance Metrics

**Expected Performance (Approximate):**

| Phase | Duration | Records |
|-------|----------|---------|
| Selenium (Phase 1) | 2-5 minutes | ~100-500 job URLs |
| Scrapy (Phase 2) | 5-15 minutes* | ~100-500 job details |
| Analysis (Phase 3) | < 1 minute | 5+ visualizations |
| **Total Pipeline** | **10-25 minutes** | **Professional Report** |

*Depends on number of jobs and network speed

---

## 👥 Team Collaboration

**Git Workflow for Team:**

1. **Developer A:**
   ```bash
   git checkout -b feature/selenium-enhancement
   # ... make changes ...
   git push -u origin feature/selenium-enhancement
   # Create Pull Request on GitHub
   ```

2. **Code Review & Merge:**
   - Team reviews changes
   - Merge to develop after approval
   - Delete feature branch

3. **Weekly Integration:**
   ```bash
   git checkout develop
   git pull origin develop
   # Test all features together
   ```

---

## 📞 Support & Documentation

**Phase-Specific Docs:**
- [Selenium Script Guide](SELENIUM.md)
- [Scrapy Spider Guide](SCRAPY.md)
- [Analysis Script Guide](ANALYSIS.md)

**Additional Resources:**
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Scrapy Documentation](https://docs.scrapy.org/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## 📄 License & Attribution

**Course:** Tools & Techniques for Data Science  
**Instructor:** [Course Instructor Name]  
**University:** University of Central Punjab  
**Year:** 2026  
**Assignment:** Professional Data Science Project - Hybrid Job Scraping System

---

## ✨ Conclusion

This project demonstrates professional data engineering practices:

- ✓ Robust error handling and logging
- ✓ Ethical web scraping compliance
- ✓ Structured data extraction
- ✓ Comprehensive analysis and visualization
- ✓ Production-grade code quality
- ✓ Professional Git workflow
- ✓ Complete documentation

**Ready for deployment and team collaboration!**

---

*Last Updated: March 19, 2026*
