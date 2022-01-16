import scrapy


class Job(scrapy.Item):
    company = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()

