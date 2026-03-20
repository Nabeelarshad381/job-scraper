"""
Pipeline runner script - executes the complete job scraping workflow.

Usage:
    python run_pipeline.py

Workflow:
    1. Run Selenium script to extract job URLs
    2. Run Scrapy spider to extract job details
    3. Run analysis to generate reports
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_command(cmd, description):
    """
    Execute a shell command and handle errors.
    
    Args:
        cmd (str or list): Command to run
        description (str): Description of what's running
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info(f"\n{'='*70}")
        logger.info(f"[PHASE] {description}")
        logger.info(f"{'='*70}\n")
        
        result = subprocess.run(cmd, shell=True, check=True, capture_output=False)
        
        logger.info(f"\n✓ {description} completed successfully\n")
        return True
    
    except subprocess.CalledProcessError as e:
        logger.error(f"\n✗ {description} failed with error code {e.returncode}\n")
        return False
    except Exception as e:
        logger.error(f"\n✗ {description} encountered exception: {e}\n")
        return False


def check_prerequisites():
    """Check if all required packages are installed."""
    try:
        logger.info("Checking prerequisites...")
        
        import selenium
        import scrapy
        import pandas
        import matplotlib
        
        logger.info("✓ All required packages are installed")
        return True
    
    except ImportError as e:
        logger.error(f"✗ Missing package: {e}")
        logger.info("Run: pip install -r requirements.txt")
        return False


def main():
    """Execute the complete job scraping pipeline."""
    
    logger.info("\n" + "="*70)
    logger.info("JOB SCRAPING PIPELINE - COMPLETE WORKFLOW")
    logger.info("University of Central Punjab - Tools & Techniques for DS")
    logger.info("="*70 + "\n")
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Phase 1: Selenium Scraping
    logger.info("\n[SEQUENCE] Starting Phase 1 - Selenium Browser Automation...")
    phase1_success = run_command(
        "cd selenium && python ashby_scraper.py",
        "Phase 1: Selenium Job Link Extraction"
    )
    
    if not phase1_success:
        logger.error("Phase 1 failed. Stopping pipeline.")
        sys.exit(1)
    
    # Check if job links were created
    job_links_path = "data/raw/job_links.csv"
    if not Path(job_links_path).exists():
        logger.error(f"Job links file not found: {job_links_path}")
        logger.error("Phase 1 may have completed without scraping jobs.")
        sys.exit(1)
    
    time.sleep(2)  # Polite delay between phases
    
    # Phase 2: Scrapy Extraction
    logger.info("\n[SEQUENCE] Starting Phase 2 - Scrapy Job Details Extraction...")
    phase2_success = run_command(
        "cd scrapy_project && scrapy crawl ashby_jobs",
        "Phase 2: Scrapy Job Details Extraction"
    )
    
    if not phase2_success:
        logger.warning("Phase 2 encountered issues but may have collected some data.")
    
    # Check if jobs CSV was created
    jobs_csv_path = "data/final/jobs.csv"
    if Path(jobs_csv_path).exists():
        logger.info(f"✓ Job data file created: {jobs_csv_path}")
    else:
        logger.warning(f"Job data file not found: {jobs_csv_path}")
    
    time.sleep(2)  # Polite delay between phases
    
    # Phase 3: Analysis & Reports
    logger.info("\n[SEQUENCE] Starting Phase 3 - Data Analysis & Reporting...")
    phase3_success = run_command(
        "cd analysis && python job_analysis.py",
        "Phase 3: Job Data Analysis & Visualization"
    )
    
    if not phase3_success:
        logger.warning("Phase 3 encountered issues.")
    
    # Final Summary
    logger.info("\n" + "="*70)
    logger.info("PIPELINE EXECUTION SUMMARY")
    logger.info("="*70)
    logger.info(f"Phase 1 (Selenium):    {'✓ SUCCESS' if phase1_success else '✗ FAILED'}")
    logger.info(f"Phase 2 (Scrapy):      {'✓ SUCCESS' if phase2_success else '⚠ PARTIAL'}")
    logger.info(f"Phase 3 (Analysis):    {'✓ SUCCESS' if phase3_success else '⚠ PARTIAL'}")
    logger.info("="*70 + "\n")
    
    # Check final output files
    logger.info("OUTPUT FILES:")
    output_files = [
        ("Job Links", "data/raw/job_links.csv"),
        ("Job Data", "data/final/jobs.csv"),
        ("Analysis Report", "analysis/reports/analysis_report.txt"),
    ]
    
    for name, path in output_files:
        if Path(path).exists():
            size = Path(path).stat().st_size
            logger.info(f"  ✓ {name}: {path} ({size:,} bytes)")
        else:
            logger.info(f"  ○ {name}: {path} (not found)")
    
    logger.info("\n" + "="*70)
    if phase1_success and phase2_success and phase3_success:
        logger.info("✓ PIPELINE COMPLETED SUCCESSFULLY")
    else:
        logger.warning("⚠ PIPELINE COMPLETED WITH ISSUES")
    logger.info("="*70 + "\n")


if __name__ == "__main__":
    main()
