"""
This python script provides a simple way to check a website for broken links and report them to a .csv file.
Release: v1.0-beta1

---Dependencies---
Scrapy (https://scrapy.org)
v1.0-beta: Unix environment

---Implementation---
) Create target directory & cd to empty directory. NOTE: Target directory MUST be empty!
) Paste code into text editor
) Provide parameters
    - target_urls
    - start_urls
    - handle_httpstatus_list
) Save as main.py
) Open a terminal
) Set up and activate a python virtual environment
) Install scrapy with: $ pip install scrapy
) Run the crawler with: $ scrapy runspider script.py -o <insert_report_name.csv>
"""

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field


# Headings for each column
class MyItems(Item):
    Referer = Field()
    Response = Field()
    Status = Field()


#
class Spider(CrawlSpider):
    name = "Broken Link Crawler"
    target_domains = ["corescientific.com"]  # restrict crawling to this domain
    start_urls = ["https://corescientific.com"]  # start crawling here
    handle_httpstatus_list = [400, 403, 404, 408, 410, 500, 502, 504, 511]  # specify error codes reported
    # Throttle http requests to prevent response 429
    custom_settings = {
        'CONCURRENT_REQUESTS': 25,
        'DOWNLOAD_DELAY': 0.25,  # delay between requests in seconds
        'REDIRECT_ENABLED': True
    }

    rules = [
        Rule(  # Extract all unique links and follow them
            LinkExtractor(allow_domains=target_domains, unique='Yes'),
            callback='parse_my_url',
            follow=True),
        Rule(  # Extract all unique external links but don't follow them
            LinkExtractor(allow='', unique='Yes'),
            callback='parse_my_url',
            follow=False
        )
    ]

    # method that yields a tuple containing the referer,
    def parse_my_url(self, response):
        report = [400, 403, 404, 408, 410, 500, 502, 504, 511]  # should match handle_httpstatus_list
        if response.status in report:  # if the response matches then creates a MyItems
            item = MyItems()
            item['Referer'] = response.request.headers.get('Referer')
            item['Response'] = response.url
            item['Status'] = response.status
            yield item
        yield None  # if the response did not match return empty
