
import scrapy
from scrapy_selenium import SeleniumRequest
import re

from scraper.scraper.items import Job

class GradsunSpider(scrapy.Spider):
    name = "gradsun_spider"
    allowed_domains = ['indeed.com']
    start_urls = ['https://ca.indeed.com/jobs?q=software%20developer']

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, wait_time=10, callback=self.parse)

    def parse(self, response):
        SET_SELECTOR = 'td .resultContent'
        for section in response.selector.css(SET_SELECTOR):
            item = Job()
            try:
                item['title'] = re.search('title="(.+?)"', section.get()).group(1)
                item['company'] = re.search('companyName">(.+?)<', section.get()).group(1)
            except Exception as e:
                # skip because it's important
                continue
            
            try:
                item['salary'] = re.search('salary-snippet"><span>(.+?)<', section.get()).group(1)
            except:
                # yield it because it's not important
                pass

            yield item