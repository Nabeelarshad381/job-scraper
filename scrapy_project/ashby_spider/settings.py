"""
Scrapy settings for ashby_spider project.
"""

BOT_NAME = 'ashby_spider'

SPIDER_MODULES = ['ashby_spider.spiders']
NEWSPIDER_MODULE = 'ashby_spider.spiders'

# Crawl responsibly by identifying yourself
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 1

# Polite delay between requests (2 seconds as per requirements)
DOWNLOAD_DELAY = 2

# Configure pipelines
ITEM_PIPELINES = {
    'ashby_spider.pipelines.AshbyPipeline': 300,
    'ashby_spider.pipelines.CSVExportPipeline': 400,
}

# Logging configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'

# Retry configuration
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408]

# Timeout configuration
DOWNLOAD_TIMEOUT = 30

# Disable cookies to avoid state persistence
COOKIES_ENABLED = False

# Enable AutoThrottle extension
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False
