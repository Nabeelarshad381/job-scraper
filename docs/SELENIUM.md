# Phase 1: Selenium Browser Automation Guide

**Objective:** Extract job posting URLs from Ashby HQ portal using Selenium WebDriver

**File:** `selenium/ashby_scraper.py`

---

## 🎯 Overview

The Selenium scraper automates browser navigation to the Ashby HQ job portal and extracts URLs to individual job postings. It handles JavaScript-rendered content and implements industry-standard practices for robust automation.

## 🔧 Key Components

### 1. AshbyJobScraper Class

Main class orchestrating the scraping workflow:

```python
class AshbyJobScraper:
    def __init__(self):
        self.base_url = "https://jobs.ashbyhq.com/ashby-embed-demo-org"
        self.job_links = []
        self.polite_delay = 2  # Ethical compliance
```

### 2. WebDriver Setup

```python
def setup_driver(self):
    edge_options = EdgeOptions()
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    self.driver = webdriver.Edge(options=edge_options)
    self.wait = WebDriverWait(self.driver, timeout=15)
```

**Why these options?**
- `--no-sandbox`: Allows running in restricted environments
- `--disable-dev-shm-usage`: Prevents memory issues
- `disable-blink-features`: Prevents detection as automated browser
- `WebDriverWait`: Explicit waits up to 15 seconds

### 3. Robots.txt Compliance Check

```python
def check_robots_txt(self):
    """Verify ethical scraping practices before starting."""
    self.driver.get("https://jobs.ashbyhq.com/robots.txt")
    # Check and log compliance
```

### 4. JavaScript-Content Loading

```python
def scroll_to_load_all_jobs(self, max_scrolls=10):
    """Scroll page to trigger lazy loading of job cards."""
    last_height = self.driver.execute_script("return document.body.scrollHeight")
    
    while scroll_count < max_scrolls:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait and check if new content loaded
```

**How it works:**
1. Get current page height
2. Scroll to bottom
3. Wait 2 seconds (polite delay)
4. Compare new height with old height
5. If height changed, repeat; if not, all jobs loaded

### 5. URL Extraction

```python
def extract_job_links(self):
    """Extract job detail page URLs from job board."""
    job_elements = self.wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[@class='job-board-item'] | //a[contains(@href, '/job/')]"))
    )
    
    for element in job_elements:
        url = element.get_attribute('href')
        if url and 'jobs.ashbyhq.com' in url:
            self.job_links.append(url)
```

## 📊 XPath/CSS Selectors Reference

The spider uses multiple selector strategies for robustness:

```python
# Job Title
h1::text
h1 //text()
[data-testid="job-title"]::text

# Job Links
//a[@class='job-board-item']
//a[contains(@href, '/job/')]
[data-testid='job-board']

# Company Name
h2::text
//a[contains(@href, "ashby")]/text()

# Location
[class*="location"]::text
//text()[contains(., "Remote")]
```

## 🔄 Complete Workflow

**Sequence:** Setup → Navigate → Load → Extract → Save → Verify

```
1. Initialize WebDriver
   ↓
2. Check robots.txt compliance
   ↓
3. Navigate to Ashby portal
   ↓
4. Scroll to load all job cards (infinite scroll)
   ↓
5. Extract job URLs from DOM
   ↓
6. Save URLs to CSV
   ↓
7. Verify sample links work
   ↓
8. Close WebDriver
```

## 💻 Running Selenium Scraper

**Basic execution:**
```bash
cd selenium
python ashby_scraper.py
```

**With logging:**
```bash
# Logging automatically saved to ../logs/selenium_scraper.log
tail -f ../logs/selenium_scraper.log
```

**Custom configuration:**
```python
scraper = AshbyJobScraper()
scraper.base_url = "https://alternative-url.com"
scraper.polite_delay = 3  # Increase delay
scraper.run()
```

## 📤 Output Format

**File:** `data/raw/job_links.csv`

```csv
job_url,extracted_timestamp
https://jobs.ashbyhq.com/ashby-embed-demo-org/job/engineering-001,2026-03-19T10:15:30.123456
https://jobs.ashbyhq.com/ashby-embed-demo-org/job/sales-004,2026-03-19T10:15:32.654321
```

