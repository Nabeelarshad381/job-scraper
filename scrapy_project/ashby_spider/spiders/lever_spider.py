import scrapy
from scrapy import signals
from scrapy.exceptions import DropItem
import csv
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class LeverSpider(scrapy.Spider):
    """
    Lever Job Spider - Match Group
    Targets: All tech roles
    Source: https://jobs.lever.co/matchgroup
    """

    name = 'lever_spider'
    allowed_domains = ['jobs.lever.co']
    start_urls = ['https://jobs.lever.co/matchgroup']

    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 1,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 10,
        'RETRY_TIMES': 3,
        'ITEM_PIPELINES': {
            'ashby_spider.pipelines.AshbyPipeline': 300,
            'ashby_spider.pipelines.CSVExportPipeline': 400,
        }
    }

    def __init__(self, *args, **kwargs):
        super(LeverSpider, self).__init__(*args, **kwargs)
        self.job_links = []
        self.target_roles = ['Data Scientist', 'Software Engineer']

    @classmethod
    def from_crawler(cls, crawler):
        spider = super(LeverSpider, cls).from_crawler(crawler)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def parse(self, response):
        """Parse job listing page"""
        logger.info(f"Parsing Lever page: {response.url}")

        # Extract job listings - Lever uses div.posting
        job_listings = response.css('div.posting')
        logger.info(f"Found {len(job_listings)} job postings on listing page")

        if not job_listings:
            # Fallback: try extracting all job links by href pattern
            logger.warning("No div.posting found, trying fallback link extraction")
            all_links = response.css('a[href*="/matchgroup/"]')
            for link in all_links:
                job_url = link.attrib.get('href', '')
                if job_url and '/matchgroup/' in job_url and job_url not in [jl.get('job_url') for jl in self.job_links]:
                    job_title = link.css('::text').get('').strip()
                    yield scrapy.Request(
                        url=response.urljoin(job_url),
                        callback=self.parse_job_detail,
                        meta={
                            'job_title': job_title or 'Unknown',
                            'department': 'General',
                            'location': '',
                            'source': 'lever_matchgroup'
                        }
                    )
            return

        for job_listing in job_listings:
            # Lever has various selector patterns
            job_title = (
                job_listing.css('h5 a::text').get('').strip() or
                job_listing.css('.posting-title a::text').get('').strip() or
                job_listing.css('a::text').get('').strip()
            )
            department = (
                job_listing.css('span.department::text').get('').strip() or
                job_listing.css('span.posting-category::text').get('').strip() or
                'General'
            )
            location = (
                job_listing.css('span.location::text').get('').strip() or
                job_listing.css('.posting-categories .sort-by-location::text').get('').strip() or
                ''
            )
            job_url = (
                job_listing.css('a.posting-title::attr(href)').get() or
                job_listing.css('h5 a::attr(href)').get() or
                job_listing.css('a::attr(href)').get()
            )

            if job_url:
                job_url = response.urljoin(job_url)
                self.job_links.append({
                    'job_url': job_url,
                    'job_title': job_title,
                    'department': department,
                    'source': 'lever_matchgroup',
                    'extracted_timestamp': datetime.now().isoformat()
                })

                logger.info(f"✓ Extracted: {job_title}")

                yield scrapy.Request(
                    url=job_url,
                    callback=self.parse_job_detail,
                    meta={
                        'job_title': job_title,
                        'department': department,
                        'location': location,
                        'source': 'lever_matchgroup'
                    }
                )

    def parse_job_detail(self, response):
        """Parse individual job detail page"""
        job_title = response.meta.get('job_title', '')
        department = response.meta.get('department', '')
        location = response.meta.get('location', '')
        source = response.meta.get('source', '')

        # Extract fields from Lever platform
        description_parts = response.css('div.content-wrapper .section-wrapper .content li::text').getall()
        if not description_parts:
            description_parts = response.css('div.content-wrapper ::text').getall()
        job_description = ' '.join([p.strip() for p in description_parts if p.strip()])
        company_name = 'Match Group'

        # Extract employment type
        employment_type = self._extract_employment_type(job_description)

        # Extract posted date
        posted_date_text = response.css('span.posted-date::text').get('')
        posted_date = self._parse_date(posted_date_text)

        # Extract skills
        required_skills = self._extract_skills(job_description)

        # Location tagging
        location_type = self._tag_location_type(location)
        location_with_tag = f"{location} [{location_type}]" if location else f"Unknown [{location_type}]"

        item = {
            'job_title': job_title,
            'company_name': company_name,
            'location': location_with_tag,
            'department': department,
            'employment_type': employment_type,
            'posted_date': posted_date,
            'job_url': response.url,
            'job_description': job_description[:500],  # First 500 chars
            'required_skills': required_skills,
            'source': source
        }

        logger.info(f"✓ Parsed: {job_title} at {company_name}")
        yield item

    def _is_target_role(self, job_title, department):
        """Check if job matches target roles"""
        combined = f"{job_title} {department}".lower()
        return any(role.lower() in combined for role in self.target_roles)

    def _extract_employment_type(self, text):
        """Extract employment type from job description"""
        text_lower = text.lower()
        if 'full-time' in text_lower or 'full time' in text_lower:
            return 'Full-time'
        elif 'part-time' in text_lower or 'part time' in text_lower:
            return 'Part-time'
        elif 'contract' in text_lower:
            return 'Contract'
        elif 'internship' in text_lower or 'intern' in text_lower:
            return 'Internship'
        elif 'temporary' in text_lower or 'temp' in text_lower:
            return 'Temporary'
        return 'Full-time'

    def _tag_location_type(self, location):
        """Tag location as REMOTE, HYBRID, or ON-SITE"""
        location_lower = location.lower() if location else ''

        if 'remote' in location_lower:
            return 'REMOTE'
        elif 'hybrid' in location_lower:
            return 'HYBRID'
        else:
            return 'ON-SITE'

    def _parse_date(self, date_text):
        """Parse date string"""
        if not date_text:
            return datetime.now().strftime('%Y-%m-%d')
        return date_text.strip()

    def _extract_skills(self, text):
        """Extract required skills from job description"""
        common_skills = [
            'Python', 'R', 'SQL', 'Java', 'C++', 'JavaScript', 'Scala',
            'Spark', 'Hadoop', 'TensorFlow', 'PyTorch', 'Keras',
            'Pandas', 'NumPy', 'Scikit-learn', 'Matplotlib', 'Seaborn',
            'AWS', 'Google Cloud', 'Azure', 'Docker', 'Kubernetes',
            'Git', 'Jenkins', 'Linux', 'Tableau', 'Power BI',
            'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision',
            'Statistics', 'Linear Algebra', 'Data Mining', 'A/B Testing',
            'Experiment Design', 'Big Data'
        ]

        found_skills = []
        for skill in common_skills:
            if skill.lower() in text.lower():
                found_skills.append(skill)

        return ', '.join(found_skills) if found_skills else 'General'

    def spider_closed(self, reason):
        """Save extracted links when spider closes"""
        logger.info(f"Spider closed: {reason}")
        logger.info(f"Total jobs extracted: {len(self.job_links)}")

        # Save to CSV
        if self.job_links:
            import os as _os
            base_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
            filename = _os.path.join(base_dir, 'data', 'raw', 'job_links_lever.csv')
            _os.makedirs(_os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['job_url', 'job_title', 'department', 'source', 'extracted_timestamp']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.job_links)
            logger.info(f"✓ Saved {len(self.job_links)} job links to {filename}")
