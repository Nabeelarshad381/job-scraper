"""
Data Analysis and Reporting Script for Job Scraping Results.

Author: Senior Data Engineer
Course: Tools & Techniques for DS - University of Central Punjab
Date: March 2026

This script analyzes the scraped job data to provide insights on:
- Top skills required
- Top job locations
- Top hiring companies
- Count of entry-level/intern roles
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from pathlib import Path
from collections import Counter
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JobDataAnalyzer:
    """Analyze job scraping data and generate insights."""
    
    def __init__(self, csv_path='../data/final/jobs.csv', output_dir='./reports'):
        """
        Initialize analyzer with data path.
        
        Args:
            csv_path (str): Path to jobs CSV file
            output_dir (str): Directory to save reports
        """
        self.csv_path = csv_path
        self.output_dir = output_dir
        self.df = None
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def load_data(self):
        """Load and validate job data from CSV."""
        try:
            logger.info(f"Loading data from {self.csv_path}...")
            self.df = pd.read_csv(self.csv_path)
            
            logger.info(f"Loaded {len(self.df)} job records")
            logger.info(f"Columns: {list(self.df.columns)}")
            
            return True
        
        except FileNotFoundError:
            logger.error(f"CSV file not found: {self.csv_path}")
            return False
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False
    
    def clean_data(self):
        """Clean and preprocess data."""
        try:
            logger.info("Cleaning data...")
            
            # Remove duplicates
            self.df = self.df.drop_duplicates(subset=['job_url'])
            logger.info(f"Removed duplicates. {len(self.df)} records remaining")
            
            # Fill missing values
            self.df['location'].fillna('Not specified', inplace=True)
            self.df['department'].fillna('General', inplace=True)
            self.df['employment_type'].fillna('Full-time', inplace=True)
            self.df['required_skills'].fillna('', inplace=True)
            
            logger.info("Data cleaning completed")
            
        except Exception as e:
            logger.error(f"Error cleaning data: {e}")
    
    def analyze_top_skills(self, top_n=15):
        """
        Analyze and visualize top required skills.
        
        Args:
            top_n (int): Number of top skills to display
            
        Returns:
            pd.Series: Top skills with counts
        """
        try:
            logger.info(f"Analyzing top {top_n} required skills...")
            
            # Parse skills (assuming pipe-separated format)
            all_skills = []
            
            for skills_str in self.df['required_skills'].dropna():
                if isinstance(skills_str, str) and skills_str.strip():
                    skills = [s.strip() for s in skills_str.split('|')]
                    all_skills.extend(skills)
            
            # Count skill frequencies
            skill_counts = Counter(all_skills)
            top_skills = pd.Series(dict(skill_counts.most_common(top_n)))
            
            logger.info(f"Found {len(skill_counts)} unique skills")
            logger.info(f"Top {top_n} skills:")
            for skill, count in top_skills.items():
                logger.info(f"  {skill}: {count}")
            
            # Visualize
            plt.figure(figsize=(12, 6))
            top_skills.plot(kind='barh', color='steelblue')
            plt.title(f'Top {top_n} Required Skills', fontsize=14, fontweight='bold')
            plt.xlabel('Frequency')
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'top_skills.png'), dpi=300)
            logger.info("Saved: top_skills.png")
            plt.close()
            
            return top_skills
        
        except Exception as e:
            logger.error(f"Error analyzing skills: {e}")
            return pd.Series()
    
    def analyze_top_locations(self, top_n=10):
        """
        Analyze and visualize top job locations.
        
        Args:
            top_n (int): Number of top locations to display
            
        Returns:
            pd.Series: Top locations with counts
        """
        try:
            logger.info(f"Analyzing top {top_n} locations...")
            
            # Extract location type tags
            location_counts = self.df['location'].value_counts().head(top_n)
            
            logger.info(f"Top {top_n} locations:")
            for location, count in location_counts.items():
                logger.info(f"  {location}: {count}")
            
            # Count remote/hybrid/on-site
            location_types = self.df['location'].apply(self._extract_location_type)
            type_counts = location_types.value_counts()
            
            # Visualize locations
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            
            # Top locations
            location_counts.plot(kind='bar', ax=axes[0], color='coral')
            axes[0].set_title(f'Top {top_n} Job Locations', fontweight='bold')
            axes[0].set_xlabel('')
            axes[0].set_ylabel('Count')
            axes[0].tick_params(axis='x', rotation=45)
            
            # Location type distribution
            type_counts.plot(kind='pie', ax=axes[1], autopct='%1.1f%%',
                            colors=['#ff9999', '#66b3ff', '#99ff99'])
            axes[1].set_title('Work Environment Distribution', fontweight='bold')
            axes[1].set_ylabel('')
            
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'top_locations.png'), dpi=300)
            logger.info("Saved: top_locations.png")
            plt.close()
            
            return location_counts
        
        except Exception as e:
            logger.error(f"Error analyzing locations: {e}")
            return pd.Series()
    
    def analyze_top_companies(self, top_n=10):
        """
        Analyze and visualize top hiring companies.
        
        Args:
            top_n (int): Number of top companies to display
            
        Returns:
            pd.Series: Top companies with counts
        """
        try:
            logger.info(f"Analyzing top {top_n} hiring companies...")
            
            company_counts = self.df['company_name'].value_counts().head(top_n)
            
            logger.info(f"Top {top_n} companies:")
            for company, count in company_counts.items():
                logger.info(f"  {company}: {count} positions")
            
            # Visualize
            plt.figure(figsize=(12, 6))
            company_counts.plot(kind='barh', color='mediumseagreen')
            plt.title(f'Top {top_n} Hiring Companies', fontsize=14, fontweight='bold')
            plt.xlabel('Number of Open Positions')
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'top_companies.png'), dpi=300)
            logger.info("Saved: top_companies.png")
            plt.close()
            
            return company_counts
        
        except Exception as e:
            logger.error(f"Error analyzing companies: {e}")
            return pd.Series()
    
    def analyze_entry_level_roles(self):
        """
        Analyze and visualize entry-level and intern roles.
        
        Returns:
            dict: Statistics on entry-level roles
        """
        try:
            logger.info("Analyzing entry-level and intern roles...")
            
            # Define entry-level keywords
            entry_level_keywords = ['intern', 'junior', 'entry-level', 'graduate', 'trainee']
            
            # Filter entry-level roles
            entry_level_mask = self.df['job_title'].str.lower().str.contains(
                '|'.join(entry_level_keywords), na=False
            )
            entry_level_df = self.df[entry_level_mask]
            
            # Filter intern roles
            intern_mask = self.df['employment_type'].str.lower().str.contains(
                'intern', na=False
            )
            intern_df = self.df[intern_mask]
            
            # Statistics
            stats = {
                'total_jobs': len(self.df),
                'entry_level_count': len(entry_level_df),
                'intern_count': len(intern_df),
                'entry_level_percentage': (len(entry_level_df) / len(self.df) * 100),
                'intern_percentage': (len(intern_df) / len(self.df) * 100),
            }
            
            logger.info("Entry-level Role Statistics:")
            logger.info(f"  Total jobs: {stats['total_jobs']}")
            logger.info(f"  Entry-level roles: {stats['entry_level_count']} ({stats['entry_level_percentage']:.1f}%)")
            logger.info(f"  Intern positions: {stats['intern_count']} ({stats['intern_percentage']:.1f}%)")
            
            # Visualize
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            
            # Pie chart
            labels = ['Other Roles', 'Entry-Level Roles']
            sizes = [
                stats['total_jobs'] - stats['entry_level_count'],
                stats['entry_level_count']
            ]
            colors = ['#ff9999', '#66b3ff']
            
            axes[0].pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
            axes[0].set_title('Entry-Level vs Other Roles', fontweight='bold')
            
            # Bar chart
            categories = ['Entry-Level', 'Intern']
            counts = [stats['entry_level_count'], stats['intern_count']]
            axes[1].bar(categories, counts, color=['#99ff99', '#ffcc99'])
            axes[1].set_title('Entry-Level and Intern Positions', fontweight='bold')
            axes[1].set_ylabel('Count')
            
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'entry_level_analysis.png'), dpi=300)
            logger.info("Saved: entry_level_analysis.png")
            plt.close()
            
            return stats
        
        except Exception as e:
            logger.error(f"Error analyzing entry-level roles: {e}")
            return {}
    
    def generate_summary_report(self):
        """Generate a comprehensive text summary report."""
        try:
            logger.info("Generating summary report...")
            
            report = f"""
{'='*70}
JOB SCRAPING ANALYSIS REPORT
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}

