"""
This python script provides a simple way to check a website for broken links and report them to a .csv file.
Release: v1.0-beta1

-------------------------------------Dependencies---------------------------------------
Scrapy (https://scrapy.org)
v1.0-beta: Unix environment

-------------------------------------Implementation-------------------------------------
1) Create target directory & cd to empty directory. NOTE: Target directory MUST be empty!
2) Paste code into text editor
3) Provide parameters
    - target_urls
    - start_urls
    - handle_httpstatus_list
    - report
4) Save as main.py
5) Open a terminal
6) Set up and activate a python virtual environment. Refer to environmentsetup.txt
7) Install scrapy with: $ pip install scrapy
8) Run the crawler with: $ scrapy runspider script.py -o <insert_report_name.csv>

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
    target_domains = ["<insert domain here>"]  # restrict crawling to this domain
    start_urls = ["<insert starting URL here"]  # start crawling here
    handle_httpstatus_list = [<insert list of error codes as ints separated by commas>]  # specify error codes reported
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

    # method that yields a tuple containing the referer's header, the response the http request, and the status of the requested link
    def parse_my_url(self, response):
        report = [insert error/response codes separated by a comma]  # should match handle_httpstatus_list
        if response.status in report:  # if the response matches then creates a MyItems
            item = MyItems()
            item['Referer'] = response.request.headers.get('Referer')
            item['Response'] = response.url
            item['Status'] = response.status
            yield item
        yield None  # if the response did not match yield nothing
