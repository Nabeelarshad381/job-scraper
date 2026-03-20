"""
Scrapy Pipeline for data cleaning and export.
"""

import csv
import logging
from datetime import datetime
from itemadapter import ItemAdapter
import os


class AshbyPipeline:
    """
    Data cleaning and processing pipeline.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def process_item(self, item, spider):
        """
        Process and clean each item.
        
        Args:
            item: Scrapy item to process
            spider: The spider instance
            
        Returns:
            Processed item
        """
        adapter = ItemAdapter(item)
        
        # Clean whitespace from all fields
        for field_name in adapter.field_names():
            if isinstance(adapter.get(field_name), str):
                adapter[field_name] = adapter.get(field_name).strip()
        
        # Ensure skills is a list
        if adapter.get('required_skills'):
            if isinstance(adapter['required_skills'], str):
                # Convert comma-separated string to list
                adapter['required_skills'] = [
                    skill.strip() 
                    for skill in adapter['required_skills'].split(',')
                ]
        else:
            adapter['required_skills'] = []
        
        # Add extraction timestamp if not present
        if not adapter.get('extracted_timestamp'):
            adapter['extracted_timestamp'] = datetime.now().isoformat()
        
        self.logger.debug(f"Processed item: {adapter.get('job_title')}")
        return item


class CSVExportPipeline:
    """
    Export items to CSV file with all required fields.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.file = None
        self.writer = None
        self.output_path = '../data/final/jobs.csv'
        
        # Define field order
        self.fields = [
            'job_title',
            'company_name',
            'location',
            'department',
            'employment_type',
            'posted_date',
            'job_url',
            'job_description',
            'required_skills',
            'extracted_timestamp'
        ]
    
    def open_spider(self, spider):
        """
        Initialize CSV file when spider opens.
        
        Args:
            spider: The spider instance
        """
        try:
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            
            self.file = open(self.output_path, 'w', newline='', encoding='utf-8')
            self.writer = csv.DictWriter(self.file, fieldnames=self.fields)
            self.writer.writeheader()
            
            self.logger.info(f"Opened CSV file for export: {self.output_path}")
        except Exception as e:
            self.logger.error(f"Error opening CSV file: {e}")
            raise
    
    def close_spider(self, spider):
        """
        Close CSV file when spider closes.
        
        Args:
            spider: The spider instance
        """
        if self.file:
            self.file.close()
            self.logger.info(f"Closed CSV file: {self.output_path}")
    
    def process_item(self, item, spider):
        """
        Write item to CSV file.
        
        Args:
            item: Scrapy item to write
            spider: The spider instance
            
        Returns:
            Item (unchanged)
        """
        try:
            adapter = ItemAdapter(item)
            row = {}
            
            for field in self.fields:
                value = adapter.get(field, '')
                
                # Convert skills list to string
                if field == 'required_skills' and isinstance(value, list):
                    value = '|'.join(value)  # Using pipe as delimiter
                
                row[field] = value
            
            self.writer.writerow(row)
            self.logger.debug(f"Wrote job: {adapter.get('job_title')}")
            
        except Exception as e:
            self.logger.error(f"Error writing item to CSV: {e}")
        
        return item
