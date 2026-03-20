import scrapy
from scrapy import signals
from scrapy.exceptions import DropItem
import csv
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class GreenhouseSpider(scrapy.Spider):
    """
    Greenhouse Job Spider - BeviCareers
    Targets: Data Scientists, ML Engineers
    Source: https://boards.greenhouse.io/bevicareers
    """

    name = 'greenhouse_spider'
    allowed_domains = ['boards-api.greenhouse.io']
    # Use Greenhouse Job Board API instead of dynamic HTML rendering.
    start_urls = ['https://boards-api.greenhouse.io/v1/boards/bevicareers/jobs']

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
        super(GreenhouseSpider, self).__init__(*args, **kwargs)
        self.job_links = []
        self.target_roles = ['Data Scientist', 'Software Engineer']

    @classmethod
    def from_crawler(cls, crawler):
        spider = super(GreenhouseSpider, cls).from_crawler(crawler)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def parse(self, response):
        """Parse Greenhouse jobs list JSON."""
        logger.info(f"Fetching Greenhouse jobs list: {response.url}")

        payload = response.json()
        jobs = payload.get('jobs', []) or []

        for job in jobs:
            job_title = job.get('title', '') or ''
            job_id = job.get('id')
            if not job_id:
                continue

            job_detail_url = f'https://boards-api.greenhouse.io/v1/boards/bevicareers/jobs/{job_id}'
            yield scrapy.Request(
                url=job_detail_url,
                callback=self.parse_job_detail,
            )

    def parse_job_detail(self, response):
        """Parse individual job detail JSON from Greenhouse."""
        data = response.json()

        job_title = data.get('title', '') or ''
        company_name = data.get('company_name', '') or 'BeviCareers'
        source = 'greenhouse_bevicareers'

        location_name = (data.get('location', {}) or {}).get('name', '') or ''
        departments = data.get('departments', []) or []
        department = departments[0].get('name', '') if departments else 'General'

        # Content is HTML-escaped; decode and strip tags.
        content_html = data.get('content', '') or ''
        # Avoid importing heavy dependencies; stripping tags is sufficient for keyword scans.
        import html as _html
        import re as _re
        decoded_html = _html.unescape(content_html)
        job_description_text = _re.sub(r'<[^>]+>', ' ', decoded_html)
        job_description_text = _re.sub(r'\s+', ' ', job_description_text).strip()

        employment_type = self._extract_employment_type(job_description_text)
        required_skills = self._extract_skills(job_description_text)

        posted_date = (data.get('first_published') or '').strip()

        location_type = self._tag_location_type(location_name)
        location_with_tag = f"{location_name} [{location_type}]" if location_name else f"Unknown [{location_type}]"

        item = {
            'job_title': job_title,
            'company_name': company_name,
            'location': location_with_tag,
            'department': department,
            'employment_type': employment_type,
            'posted_date': posted_date,
            'job_url': data.get('absolute_url') or response.url,
            'job_description': job_description_text[:500],
            'required_skills': required_skills,
            'source': source,
        }

        self.job_links.append({
            'job_url': item['job_url'],
            'job_title': job_title,
            'department': department,
            'source': source,
            'extracted_timestamp': datetime.now().isoformat(),
        })

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

    def _extract_skills(self, text):
        """Extract required skills from job description"""
        common_skills = [
            'Python', 'R', 'SQL', 'Java', 'C++', 'JavaScript', 'Scala',
            'Spark', 'Hadoop', 'TensorFlow', 'PyTorch', 'Keras',
            'Pandas', 'NumPy', 'Scikit-learn', 'Matplotlib', 'Seaborn',
            'AWS', 'Google Cloud', 'Azure', 'Docker', 'Kubernetes',
            'Git', 'Jenkins', 'Linux', 'Tableau', 'Power BI',
            'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision',
            'Statistics', 'Linear Algebra', 'Data Mining', 'A/B Testing'
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
            filename = _os.path.join(base_dir, 'data', 'raw', 'job_links_greenhouse.csv')
            _os.makedirs(_os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['job_url', 'job_title', 'department', 'source', 'extracted_timestamp']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.job_links)
            logger.info(f"✓ Saved {len(self.job_links)} job links to {filename}")