## 🛡️ Error Handling

### TimeoutException
**Cause:** Element not found within 15 seconds
**Solution:** Increase timeout or verify HTML structure changed

### StaleElementReferenceException
**Cause:** Element became stale after page reload
**Solution:** Automatically caught and skipped

### NoSuchElementException
**Cause:** Selector doesn't match current DOM
**Solution:** Log warning and continue with next element

## 🔧 Customization

### Change Browser
```python
# Use Chrome instead of Edge
from selenium.webdriver.chrome.options import Options as ChromeOptions
self.driver = webdriver.Chrome(options=edge_options)
```

### Increase Wait Time
```python
self.wait = WebDriverWait(self.driver, timeout=30)  # 30 seconds
```

### Modify Polite Delay
```python
self.polite_delay = 5  # 5 seconds between requests
```

### Run in Headless Mode
```python
edge_options.add_argument("--headless")  # Hide browser window
```

## 📊 Sample Output Log

```
2026-03-19 10:15:20,123 - INFO - ================================================== ==
2026-03-19 10:15:20,124 - INFO - Starting Ashby Job Scraper
2026-03-19 10:15:20,125 - INFO - ================================================== ==
2026-03-19 10:15:21,456 - INFO - Initializing WebDriver...
2026-03-19 10:15:23,789 - INFO - WebDriver initialized successfully
2026-03-19 10:15:24,012 - INFO - Checking robots.txt compliance...
2026-03-19 10:15:26,345 - INFO - Navigating to https://jobs.ashbyhq.com/...
2026-03-19 10:15:28,678 - INFO - Job board loaded successfully
2026-03-19 10:15:28,679 - INFO - Starting infinite scroll to load all jobs...
2026-03-19 10:15:30,901 - INFO - Scrolled 1/10 times
2026-03-19 10:15:32,234 - INFO - Scrolled 2/10 times
2026-03-19 10:15:34,567 - INFO - Scrolled 3/10 times
2026-03-19 10:15:34,890 - INFO - Reached end of jobs list after 3 scrolls
2026-03-19 10:15:35,123 - INFO - Extracting job links...
2026-03-19 10:15:35,456 - INFO - Found 247 job elements
2026-03-19 10:15:36,789 - INFO - Total unique job links extracted: 245
2026-03-19 10:15:36,802 - INFO - Saving 245 job links to ../data/raw/job_links.csv...
2026-03-19 10:15:36,845 - INFO - Successfully saved 245 job links to CSV
2026-03-19 10:15:36,846 - INFO - Verifying 3 sample links...
2026-03-19 10:15:38,123 - INFO - [1] ✓ Link verified
2026-03-19 10:15:40,456 - INFO - [2] ✓ Link verified
2026-03-19 10:15:42,789 - INFO - [3] ✓ Link verified
2026-03-19 10:15:42,810 - INFO - Closing WebDriver...
2026-03-19 10:15:43,123 - INFO - WebDriver closed successfully
2026-03-19 10:15:43,124 - INFO - ================================================== ==
2026-03-19 10:15:43,125 - INFO - Scraping completed successfully!
2026-03-19 10:15:43,126 - INFO - Total jobs extracted: 245
2026-03-19 10:15:43,127 - INFO - ================================================== ==
```

## ⚠️ Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "WebDriver executable not found" | Missing Edge driver | `pip install webdriver-manager` |
| "Timeout waiting for job board" | Slow network or page changes | Increase timeout to 30 seconds |
| "No jobs extracted" | HTML structure changed | Update CSS/XPath selectors |
| "Stale element" warnings | Page reloading during scrape | Normal, automatically handled |

## 🚀 Performance Optimization

**Current settings (default):**
- Pages scrolled: 10 max
- Polite delay: 2 seconds
- Wait timeout: 15 seconds
- Estimated duration: 3-5 minutes

**For faster execution (less thorough):**
```python
scraper.scroll_to_load_all_jobs(max_scrolls=3)  # Fewer scrolls
```

---

*Reference: Selenium 4.10+, Edge WebDriver, Python 3.8+*
