# Phase 3: Data Analysis & Reporting Guide

**Objective:** Analyze scraped job data and generate insights with visualizations

**File:** `analysis/job_analysis.py`

---

## 🎯 Overview

The analysis script performs comprehensive statistical analysis on the scraped job dataset and generates:
- Top required skills (visualization)
- Top job locations with work environment breakdown
- Top hiring companies
- Entry-level/intern role analysis
- Summary statistics and reports

## 📊 Analysis Components

### JobDataAnalyzer Class

```python
class JobDataAnalyzer:
    def __init__(self, csv_path, output_dir):
        """
        Initialize analyzer with data source and output location.
        
        Args:
            csv_path: Path to jobs.csv from Phase 2
            output_dir: Directory for generated reports
        """
    
    def load_data(self):
        """Load CSV into Pandas DataFrame"""
    
    def clean_data(self):
        """Remove duplicates, handle missing values"""
    
    def analyze_top_skills(self, top_n=15):
        """Extract and visualize top required skills"""
    
    def analyze_top_locations(self, top_n=10):
        """Analyze geographic distribution and work types"""
    
    def analyze_top_companies(self, top_n=10):
        """Identify companies with most openings"""
    
    def analyze_entry_level_roles(self):
        """Count entry-level and internship positions"""
    
    def generate_summary_report(self):
        """Create text summary of all findings"""
    
    def run_full_analysis(self):
        """Execute complete analysis pipeline"""
```

## 💻 Running Analysis

```bash
cd analysis
python job_analysis.py
```

**Output:**
- Console output with statistics
- PNG visualizations in `reports/` directory
- Text summary in `reports/analysis_report.txt`

## 📈 Analysis 1: Top Skills

**Purpose:** Identify most demanded skills in job market

```python
def analyze_top_skills(self, top_n=15):
    """
    Extract required skills from job descriptions.
    
    Extraction methods:
    1. Parse pipe-separated skills field
    2. Match against common skills list
    3. Extract from bullet points
    
    Returns:
        - Bar chart (horizontal): top 15 skills
        - Frequency count for each skill
    """
```

**How it works:**

```python
# Method 1: Parse from skills column
all_skills = []
for skills_str in self.df['required_skills']:
    # Split by pipe: "Python|JavaScript|React"
    skills = skills_str.split('|')
    all_skills.extend(skills)

# Count frequencies
skill_counts = Counter(all_skills)
top_skills = dict(skill_counts.most_common(15))
```

**Output Visualization:**

```
Top 15 Required Skills
────────────────────────────────────
Python          ████████████ 45
JavaScript      ██████████ 38
SQL             █████████ 32
React           ███████ 25
AWS             ██████ 20
Docker          █████ 18
TypeScript      █████ 17
Kubernetes      ████ 14
...
```

**File:** `reports/top_skills.png`

## 📍 Analysis 2: Top Locations

**Purpose:** Understand geographic job distribution and work arrangements

```python
def analyze_top_locations(self, top_n=10):
    """
    Analyze job locations with work environment classification.
    
    Work environment categorization:
    - [REMOTE]: Fully remote position
    - [HYBRID]: Mixed on-site and remote
    - [ON-SITE]: Office-based position
    
    Visualizations:
    1. Bar chart: Top 10 locations
    2. Pie chart: Work environment distribution
    """
```

**Work Environment Detection:**

```python
def _extract_location_type(self, location_str):
    """Extract tag from location string"""
    location_upper = str(location_str).upper()
    
    if '[REMOTE]' in location_upper:
        return 'Remote'
    elif '[HYBRID]' in location_upper:
        return 'Hybrid'
    else:
        return 'On-site'

# Analysis
location_types = df['location'].apply(_extract_location_type)
percentages = location_types.value_counts(normalize=True) * 100
```

**Output Visualizations:**

```
Chart 1: Top 10 Locations
─────────────────────────────
San Francisco       ███████ 25
New York           ██████ 22
Austin             ████ 15
Seattle            ████ 14
Remote             ███ 12
...

Chart 2: Work Environment Distribution
──────────────────────────────────────
Remote: 45%  □□□□□
Hybrid: 30%  □□□
On-site: 25% □□
```

