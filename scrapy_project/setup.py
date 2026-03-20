"""
Setup script for Scrapy project.
"""

from setuptools import setup, find_packages

setup(
    name='ashby-job-spider',
    version='1.0.0',
    description='Ashby HQ Job Portal Web Scraper',
    author='Senior Data Engineer',
    author_email='ds@university.edu',
    packages=find_packages(),
    install_requires=[
        'scrapy>=2.9.0',
        'pandas>=2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'ashby-spider=ashby_spider.spiders.ashby_spider:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
)
