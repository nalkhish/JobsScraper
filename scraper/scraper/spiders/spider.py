import re
import time
import random
from typing import List, Type

import scrapy
from scrapy_selenium import SeleniumRequest
from scraper.scraper.exceptions import InvalidRequiredField

from scraper.scraper.items import Job
from scraper.scraper.serializers import (
    BaseSerializer,
    DetailsSerializer, 
    SummarySerializer, 
    CompanySerializer, SalarySerializer, TitleSerializer, LocationSerializer
)

class IndeedSpider(scrapy.Spider):
    name = "indeed_spider"
    allowed_domains = ['indeed.com']
    field_classes: List[Type[BaseSerializer]] = [
        SummarySerializer,
        TitleSerializer,
        CompanySerializer,
        SalarySerializer,
        LocationSerializer,
        DetailsSerializer
    ]    
    item_class = Job   

    def get_item(self, *args, **kwargs):
        return self.item_class(*args, **kwargs)

    def start_requests(self):
        start_urls = [
            (
                "https://ca.indeed.com/jobs?as_and=software%20developer"
                "&as_phr&as_any=python%20typescript%20javascript%20React.js"
                "&as_not&as_ttl&as_cmp&jt=all&st&salary=%2470k-150k&fromage=15"
                f"&limit=50&start={start}&sort=date&psf=advsrch&from=advancedsearch"
            )
            for start in [0,] # [0, 50, 100, 150, 200, 250]
        ]        

        for url in start_urls:
            # time.sleep(random.randrange(60,600))
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        SET_SELECTOR = 'div.slider_item'
        for section in response.selector.css(SET_SELECTOR):
            job = self.get_item()
            try:
                for field in self.field_classes:
                    try:
                        serializer = field(data=section.get())
                        job[field.name] = serializer.validated_data
                    except Exception as e:
                        if field.required:
                            raise InvalidRequiredField
            except InvalidRequiredField:
                # skip job when parsing required field produces an exception
                continue
            except Exception as e:
                pass
            yield job