**File:** `reports/top_locations.png`

## 🏢 Analysis 3: Top Hiring Companies

**Purpose:** Identify companies with most job openings

```python
def analyze_top_companies(self, top_n=10):
    """
    Rank companies by number of open positions.
    
    Calculation:
        company_counts = df['company_name'].value_counts()
        top_companies = company_counts.head(10)
    
    Visualization:
        - Horizontal bar chart showing opening count
    """
```

**Implementation:**

```python
company_counts = self.df['company_name'].value_counts().head(10)

# Visualization
plt.figure(figsize=(12, 6))
company_counts.plot(kind='barh', color='mediumseagreen')
plt.title('Top 10 Hiring Companies', fontsize=14, fontweight='bold')
plt.xlabel('Number of Open Positions')
plt.tight_layout()
plt.savefig('reports/top_companies.png', dpi=300)
```

**Output Visualization:**

```
Top 10 Hiring Companies
──────────────────────────────
Ashby           ███████████ 45
TechCorp        ████████ 32
DataHub         ██████ 22
CloudSys        █████ 18
DevOps Inc      ████ 15
...
```

**File:** `reports/top_companies.png`

## 👶 Analysis 4: Entry-Level & Intern Roles

**Purpose:** Quantify opportunities for graduates and interns

```python
def analyze_entry_level_roles(self):
    """
    Identify and count entry-level and internship positions.
    
    Matching criteria:
    - Job title contains: "intern", "junior", "entry-level", "graduate", "trainee"
    - Employment type contains: "intern", "internship"
    
    Returns:
        dict with statistics:
        - total_jobs: Total jobs scraped
        - entry_level_count: Matching entry-level jobs
        - intern_count: Matching internship positions
        - entry_level_percentage: % of entry-level
        - intern_percentage: % of intern roles
    """
```

**Detection Logic:**

```python
entry_level_keywords = ['intern', 'junior', 'entry-level', 'graduate', 'trainee']

# Find entry-level by title
entry_level_mask = df['job_title'].str.lower().str.contains(
    '|'.join(entry_level_keywords), na=False
)
entry_level_df = df[entry_level_mask]

# Find interns by employment type
intern_mask = df['employment_type'].str.lower().str.contains('intern', na=False)
intern_df = df[intern_mask]

# Calculate statistics
entry_level_count = len(entry_level_df)
intern_count = len(intern_df)
entry_level_pct = (entry_level_count / len(df)) * 100
intern_pct = (intern_count / len(df)) * 100
```

**Output Visualizations:**

```
Chart 1: Entry-Level vs Other Roles
───────────────────────────────
Entry-Level: 25%  □□□
Other:       75%  □□□□□□□

Chart 2: Entry-Level Position Breakdown
───────────────────────────────────────
Entry-Level:  ████ 45 positions
Internship:   ██ 15 positions
```

**File:** `reports/entry_level_analysis.png`

## 📝 Analysis 5: Summary Report

**Purpose:** Provide professional text summary of all findings

```python
def generate_summary_report(self):
    """
    Generate comprehensive text report with all metrics.
    
    Contents:
    1. Dataset Overview
    2. Employment Type Breakdown
    3. Department Distribution
    4. Top Locations
    5. Top Companies
    6. Data Quality Metrics
    
    Output: Text file (analysis_report.txt)
    """
```

**Sample Report Output:**

