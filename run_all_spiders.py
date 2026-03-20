#!/usr/bin/env python3
"""
Run All Job Spiders - Combined Execution Script
Scrapes Data Scientists and ML Engineers from:
1. BeviCareers (Greenhouse)
2. Netflix (Lever)
3. Ashby (BeviCareers)

Combines all results into a single jobs.csv file
"""

import os
import sys
import subprocess
import csv
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MultiSpiderRunner:
    """Run multiple spiders and combine results"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        # Scrapy "active project" directory (must contain scrapy.cfg).
        self.scrapy_project_dir = self.project_dir / 'scrapy_project'
        self.selenium_dir = self.project_dir / 'selenium'
        self.data_dir = self.project_dir / 'data' / 'final'
        self.ashby_job_links_csv = self.project_dir / 'data' / 'raw' / 'job_links.csv'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        # Spider names must match the `name = ...` attribute inside each spider.
        self.spiders = ['ashby_jobs', 'greenhouse_spider', 'lever_spider']
        self.combined_file = self.data_dir / 'jobs.csv'
        self.all_jobs = []
        
    def run_all_spiders(self):
        """Execute all spiders sequentially"""
        logger.info("\n" + "="*70)
        logger.info("STARTING MULTI-SPIDER JOB EXTRACTION")
        logger.info("="*70 + "\n")
        
        logger.info(f"Target: Data Scientists & ML Engineers")
        logger.info(f"Sources: Ashby, Greenhouse, Lever (Netflix)")
        logger.info(f"Output: {self.combined_file}\n")
        
        for i, spider in enumerate(self.spiders, 1):
            logger.info(f"\n{'─'*70}")
            logger.info(f"[{i}/{len(self.spiders)}] Running {spider.upper()}")
            logger.info(f"{'─'*70}\n")
            
            try:
                # Ashby spider depends on Selenium Phase 1 job links.
                if spider == 'ashby_jobs':
                    self._ensure_ashby_job_links()
                self._run_spider(spider)
            except Exception as e:
                logger.error(f"Error running {spider}: {e}")
                continue
        
        logger.info("\n" + "="*70)
        logger.info("COMBINING RESULTS")
        logger.info("="*70 + "\n")
        
        self._combine_results()

    def _ensure_ashby_job_links(self):
        """Ensure `data/raw/job_links.csv` exists before crawling Ashby."""
        # Treat empty files as missing.
        if self.ashby_job_links_csv.exists() and self.ashby_job_links_csv.stat().st_size > 0:
            logger.info(f"✓ Phase 1 job links found: {self.ashby_job_links_csv}")
            return

        logger.info("Phase 1 prerequisites missing; running Selenium link extraction (Ashby)...")
        cmd = [sys.executable, "ashby_scraper.py"]
        result = subprocess.run(
            cmd,
            cwd=str(self.selenium_dir),
            capture_output=True,
            text=True
        )
        if result.stdout:
            logger.info(result.stdout)
        if result.stderr:
            logger.warning(result.stderr)
        if result.returncode != 0:
            raise Exception("Selenium Phase 1 failed; cannot proceed with Ashby crawl.")

        if not self.ashby_job_links_csv.exists() or self.ashby_job_links_csv.stat().st_size == 0:
            raise Exception("Selenium Phase 1 completed but job_links.csv is still missing/empty.")

        logger.info(f"✓ Selenium Phase 1 completed: {self.ashby_job_links_csv}")
        
    def _run_spider(self, spider_name):
        """Run individual spider using Scrapy"""
        cmd = [
            sys.executable, '-m', 'scrapy', 'crawl', spider_name
        ]
        
        logger.info(f"Executing: {' '.join(cmd)}\n")
        
        result = subprocess.run(
            cmd,
            cwd=str(self.scrapy_project_dir),
            capture_output=True,
            text=True
        )
        
        # Log spider output
        if result.stdout:
            logger.info(result.stdout)
        
        if result.stderr:
            logger.warning(result.stderr)
        
        if result.returncode != 0:
            raise Exception(f"Spider {spider_name} failed with code {result.returncode}")
        
        logger.info(f"✓ {spider_name} completed successfully")
    
    def _combine_results(self):
        """Combine CSV results from all spiders"""
        try:
            # Define fields
            fields = [
                'job_title', 'company_name', 'location', 'department',
                'employment_type', 'posted_date', 'job_url', 'job_description',
                'required_skills', 'source'
            ]
            
            # Collect all jobs
            all_jobs = []
            
            # Read from main jobs.csv (contains all spider results)
            if self.combined_file.exists():
                with open(self.combined_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        all_jobs.append(row)
            
            # Generate summary statistics
            logger.info(f"\n{'─'*70}")
            logger.info("EXTRACTION SUMMARY")
            logger.info(f"{'─'*70}\n")
            
            total_jobs = len(all_jobs)
            logger.info(f"Total Data Science/ML Jobs Found: {total_jobs}")
            
            # Count by source
            source_counts = {}
            for job in all_jobs:
                source = job.get('source', 'unknown')
                source_counts[source] = source_counts.get(source, 0) + 1
            
            logger.info(f"\nJobs by Source:")
            for source, count in sorted(source_counts.items()):
                logger.info(f"  • {source}: {count} jobs")
            
            # Count by company
            company_counts = {}
            for job in all_jobs:
                company = job.get('company_name', 'unknown')
                company_counts[company] = company_counts.get(company, 0) + 1
            
            logger.info(f"\nTop Companies:")
            for company, count in sorted(company_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                logger.info(f"  • {company}: {count} positions")
            
            # Count by location
            location_counts = {}
            for job in all_jobs:
                location = job.get('location', 'unknown')
                # Extract base location (before the bracket)
                base_location = location.split('[')[0].strip() if '[' in location else location
                location_counts[base_location] = location_counts.get(base_location, 0) + 1
            
            logger.info(f"\nTop Locations:")
            for location, count in sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                logger.info(f"  • {location}: {count} positions")
            
            # Count employment types
            employment_counts = {}
            for job in all_jobs:
                emp_type = job.get('employment_type', 'unknown')
                employment_counts[emp_type] = employment_counts.get(emp_type, 0) + 1
            
            logger.info(f"\nEmployment Types:")
            for emp_type, count in sorted(employment_counts.items(), key=lambda x: x[1], reverse=True):
                logger.info(f"  • {emp_type}: {count} positions")
            
            # Identify entry-level positions
            entry_level = [job for job in all_jobs 
                          if any(word in job.get('job_title', '').lower() 
                                for word in ['junior', 'entry', 'intern', 'graduate'])]
            
            if total_jobs > 0:
                logger.info(f"\nEntry-Level Positions: {len(entry_level)} ({len(entry_level)/total_jobs*100:.1f}%)")
            else:
                logger.info(f"\nEntry-Level Positions: 0 (no jobs scraped)")
            
            logger.info(f"\n{'─'*70}")
            logger.info(f"✓ Combined results saved to: {self.combined_file}")
            logger.info(f"✓ Total records: {total_jobs}")
            logger.info(f"{'─'*70}\n")
            
        except Exception as e:
            logger.error(f"Error combining results: {e}")
            raise
    
    def run(self):
        """Main execution"""
        try:
            self.run_all_spiders()
            logger.info("\n" + "="*70)
            logger.info("✓ ALL SPIDERS COMPLETED SUCCESSFULLY")
            logger.info("="*70 + "\n")
            
            logger.info("NEXT STEPS:")
            logger.info("1. Review results in: data/final/jobs.csv")
            logger.info("2. Run analysis: python analysis/job_analysis.py")
            logger.info("3. Check reports: analysis/reports/analysis_report.txt")
            logger.info("\n" + "="*70 + "\n")
            
        except Exception as e:
            logger.error(f"\n❌ EXECUTION FAILED: {e}\n")
            sys.exit(1)


if __name__ == '__main__':
    runner = MultiSpiderRunner()
    runner.run()
