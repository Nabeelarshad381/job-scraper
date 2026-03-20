# Quick Start - 3 Job Sources with Data Scientists Filter

**Your project now scrapes from 3 sources and automatically filters for Data Scientists & ML Engineers!**

---

## 🚀 Quick Run (All 3 Spiders)

```bash
cd c:\Users\Lenovo\job scraper
python run_all_spiders.py
```

This will:
1. ✅ Run Ashby spider
2. ✅ Run Greenhouse spider  
3. ✅ Run Lever (Netflix) spider
4. ✅ Filter for Data Scientists & ML Engineers only
5. ✅ Combine all results
6. ✅ Generate job statistics

---

## 📊 Individual Spiders

Run one spider at a time:

```bash
# Ashby BeviCareers
scrapy crawl ashby_spider

# Greenhouse BeviCareers
scrapy crawl greenhouse_spider

# Lever Netflix
scrapy crawl lever_spider
```

---

## 📁 Data Flow

```
Job Websites
    ↓
Selenium/Spiders extract links → data/raw/job_links*.csv
    ↓
Spiders extract details
    ↓
ROLE FILTER: Keep only Data Scientists & ML Engineers
    ↓
Clean & normalize data
    ↓
Export → data/final/jobs.csv
    ↓
Analysis & Visualizations → analysis/reports/
```

---

## 🎯 What Gets Filtered

**Accepted Roles:**
- ✅ Data Scientist
- ✅ ML Engineer
- ✅ Machine Learning Engineer
- ✅ Data Engineer

**Example Titles:**
- ✅ "Senior Data Scientist"
- ✅ "ML Engineer (Remote)"
- ✅ "Junior Data Engineer"
- ❌ "Software Engineer" (REJECTED)
- ❌ "Product Manager" (REJECTED)

---

## 📈 Expected Results

| Metric | Target |
|--------|--------|
| Total jobs scraped | 200+ |
| Data Science matches | 40-80 |
| Filter acceptance rate | 15-25% |
| Top skills | Python, SQL, ML, TensorFlow |
| Top locations | Remote, SF, NYC |
| Entry-level positions | 10-20% |

---

## 🔧 Customize Roles

Edit spider files to filter different roles:

**File:** `scrapy_project/ashby_spider/spiders/ashby_spider.py` (line ~25)

```python
self.target_roles = ['Data Scientist', 'ML Engineer', 'Machine Learning']
```

Change to:

```python
self.target_roles = ['Backend Engineer', 'DevOps', 'Cloud Architect']
```

Same for `greenhouse_spider.py` and `lever_spider.py`

---

## 📖 Documentation

- [MULTIPLE_SOURCES.md](docs/MULTIPLE_SOURCES.md) - Complete multi-source guide
- [SCRAPY.md](docs/SCRAPY.md) - Scrapy framework details
- [COMMANDS.md](docs/COMMANDS.md) - All executable commands

---

## ✅ Course Requirements Met

✓ Multiple job sources (3+)  
✓ Boolean search/filtering (target role filtering)  
✓ Pagination/scrolling (Selenium)  
✓ 9 required fields extracted  
✓ CSV export  
✓ Data analysis & insights  
✓ GitHub with proper branching  

---

**Status:** 🚀 Ready to run! Execute `python run_all_spiders.py` now

