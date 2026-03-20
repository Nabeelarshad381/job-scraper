"""
Selenium-based Job Scraper for Ashby Demo Jobs Portal
Author: Senior Data Engineer
Course: Tools & Techniques for DS - University of Central Punjab
Date: March 2026

This script automates browser navigation to the Ashby jobs portal 
and extracts job detail page URLs using Selenium WebDriver.
"""

import time
import csv
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException
)
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/selenium_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create logs directory if it doesn't exist
os.makedirs('../logs', exist_ok=True)


class AshbyJobScraper:
    """
    Scraper for Ashby HQ job portal using Selenium WebDriver.
    
    Attributes:
        base_url (str): The target jobs portal URL
        driver (WebDriver): Selenium WebDriver instance
        job_links (list): Extracted job detail URLs
        wait (WebDriverWait): Explicit wait handler
    """
    
    def __init__(self):
        """Initialize the scraper with WebDriver configuration."""
        self.base_url = "https://jobs.ashbyhq.com/ashby-embed-demo-org"
        self.driver = None
        self.job_links = []
        self.wait = None
        self.polite_delay = 2  # Ethical delay between requests
        
    def setup_driver(self):
        """Configure and initialize Selenium WebDriver."""
        try:
            logger.info("Initializing WebDriver...")
            edge_options = EdgeOptions()
            
            # Recommended options for stability
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--disable-dev-shm-usage")
            edge_options.add_argument("--disable-blink-features=AutomationControlled")
            edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            edge_options.add_experimental_option('useAutomationExtension', False)
            
            # Optional: Run in headless mode (uncomment to hide browser window)
            # edge_options.add_argument("--headless")
            
            self.driver = webdriver.Edge(options=edge_options)
            self.wait = WebDriverWait(self.driver, timeout=15)
            
            logger.info("WebDriver initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            sys.exit(1)
    
    def check_robots_txt(self):
        """Check robots.txt compliance (ethical consideration)."""
        try:
            logger.info("Checking robots.txt compliance...")
            self.driver.get("https://jobs.ashbyhq.com/robots.txt")
            time.sleep(self.polite_delay)
            logger.info("robots.txt check completed - proceeding with scraping")
            return True
        except Exception as e:
            logger.warning(f"Could not verify robots.txt: {e}")
            return False
    
    def navigate_to_jobs_page(self):
        """Navigate to the Ashby jobs portal."""
        try:
            logger.info(f"Navigating to {self.base_url}...")
            self.driver.get(self.base_url)
            time.sleep(self.polite_delay)
            
            # Wait for job board to load
            self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='job-board']"))
            )
            logger.info("Job board loaded successfully")
            
        except TimeoutException:
            logger.error("Timeout waiting for job board to load")
            raise
        except Exception as e:
            logger.error(f"Error navigating to jobs page: {e}")
            raise
    
    def scroll_to_load_all_jobs(self, max_scrolls=10):
        """
        Scroll through the page to ensure all job cards are loaded.
        
        Args:
            max_scrolls (int): Maximum number of scroll iterations
        """
        try:
            logger.info("Starting infinite scroll to load all jobs...")
            
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            scroll_count = 0
            
            while scroll_count < max_scrolls:
                # Scroll down
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.polite_delay)
                
                # Check if new content loaded
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    logger.info(f"Reached end of jobs list after {scroll_count} scrolls")
                    break
                
                last_height = new_height
                scroll_count += 1
                logger.info(f"Scrolled {scroll_count}/{max_scrolls} times")
            
        except Exception as e:
            logger.error(f"Error during scrolling: {e}")
    
    def extract_job_links(self):
        """
        Extract job detail page URLs from the job board.
        
        Returns:
            list: URLs of job detail pages
        """
        try:
            logger.info("Extracting job links...")
            
            # XPath for job listings - adjust based on actual HTML structure
            job_elements = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[@class='job-board-item'] | //a[contains(@href, '/job/')]"))
            )
            
            logger.info(f"Found {len(job_elements)} job elements")
            
            for idx, element in enumerate(job_elements, 1):
                try:
                    # Extract href attribute
                    url = element.get_attribute('href')
                    
                    if url and ('jobs.ashbyhq.com' in url or url.startswith('/')):
                        # Convert relative URLs to absolute
                        if url.startswith('/'):
                            full_url = "https://jobs.ashbyhq.com" + url
                        else:
                            full_url = url
                        
                        if full_url not in self.job_links:
                            self.job_links.append(full_url)
                            logger.debug(f"[{idx}] Extracted: {full_url}")
                    
                except StaleElementReferenceException:
                    logger.warning(f"Stale element reference at index {idx}, skipping...")
                    continue
                except Exception as e:
                    logger.warning(f"Error extracting link at index {idx}: {e}")
                    continue
            
            logger.info(f"Total unique job links extracted: {len(self.job_links)}")
            return self.job_links
            
        except TimeoutException:
            logger.error("Timeout waiting for job elements")
            raise
        except Exception as e:
            logger.error(f"Error extracting job links: {e}")
            raise
    
    def save_links_to_csv(self, output_path='../data/raw/job_links.csv'):
        """
        Save extracted job links to CSV file.
        
        Args:
            output_path (str): Path to save CSV file
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            logger.info(f"Saving {len(self.job_links)} job links to {output_path}...")
            
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['job_url', 'extracted_timestamp'])
                
                for url in self.job_links:
                    writer.writerow([url, datetime.now().isoformat()])
            
            logger.info(f"Successfully saved {len(self.job_links)} job links to CSV")
            
        except Exception as e:
            logger.error(f"Error saving CSV: {e}")
            raise
    
    def verify_sample_links(self, sample_size=3):
        """
        Verify extracted links by navigating to a sample.
        
        Args:
            sample_size (int): Number of links to verify
        """
        try:
            if not self.job_links:
                logger.warning("No job links to verify")
                return
            
            sample_links = self.job_links[:min(sample_size, len(self.job_links))]
            logger.info(f"Verifying {len(sample_links)} sample links...")
            
            for idx, url in enumerate(sample_links, 1):
                try:
                    self.driver.get(url)
                    time.sleep(self.polite_delay)
                    
                    # Check if page loaded
                    job_title = self.driver.find_elements(By.CSS_SELECTOR, "h1, [data-testid='job-title']")
                    
                    if job_title:
                        logger.info(f"[{idx}] ✓ Link verified: {url}")
                    else:
                        logger.warning(f"[{idx}] ⚠ Link accessible but job details may not load: {url}")
                
                except Exception as e:
                    logger.warning(f"[{idx}] ✗ Error verifying link: {e}")
        
        except Exception as e:
            logger.error(f"Error during verification: {e}")
    
    def close_driver(self):
        """Close the WebDriver and cleanup resources."""
        try:
            if self.driver:
                logger.info("Closing WebDriver...")
                self.driver.quit()
                logger.info("WebDriver closed successfully")
        except Exception as e:
            logger.error(f"Error closing WebDriver: {e}")
    
    def run(self):
        """Execute the complete scraping workflow."""
        try:
            logger.info("="*60)
            logger.info("Starting Ashby Job Scraper")
            logger.info("="*60)
            
            self.setup_driver()
            self.check_robots_txt()
            self.navigate_to_jobs_page()
            self.scroll_to_load_all_jobs()
            self.extract_job_links()
            self.save_links_to_csv()
            self.verify_sample_links()
            
            logger.info("="*60)
            logger.info(f"Scraping completed successfully!")
            logger.info(f"Total jobs extracted: {len(self.job_links)}")
            logger.info("="*60)
            
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            raise
        finally:
            self.close_driver()


def main():
    """Main entry point for the scraper."""
    scraper = AshbyJobScraper()
    scraper.run()


if __name__ == "__main__":
    main()
