"""
Scrapy Item definitions for Ashby job extraction.
"""

import scrapy


class JobItem(scrapy.Item):
    """
    Item class for extracted job data.
    
    Fields:
        - job_title: Title of the position
        - company_name: Hiring company name
        - location: Job location (with remote/hybrid tag)
        - department: Department/Team
        - employment_type: Full-time, Part-time, Contract, Intern, etc.
        - posted_date: Publication date
        - job_url: Link to job posting
        - job_description: Full job description text
        - required_skills: List of required skills
        - extracted_timestamp: When the job was extracted
    """
    
    job_title = scrapy.Field()
    company_name = scrapy.Field()
    location = scrapy.Field()
    department = scrapy.Field()
    employment_type = scrapy.Field()
    posted_date = scrapy.Field()
    job_url = scrapy.Field()
    job_description = scrapy.Field()
    required_skills = scrapy.Field()
    extracted_timestamp = scrapy.Field()