```
======================================================================
JOB SCRAPING ANALYSIS REPORT
Generated: 2026-03-19 12:45:30
======================================================================

DATASET OVERVIEW:
- Total jobs extracted: 487
- Date range: Recently to 2026-03-15
- Unique companies: 23
- Unique locations: 15

EMPLOYMENT TYPE BREAKDOWN:
Full-time:    425 (87%)
Part-time:     35 (7%)
Contract:      20 (4%)
Internship:     7 (2%)

DEPARTMENT BREAKDOWN:
Engineering:      145
Sales:            89
Product:          78
Marketing:        65
Operations:       45
...

TOP 10 LOCATIONS:
San Francisco, CA [REMOTE]:  85
New York, NY [ON-SITE]:      67
Austin, TX [HYBRID]:         45
Seattle, WA [REMOTE]:        38
...

TOP 10 COMPANIES:
Ashby:           45
TechCorp:        32
DataHub:         22
...

DATA QUALITY METRICS:
- Complete job titles:        487 / 487 (100%)
- Complete descriptions:      483 / 487 (99%)
- Jobs with skills:           452 / 487 (93%)

======================================================================
Report generated successfully.
======================================================================
```

**File:** `reports/analysis_report.txt`

## 🛠️ Data Cleaning Steps

```python
def clean_data(self):
    """Prepare data for analysis"""
    
    # 1. Remove duplicates (by job_url)
    df = df.drop_duplicates(subset=['job_url'])
    
    # 2. Handle missing values
    df['location'].fillna('Not specified', inplace=True)
    df['department'].fillna('General', inplace=True)
    df['employment_type'].fillna('Full-time', inplace=True)
    df['required_skills'].fillna('', inplace=True)
    
    # 3. Standardize text
    df['job_title'] = df['job_title'].str.strip()
    df['company_name'] = df['company_name'].str.lower().str.title()
```

## 📊 DataFrame Operations Reference

```python
# Load data
import pandas as pd
df = pd.read_csv('../data/final/jobs.csv')

# Basic info
print(df.shape)              # (487, 10) - rows, columns
print(df.columns)            # Column names
print(df.dtypes)             # Data types
print(df.head())             # First 5 rows
print(df.info())             # Data summary

# Value counts
df['employment_type'].value_counts()     # Count unique values
df['location'].value_counts(normalize=True)  # Proportions

# Filtering
remote_jobs = df[df['location'].str.contains('REMOTE')]
engineering = df[df['department'].str.contains('Engineering')]

# String operations
df[df['job_title'].str.lower().str.contains('intern')]

# Statistics
df['job_description'].str.len().describe()  # Summary stats
```

## 🎨 Visualization Configuration

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Create figure with subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1
data.plot(kind='barh', ax=axes[0], color='coral')
axes[0].set_title('Title', fontweight='bold')

# Plot 2
data.plot(kind='pie', ax=axes[1], autopct='%1.1f%%')
axes[1].set_ylabel('')

# Save
plt.tight_layout()
plt.savefig('output.png', dpi=300)
plt.close()
```

## 🔧 Customization Options

```python
# Change output directory
analyzer = JobDataAnalyzer(
    csv_path='../data/final/jobs.csv',
    output_dir='./custom_reports'  # Custom path
)

# Analyze different top-N
analyzer.analyze_top_skills(top_n=20)      # Top 20 instead of 15
analyzer.analyze_top_locations(top_n=15)   # Top 15 locations

# Run specific analyses
analyzer.load_data()
analyzer.clean_data()
analyzer.analyze_top_skills()          # Only skills
```

## 📋 Output Files Summary

| File | Content |
|------|---------|
| `reports/top_skills.png` | Top 15 required skills bar chart |
| `reports/top_locations.png` | Geographic distribution + pie chart |
| `reports/top_companies.png` | Top 10 hiring companies |
| `reports/entry_level_analysis.png` | Entry-level role breakdown |
| `reports/analysis_report.txt` | Complete text summary |

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "FileNotFoundError: jobs.csv not found" | Run Phase 2 (Scrapy) first |
| "No jobs extracted" message | Check Phase 1 & 2 output files |
| Charts not displaying | Verify matplotlib, seaborn installed |
| Permission denied on reports/ | Check folder permissions |

## 🚀 Performance

```
Dataset Size          Analysis Time
─────────────────────────────────
100 jobs              < 1 second
500 jobs              ~2 seconds
1000 jobs             ~4 seconds
5000 jobs             ~15 seconds
```

---

*Reference: Pandas 2.0+, Matplotlib 3.7+, Python 3.8+*