DATASET OVERVIEW:
- Total jobs extracted: {len(self.df)}
- Date range: {self.df['posted_date'].min()} to {self.df['posted_date'].max()}
- Unique companies: {self.df['company_name'].nunique()}
- Unique locations: {self.df['location'].nunique()}

EMPLOYMENT TYPE BREAKDOWN:
{self.df['employment_type'].value_counts().to_string()}

DEPARTMENT BREAKDOWN:
{self.df['department'].value_counts().head(10).to_string()}

TOP 10 LOCATIONS:
{self.df['location'].value_counts().head(10).to_string()}

TOP 10 COMPANIES:
{self.df['company_name'].value_counts().head(10).to_string()}

DATA QUALITY METRICS:
- Complete job titles: {self.df['job_title'].notna().sum()} / {len(self.df)}
- Complete descriptions: {self.df['job_description'].notna().sum()} / {len(self.df)}
- Jobs with skills: {(self.df['required_skills'].str.len() > 0).sum()} / {len(self.df)}

{'='*70}
Report generated successfully. Check reports/ directory for visualizations.
{'='*70}
"""
            
            print(report)
            
            # Save report to file
            report_path = os.path.join(self.output_dir, 'analysis_report.txt')
            with open(report_path, 'w') as f:
                f.write(report)
            logger.info(f"Saved: {report_path}")
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
    
    def _extract_location_type(self, location_str):
        """Extract location type tag from location string."""
        location_str = str(location_str).upper()
        
        if '[REMOTE]' in location_str:
            return 'Remote'
        elif '[HYBRID]' in location_str:
            return 'Hybrid'
        else:
            return 'On-site'
    
    def run_full_analysis(self):
        """Execute complete analysis pipeline."""
        try:
            if not self.load_data():
                return False
            
            self.clean_data()
            
            # Run all analyses
            self.analyze_top_skills(top_n=15)
            self.analyze_top_locations(top_n=10)
            self.analyze_top_companies(top_n=10)
            self.analyze_entry_level_roles()
            
            self.generate_summary_report()
            
            logger.info("="*70)
            logger.info("Analysis completed successfully!")
            logger.info(f"Reports saved to: {self.output_dir}")
            logger.info("="*70)
            
            return True
        
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return False


def main():
    """Main entry point for analysis script."""
    analyzer = JobDataAnalyzer(
        csv_path='../data/final/jobs.csv',
        output_dir='./reports'
    )
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main()
